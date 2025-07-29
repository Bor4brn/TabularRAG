# TabularRAG Excel - Türkçe Veri Analizi Chatbot'u

Bu proje, Excel dosyalarını analiz edebilen akıllı bir Türkçe chatbot sistemidir. RAG (Retrieval-Augmented Generation) mimarisi kullanarak hem yapısal veri sorguları hem de semantik arama yapabilir.

## 🚀 Özellikler

- **İkili Analiz Yaklaşımı**: 
  - Yapısal sorgular için Text-to-Pandas dönüşümü
  - Semantik sorgular için embedding tabanlı arama
- **Türkçe Dil Desteği**: Türkçe sorular anlayabilir ve Türkçe cevaplar üretir
- **Yerel Embedding Modeli**: `intfloat/multilingual-e5-base` modeli ile çevrimdışı çalışma
- **PostgreSQL + pgvector**: Vektör veritabanı desteği
- **Google Gemini AI**: Doğal dil işleme ve kod üretimi
- **Otomatik Niyet Tespiti**: Soruları otomatik olarak kategorize eder

## 📋 Gereksinimler

### Sistem Gereksinimleri
- Python 3.8+
- PostgreSQL veritabanı
- pgvector uzantısı yüklü PostgreSQL

### Python Kütüphaneleri
```bash
pip install pandas openpyxl sqlalchemy psycopg2-binary pgvector
pip install sentence-transformers google-generativeai python-dotenv
pip install python-docx numpy warnings
```

## ⚙️ Kurulum

1. **Projeyi klonlayın**:
```bash
git clone <repository-url>
cd TabularRAG_Excel
```

2. **Sanal ortam oluşturun**:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# veya
.venv\Scripts\activate  # Windows
```

3. **Gerekli paketleri yükleyin**:
```bash
pip install -r requirements.txt
```

4. **PostgreSQL veritabanı kurulumu**:
```sql
-- PostgreSQL'de pgvector uzantısını etkinleştirin
CREATE EXTENSION IF NOT EXISTS vector;
```

5. **Ortam değişkenlerini ayarlayın**:
`.env` dosyası oluşturup aşağıdaki bilgileri ekleyin:
```env
GEMINI_KEY=your_google_gemini_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

6. **Excel dosyanızı projeye ekleyin**:
- `Device Dataset.xlsx` dosyasını proje klasöründe bulundurun
- Veya `main.py` dosyasında `EXCEL_FILE_PATH` değişkenini güncelleyin

## 🎯 Kullanım

### Temel Kullanım
```bash
python main.py
```

Program başladıktan sonra çeşitli sorular sorabilirsiniz:

### Örnek Sorular

**Yapısal Veri Sorguları** (Pandas ile işlenir):
```
5G aboneliği olan müşterilerin ortalama faturası nedir?
Şehirlere göre müşteri sayılarını göster
En çok kullanılan cihaz markası hangisi?
```

**Semantik Sorular** (Embedding ile aranır):
```
Apple cihaz kullanan müşteriler hakkında bilgi ver
İzmir'deki müşterilerin durumu nasıl?
5G destekli cihazlar hakkında ne öğrenebilirim?
```

## 🏗️ Sistem Mimarisi

### 1. Niyet Tespiti
- `QUERY_DATASET`: Yapısal veri sorguları
- `QUERY_DOCUMENT`: Semantik arama gerektiren sorular
- `GREETING`: Karşılama mesajları
- `GOODBYE`: Veda mesajları
- `UNSUPPORTED`: Desteklenmeyen sorular

### 2. Veri İşleme Akışı

```mermaid
graph TD
    A[Kullanıcı Sorusu] --> B[Niyet Tespiti]
    B --> C{Niyet Türü}
    C -->|QUERY_DATASET| D[Text-to-Pandas]
    C -->|QUERY_DOCUMENT| E[Semantic Search]
    D --> F[Pandas Kodu Üretimi]
    F --> G[Kod Çalıştırma]
    G --> H[Sonuç Formatı]
    E --> I[Embedding Arama]
    I --> J[İlgili Veriler]
    J --> H
    H --> K[LLM ile Doğal Dil Yanıtı]
```

### 3. Embedding Sistemi
- Excel'deki her satır doğal dil cümlesine dönüştürülür
- Türkçe-uyumlu `multilingual-e5-base` modeli kullanılır
- 768 boyutlu vektörler PostgreSQL'de saklanır
- Cosine similarity ile benzerlik hesaplanır

## 📊 Veri Formatı

Sistem şu tür Excel sütunlarını destekler:
- Cihaz bilgileri (Marka, Model)
- Zaman bazlı veriler (Mayıs/Haziran karşılaştırması)
- Müşteri bilgileri (Şehir, Tenür, Abonelik durumu)
- Finansal veriler (Fatura ortalamaları)
- Kategorik veriler (Ödeme yöntemi, Fatura yöntemi)

## 🔧 Yapılandırma

### Embedding Modeli Değiştirme
```python
# main.py dosyasında
LOCAL_EMBEDDING_DIM = 768  # Model boyutuna göre ayarlayın
embedding_model = SentenceTransformer('model-name')
```

### Batch Boyutu Ayarlama
```python
batch_size = 32  # Sistem performansına göre ayarlayın
```

## 🐛 Hata Giderme

### Yaygın Hatalar

1. **Syntax Error**: Pandas kodu üretiminde hata
   - Soruyu farklı şekilde ifade edin
   - Daha basit terimler kullanın

2. **Database Connection Error**: 
   - PostgreSQL servisinin çalıştığını kontrol edin
   - `.env` dosyasındaki veritabanı URL'ini kontrol edin

3. **Embedding Model Yüklenemedi**:
   - İnternet bağlantınızı kontrol edin
   - Disk alanının yeterli olduğundan emin olun

4. **API Key Hatası**:
   - Google Gemini API anahtarınızı kontrol edin
   - API kotanızın dolmadığından emin olun

## 📈 Performans İyileştirmeleri

- **Batch Processing**: Embedding oluşturma için 32'lik gruplar halinde işlem
- **Database Indexing**: pgvector için IVFFLAT index kullanımı
- **Caching**: İşlenmiş satırlar tekrar işlenmez
- **Memory Management**: Büyük veri setleri için parça parça işlem

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🙏 Teşekkürler

- **Sentence Transformers**: Embedding modeli
- **Google Gemini**: LLM desteği
- **pgvector**: PostgreSQL vektör desteği
- **Pandas**: Veri manipülasyonu

## 📧 İletişim

Herhangi bir sorunuz için issue açabilir veya email gönderebilirsiniz.

---

**Not**: İlk çalıştırmada embedding modeli indirilecek ve Excel verileri işlenecektir. Bu işlem biraz zaman alabilir.
