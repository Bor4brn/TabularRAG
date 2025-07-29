import os
import json
import time
import random
from dotenv import load_dotenv
import pandas as pd
import warnings
import docx
from sqlalchemy import create_engine, text, inspect, Column, Integer, Text, func
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
EXCEL_FILE_PATH = "Device Dataset.xlsx"
KNOWLEDGE_BASE_PATH = "knowledge_base.docx"

if not GEMINI_API_KEY or not DATABASE_URL:
    raise ValueError("Lütfen .env dosyasında GEMINI_KEY ve DATABASE_URL değişkenlerini ayarlayın.")

genai.configure(api_key=GEMINI_API_KEY)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
LOCAL_EMBEDDING_DIM = 768 

EmbBase = declarative_base()


class DocumentEmbedding(EmbBase):
    __tablename__ = 'document_embeddings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_id = Column(Integer, nullable=False, unique=True)
    text = Column(Text, nullable=False)
    embedding = Column(Vector(LOCAL_EMBEDDING_DIM), nullable=False)


EmbBase.metadata.create_all(engine)

def detect_intent(user_message: str) -> str:
    """Tüm sorguları semantik aramaya yönlendir"""
    user_lower = user_message.lower().strip()

    if any(greeting in user_lower for greeting in ['merhaba', 'selam', 'hello', 'hi', 'hey']):
        return "GREETING"
    elif any(goodbye in user_lower for goodbye in ['hoşça kal', 'görüşürüz', 'bye', 'goodbye', 'exit', 'quit']):
        return "GOODBYE"
    else:
        return "QUERY_DOCUMENT"


def get_dataframe_schema(df: pd.DataFrame, df_name: str = 'df') -> str:
    schema_str = f"You are working with a pandas DataFrame named `{df_name}`.\n"
    schema_str += f"Columns and data types:\n{df.dtypes.to_string()}\n\n"
    schema_str += f"First 3 rows:\n{df.head(3).to_string()}\n"
    return schema_str


def text_to_pandas(user_question: str, df_schema: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    prompt = (
        f"You are an expert Python programmer specializing in pandas. Generate ONLY executable pandas code that works with the existing dataframe 'df'.\n\n"
        f"STRICT REQUIREMENTS:\n"
        f"1. Use ONLY the existing variable 'df' - never create sample data\n"
        f"2. Write code as ONE single line or simple multi-line assignment\n"
        f"3. NO import statements, NO sample data creation, NO comments\n"
        f"4. End with a result that can be evaluated or assigned to 'result'\n"
        f"5. Use exact column names from the schema below\n"
        f"6. For complex operations, break into simple steps with intermediate variables\n\n"
        f"Available DataFrame Schema:\n{df_schema}\n\n"
        f"User Question: {user_question}\n\n"
        f"Generate working pandas code (NO markdown, NO explanations):"
    )

    try:
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.1))
        pandas_code = response.text.strip()
        pandas_code = pandas_code.replace("```python", "").replace("```", "").strip()
        lines = pandas_code.split('\n')
        code_lines = []

        for line in lines:
            line = line.strip()
            if (line and
                not line.startswith('#') and
                not line.startswith('import ') and
                not line.startswith('data = ') and
                not line.startswith('df = pd.DataFrame') and
                not 'sample' in line.lower() and
                not 'example' in line.lower()):
                code_lines.append(line)

        cleaned_code = '\n'.join(code_lines)
        if '\n' in cleaned_code:
            lines = cleaned_code.split('\n')
            if not any('result =' in line for line in lines):
                last_line = lines[-1].strip()
                if not last_line.startswith('result'):
                    lines[-1] = f"result = {last_line}"
                    cleaned_code = '\n'.join(lines)

        return cleaned_code

    except Exception as e:
        print(f"Hata (text_to_pandas): {e}")
        return "# CANNOT_ANSWER"


def execute_pandas_code(pandas_code: str, df: pd.DataFrame) -> str:
    if not pandas_code or "# CANNOT_ANSWER" in pandas_code:
        return json.dumps({"error": "Bu soruyu mevcut verilerle yanıtlayamıyorum."}, ensure_ascii=False)

    try:
        cleaned_code = pandas_code.strip()
        lines = cleaned_code.split('\n')
        filtered_lines = []

        for line in lines:
            line = line.strip()
            if (line and
                not line.startswith('import ') and
                not line.startswith('data = ') and
                not line.startswith('df = pd.DataFrame') and
                not line.startswith('# ') and
                'sample' not in line.lower() and
                'example' not in line.lower()):
                filtered_lines.append(line)

        if not filtered_lines:
            return json.dumps({"error": "Kod temizlendikten sonra boş kaldı."}, ensure_ascii=False)

        final_code = '\n'.join(filtered_lines)
        local_scope = {'df': df, 'pd': pd, 'np': np}

        if len(filtered_lines) == 1:
            single_line = filtered_lines[0]
            if single_line.startswith('result ='):
                exec(single_line, {"__builtins__": {}}, local_scope)
                result = local_scope.get('result')
            else:
                result = eval(single_line, {"__builtins__": {}}, local_scope)
        else:
            if not any('result =' in line for line in filtered_lines):
                last_line = filtered_lines[-1]
                if not last_line.startswith('result'):
                    filtered_lines[-1] = f"result = {last_line}"
                    final_code = '\n'.join(filtered_lines)

            exec(final_code, {"__builtins__": {}}, local_scope)
            result = local_scope.get('result')

        if result is None:
            return json.dumps({"error": "Kod çalıştı ama sonuç None döndü."}, ensure_ascii=False)

        if isinstance(result, pd.DataFrame):
            if result.empty:
                return json.dumps({"message": "Sorguya uygun veri bulunamadı."}, ensure_ascii=False)

            result_data = []
            for idx, row in result.iterrows():
                row_data = row.to_dict()
                row_data['_row_index'] = str(idx)
                result_data.append(row_data)
            return json.dumps(result_data, indent=2, ensure_ascii=False, default=str)

        elif isinstance(result, pd.Series):
            if result.empty:
                return json.dumps({"message": "Sorguya uygun veri bulunamadı."}, ensure_ascii=False)

            series_data = {}
            for idx, val in result.items():
                series_data[str(idx)] = val
            return json.dumps(series_data, indent=2, ensure_ascii=False, default=str)

        else:
            return json.dumps({"result": result}, indent=2, ensure_ascii=False, default=str)

    except SyntaxError as e:
        return json.dumps({"error": f"Kod sözdizimi hatası: {str(e)}. Lütfen daha basit bir sorgu deneyin."}, ensure_ascii=False)
    except Exception as e:
        error_msg = str(e)
        if "invalid syntax" in error_msg:
            return json.dumps({"error": "Kod yapısında bir hata var. Lütfen soruyu farklı şekilde ifade edin."}, ensure_ascii=False)
        else:
            return json.dumps({"error": f"Kod çalıştırılırken hata: {error_msg}"}, ensure_ascii=False)



class LLMClient:
    def __init__(self, model_name="gemini-1.5-flash-latest"):
        self.model_name = model_name

    def chat(self, system_prompt: str, user_prompt: str = None, temperature=0.2):
        model = genai.GenerativeModel(self.model_name)
        full_prompt = f"{system_prompt}\n\n{user_prompt if user_prompt else ''}"
        try:
            response = model.generate_content(full_prompt,
                                              generation_config=genai.types.GenerationConfig(temperature=temperature))
            return response.text.strip()
        except Exception as e:
            print(f"Hata (LLMClient.chat): {e}")
            return "İsteğinizi işlerken bir hata oluştu."

PROMPTS = {
    "GREETING": "Merhaba! Ben sizin veri analisti asistanınızım. Excel dosyanızdaki veriler hakkında neyi merak ediyorsunuz?",
    "GOODBYE": "Yardımcı olabildiğime sevindim. Başka bir sorunuz olursa buradayım. Hoşça kalın!",
    "UNSUPPORTED": "Üzgünüm, bu konu uzmanlık alanımın dışında. Yalnızca sağlanan verilerle ilgili soruları yanıtlayabilirim.",
    "SUMMARIZE_DOCUMENT_RESULT": """Sen Türkçe konuşan bir veri analisti asistanısın. Kullanıcının sorusunu, verilen bağlam bilgileri doğrultusunda yanıtla. 

Bağlam Bilgileri (Veri Satırları):
---
{context}
---

Kullanıcının Sorusu: "{user_question}"

YANIT KURALLARI:
- Türkçe yanıt ver
- Sayısal değerleri açık şekilde belirt 
- Şehir, marka, model gibi detayları dahil et
- Mümkünse karşılaştırmalar ve örnekler ver
- Eğer kesin bir yanıt veremiyorsan, mevcut verilerle ilgili genel bilgi paylaş

Yanıtın:""",
    "SUMMARIZE_DATASET_RESULT": "You are a helpful data analyst assistant. Interpret the result of a data query (in JSON format) and present it to the user in a natural language format.\n\nData Query Result (JSON):\n---\n{data_result}\n---\n\nUser's Original Question: \"{user_question}\"\n\nAnswer:"
}

class AnalystChatbot:
    def __init__(self, excel_path: str):
        self.llm = LLMClient()
        self.db_session = SessionLocal()

        try:
            self.dataframe = pd.read_excel(excel_path)
            self.df_schema = get_dataframe_schema(self.dataframe)
            print(f"'{excel_path}' başarıyla yüklendi. {len(self.dataframe)} satır bulundu.")
        except Exception as e:
            raise RuntimeError(f"Excel dosyası okunurken hata oluştu: {e}")
        print("Türkçe-uyumlu embedding modeli yükleniyor (ilk çalıştırmada biraz zaman alabilir)...")
        self.embedding_model = SentenceTransformer('intfloat/multilingual-e5-base')
        print("Embedding modeli başarıyla yüklendi.")

        self._initialize_excel_embeddings()
    def _initialize_excel_embeddings(self):
        """Excel'deki her satırı yerel modelle vektörleştirir ve veritabanına kaydeder."""

        def row_to_sentence(row):
            """Excel satırını daha anlamlı Türkçe cümlelere dönüştürür."""
            parts = []

            if pd.notna(row.get('Mayıs Cihazı Marka')):
                parts.append(f"Müşterinin mayıs ayında kullandığı cihaz {row['Mayıs Cihazı Marka']} {row.get('Mayıs Cihazı Model', '')}")

            if pd.notna(row.get('Haziran Cihazı Marka')):
                parts.append(f"Haziran ayında kullandığı cihaz {row['Haziran Cihazı Marka']} {row.get('Haziran Cihazı Model', '')}")
            if pd.notna(row.get('Cihazın Toplam Kullanım Süresi (Ay)')):
                parts.append(f"Cihazın toplam kullanım süresi {row['Cihazın Toplam Kullanım Süresi (Ay)']} ay")

            if pd.notna(row.get('Müşterinin Cihazı Kullanma Süresi (Ay)')):
                parts.append(f"Müşterinin cihazı kullanma süresi {row['Müşterinin Cihazı Kullanma Süresi (Ay)']} ay")
            if pd.notna(row.get('Haziran Cihazı 4G Desteği')):
                support_4g = "var" if row['Haziran Cihazı 4G Desteği'] == 1 else "yok"
                parts.append(f"Haziran cihazında 4G desteği {support_4g}")

            if pd.notna(row.get('Haziran Cihazı 5G Desteği')):
                support_5g = "var" if row['Haziran Cihazı 5G Desteği'] == 1 else "yok"
                parts.append(f"Haziran cihazında 5G desteği {support_5g}")

            if pd.notna(row.get('Müşterinin 5G Abonelik Durumu')):
                subscription_5g = "var" if row['Müşterinin 5G Abonelik Durumu'] == 1 else "yok"
                parts.append(f"Müşterinin 5G aboneliği {subscription_5g}")
            if pd.notna(row.get('Turkcell Tenürü')):
                parts.append(f"Türkcell tenürü {row['Turkcell Tenürü']} ay")

            if pd.notna(row.get('Ödeme Yöntemi')):
                parts.append(f"Ödeme yöntemi {row['Ödeme Yöntemi']}")

            if pd.notna(row.get('Fatura Şehri')):
                parts.append(f"Fatura şehri {row['Fatura Şehri']}")

            if pd.notna(row.get('Fatura Yöntemi')):
                parts.append(f"Fatura yöntemi {row['Fatura Yöntemi']}")

            if pd.notna(row.get('Son 6 Aylık Fatura Ortalama')):
                parts.append(f"Son 6 aylık fatura ortalaması {row['Son 6 Aylık Fatura Ortalama']} TL")

            return ". ".join(parts) + "."

        print("Excel satırları doğal dil cümlelerine dönüştürülüyor...")
        chunks = self.dataframe.apply(row_to_sentence, axis=1).tolist()

        last_processed_chunk = self.db_session.query(func.max(DocumentEmbedding.chunk_id)).scalar() or 0

        if last_processed_chunk >= len(chunks):
            print("Tüm Excel satırları zaten işlenmiş. Embedding oluşturma atlanıyor.")
            return

        print(f"Toplam {len(chunks)} satır bulundu. {last_processed_chunk}. satırdan devam ediliyor...")

        batch_size = 32  
        chunks_to_process = chunks[last_processed_chunk:]

        for i in range(0, len(chunks_to_process), batch_size):
            batch_texts = chunks_to_process[i:i + batch_size]
            start_chunk_id = last_processed_chunk + i + 1
            end_chunk_id = start_chunk_id + len(batch_texts) - 1
            print(f"İşleniyor: satırlar {start_chunk_id}-{end_chunk_id} / {len(chunks)}")

            try:
                embedding_vectors = self.embedding_model.encode(batch_texts).tolist()

                for j, embedding_vector in enumerate(embedding_vectors):
                    chunk_id = start_chunk_id + j
                    chunk_text = batch_texts[j]
                    embedding_record = DocumentEmbedding(chunk_id=chunk_id, text=chunk_text, embedding=embedding_vector)
                    self.db_session.add(embedding_record)

                self.db_session.commit()
                print(f"Satırlar {start_chunk_id}-{end_chunk_id} başarıyla kaydedildi.")
            except Exception as e:
                print(f"Hata (Batch {start_chunk_id}-{end_chunk_id}): {e}")
                self.db_session.rollback()
    def query_semantic_data(self, query: str, top_k: int = 10) -> str:
        """Yerel modelle vektör arama yapar - daha fazla sonuç döndürür."""
        try:
            query_embedding = self.embedding_model.encode([query])[0].tolist() 
            results = self.db_session.query(DocumentEmbedding.text).order_by(
                DocumentEmbedding.embedding.cosine_distance(query_embedding)
            ).limit(top_k).all()

            return "\n".join([res[0] for res in results]) if results else ""
        except Exception as e:
            print(f"Hata (query_semantic_data): {e}")
            return ""

    def process_user_request(self, user_question: str) -> str:
        intent = detect_intent(user_question)
        print(f"Tespit Edilen Niyet: {intent}")

        if intent == "GREETING": return PROMPTS["GREETING"]
        if intent == "GOODBYE": return PROMPTS["GOODBYE"]
        if intent == "UNSUPPORTED": return PROMPTS["UNSUPPORTED"]

        if intent == "QUERY_DOCUMENT":
            print("-> Anlamsal Veri (LOKAL RAG) akışı başlatıldı...")
            context = self.query_semantic_data(user_question)
            if not context:
                return "Üzgünüm, bu soruya yanıt verebilecek bir bilgi Excel verilerinde bulunmuyor."
            prompt = PROMPTS["SUMMARIZE_DOCUMENT_RESULT"].format(context=context, user_question=user_question)
            return self.llm.chat(system_prompt=prompt)

        if intent == "QUERY_DATASET":
            print("-> Yapısal Veri (Text-to-Pandas) akışı başlatıldı...")
            pandas_code = text_to_pandas(user_question, self.df_schema)
            print(f"  > Üretilen Pandas Kodu: {pandas_code}")
            data_result = execute_pandas_code(pandas_code, self.dataframe)
            print(f"  > Veri Sonucu (JSON): {data_result[:500]}...")
            prompt = PROMPTS["SUMMARIZE_DATASET_RESULT"].format(data_result=data_result, user_question=user_question)
            return self.llm.chat(system_prompt=prompt)

        return "Sanırım sorunuzu tam olarak anlayamadım. Lütfen farklı bir şekilde ifade eder misiniz?"

    def close_session(self):
        self.db_session.close()
        print("Veritabanı bağlantısı kapatıldı.")


if __name__ == "__main__":
    print("Veri Analisti Asistanı başlatılıyor...")
    chatbot = None
    try:
        chatbot = AnalystChatbot(excel_path=EXCEL_FILE_PATH)
        print("\n" + "=" * 50)
        print("Asistan hazır. Excel verileriniz hakkında yapısal veya anlamsal sorular sorabilirsiniz.")
        print("Çıkmak için 'exit' veya 'quit' yazın.")
        print("=" * 50 + "\n")

        while True:
            user_input = input("Siz: ").strip()
            if not user_input: continue
            if user_input.lower() in ("exit", "quit", "çıkış"):
                print(f"Asistan: {PROMPTS['GOODBYE']}")
                break
            assistant_response = chatbot.process_user_request(user_input)
            print(f"Asistan: {assistant_response}\n")

    except Exception as main_error:
        print(f"\nPROGRAM BAŞLATILIRKEN KRİTİK BİR HATA OLUŞTU: {main_error}")
    finally:
        if chatbot:
            chatbot.close_session()
