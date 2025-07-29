# Excel Dosya Analiz Sistemi - RAG Tabanlı

Bu proje, Excel dosyalarındaki verileri analiz eden bir RAG (Retrieval-Augmented Generation) sistemidir. Türkçe dil desteği ile kullanıcıların doğal dil sorularına yanıt verir.

## 🚀 Özellikler

- **Anlamsal Arama**: Excel verilerini embedding vektörleri ile analiz eder
- **Türkçe Dil Desteği**: Türkçe sorular ve yanıtlar
- **Yerel Embedding**: İnternet bağlantısı gerektirmeden çalışır
- **PostgreSQL + pgvector**: Hızlı vektör araması
- **Google Gemini Entegrasyonu**: Akıllı yanıt üretimi
- **Otomatik Veri İşleme**: Excel satırlarını doğal dil cümlelerine dönüştürür

## 📋 Gereksinimler

### Sistem Gereksinimleri
- Python 3.8+
- PostgreSQL 12+ (pgvector uzantısı ile)
- RAM: En az 4GB (embedding modeli için)

### Python Kütüphaneleri
```bash
pip install -r requirements.txt
```

## 🛠️ Kurulum

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/Bor4brn/Excel-File-Analyzer-via-RAG.git
cd Excel-File-Analyzer-via-RAG
```

### 2. PostgreSQL + pgvector Kurulumu
```bash
# PostgreSQL kurulumu (macOS)
brew install postgresql

# pgvector uzantısını ekleyin
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
make install
```

### 3. Veritabanı Oluşturma
```sql
CREATE DATABASE excel_analyzer;
\c excel_analyzer;
CREATE EXTENSION IF NOT EXISTS vector;
```

### 4. Ortam Değişkenlerini Ayarlayın
`.env` dosyası oluşturun:
```env
GEMINI_KEY=your_google_gemini_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/excel_analyzer
```

### 5. Excel Dosyasını Hazırlayın
- `Device Dataset.xlsx` dosyasını proje kök dizinine yerleştirin
- Veya `EXCEL_FILE_PATH` değişkenini güncelleyin

## 🚀 Kullanım

### Sistemi Başlatma
```bash
python main.py
```

## 🏗️ Sistem Mimarisi

### 1. Veri İşleme
- Excel satırları doğal Türkçe cümlelere dönüştürülür
- Her satır için semantic embedding oluşturulur
- Vektörler PostgreSQL'de saklanır

### 2. Sorgulama
- Kullanıcı sorusu embedding'e dönüştürülür
- Cosine similarity ile en yakın veri satırları bulunur
- Gemini LLM ile doğal dil yanıtı üretilir

### 3. Teknoloji Stack
- **Embedding**: `intfloat/multilingual-e5-base`
- **Vector DB**: PostgreSQL + pgvector
- **LLM**: Google Gemini 1.5 Flash
- **Backend**: Python + SQLAlchemy

## 🔧 Yapılandırma

### Embedding Modeli Değiştirme
```python
self.embedding_model = SentenceTransformer('başka-model-adı')
LOCAL_EMBEDDING_DIM = yeni_vektör_boyutu
```

### Top-K Sonuç Sayısı
```python
def query_semantic_data(self, query: str, top_k: int = 15):
```

## 📈 Performans

- **İlk Çalıştırma**: 5-10 dakika (embedding oluşturma)
- **Sonraki Sorular**: 1-3 saniye
- **Bellek Kullanımı**: ~2GB (model + veri)
- **Vektör Arama**: <100ms

## 🐛 Sorun Giderme

### Yaygın Hatalar

**1. Embedding Format Hatası**
```
TextEncodeInput must be Union[TextInputSequence, Tuple[InputSequence, InputSequence]]
```
**Çözüm**: Kod güncellenmiş durumda, tekrar çalıştırın.

**2. PostgreSQL Bağlantı Hatası**
```
connection to server failed
```
**Çözüm**: PostgreSQL servisinin çalıştığından emin olun.

**3. Gemini API Hatası**
```
Invalid API key
```
**Çözüm**: `.env` dosyasında API anahtarını kontrol edin.

## 📞 İletişim

- GitHub: [@Bor4brn](https://github.com/Bor4brn)
- Proje Linki: [https://github.com/Bor4brn/Excel-File-Analyzer-via-RAG](https://github.com/Bor4brn/Excel-File-Analyzer-via-RAG)

---
