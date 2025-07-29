# Excel Dosya Analiz Sistemi - RAG Tabanlı

Bu proje, Excel dosyalarındaki verileri anlamsal arama (semantic search) yöntemi ile analiz eden bir RAG (Retrieval-Augmented Generation) sistemidir. Türkçe dil desteği ile kullanıcıların doğal dil sorularına yanıt verir.

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

## 📊 Desteklenen Excel Formatı

Sistem aşağıdaki sütunları destekler:
- Mayıs/Haziran Cihazı Marka & Model
- Cihaz Kullanım Süreleri
- 4G/5G Destek Bilgileri
- 5G Abonelik Durumu
- Fatura Bilgileri (Şehir, Yöntem, Ortalama)
- Türkcell Tenür Bilgisi

## 🚀 Kullanım

### Sistemi Başlatma
```bash
python main.py
```

### Örnek Sorular
```
"İstanbul'daki iPhone kullanıcılarının fatura ortalamaları nasıl?"
"5G destekli cihaz kullanan müşteriler hangi şehirlerde yoğun?"
"Samsung Galaxy kullanan müşterilerin tenür dağılımı nasıl?"
"Ankara'da en çok kullanılan cihaz markaları neler?"
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

## 📝 Lisans

MIT License - Detaylar için `LICENSE` dosyasına bakın.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📞 İletişim

- GitHub: [@Bor4brn](https://github.com/Bor4brn)
- Proje Linki: [https://github.com/Bor4brn/Excel-File-Analyzer-via-RAG](https://github.com/Bor4brn/Excel-File-Analyzer-via-RAG)

---

**Not**: Bu sistem embedding tabanlı olarak çalışır ve tüm sorular semantik arama ile yanıtlanır. Pandas kod üretimi devre dışı bırakılmıştır.
