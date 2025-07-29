# Sistem İçin Zorlu Sorular

Bu dosya, embedding tabanlı sistemin zorlanabileceği ama verilerde mevcut olan bilgileri içeren sorular listesini içerir.

## 🔥 Karmaşık Analitik Sorular

### 1. Çok Kriterli Filtreleme
```
"5G destekli cihaz kullanan ancak 5G aboneliği olmayan, fatura ortalaması 500 TL'den yüksek olan İstanbul'daki müşterilerin tenür dağılımı nasıl?"
```

### 2. Zaman Bazlı Karşılaştırma  
```
"Mayıs ayından Haziran ayına cihaz markası değiştiren müşterilerin Türkcell tenürü ortalaması ile cihaz markası değiştirmeyen müşterilerin tenür ortalaması arasında anlamlı bir fark var mı? Bu farkı şehir bazında analiz et."
```

### 3. Çapraz Tablo Analizi
```
"Her şehirdeki Apple, Samsung ve Xiaomi kullanıcılarının 5G abonelik oranlarını karşılaştır ve en yüksek 5G benimsenme oranına sahip marka-şehir kombinasyonlarını listele."
```

### 4. Korelasyon Analizi
```
"Cihaz kullanım süresi ile fatura ortalaması arasında korelasyon var mı? Bu korelasyonu marka bazında analiz et ve en güçlü korelasyona sahip markayı bul."
```

### 5. Segmentasyon Analizi
```
"Müşterileri tenür süresine göre 3 gruba ayır (0-50 ay, 51-100 ay, 100+ ay) ve her grubun cihaz tercihi, 5G kullanımı ve fatura ortalaması profilini çıkar."
```

### 6. Anomali Tespiti
```
"Fatura ortalaması şehir ortalamasının 2 katından fazla olan müşterileri tespit et ve bu müşterilerin ortak özelliklerini (cihaz, tenür, abonelik durumu) analiz et."
```

### 7. Trend Analizi
```
"Hangi şehirlerde iPhone 13'ten iPhone 14/15/16 serisine geçiş oranı en yüksek ve bu geçişi yapan müşterilerin fatura değişimi nasıl?"
```

### 8. Çoklu Bağımlılık Analizi
```
"5G aboneliği olan müşterilerin son 6 aylık fatura ortalaması ile 5G aboneliği olmayan müşterilerin fatura ortalaması arasındaki farkın standart sapması nedir ve bu fark hangi şehirlerde en belirgin şekilde görülüyor?"
```

### 9. Coğrafi Dağılım Analizi
```
"Türkiye'nin doğu, batı, güney ve kuzey bölgelerinde cihaz markası tercihlerindeki farklılıkları analiz et ve her bölgede dominant olan markaların fatura ortalamalarını karşılaştır."
```

### 10. Davranışsal Segmentasyon
```
"Aynı cihazı 6 aydan uzun süre kullanan 'sadık kullanıcılar' ile sürekli cihaz değiştiren 'değişken kullanıcılar'ı tanımla ve bu iki grubun demografik ve finansal profillerini karşılaştır."
```

## 🎯 Neden Bu Sorular Zor?

### 1. **Çoklu Filtreleme Gerektiriyor**
- Aynı anda birden fazla kritere göre filtreleme
- Mantıksal operatörler (VE, VEYA, DEĞİL)

### 2. **Matematiksel Hesaplamalar**
- Standart sapma, korelasyon, yüzdelik hesaplar
- Grup bazlı istatistikler

### 3. **Karşılaştırmalı Analiz**
- Gruplar arası fark analizi
- Zaman bazlı değişim tespiti

### 4. **Coğrafi/Kategorik Gruplama**
- Şehirleri bölgelere ayırma
- Dinamik segmentasyon

### 5. **Anomali ve Trend Tespiti**
- Aykırı değer tespiti
- Değişim paternleri

## 💡 Sistemin Bu Sorulara Yaklaşımı

Embedding tabanlı sistem bu soruları şu şekilde ele alır:

1. **Anahtar Kelime Eşleştirme**: "5G", "İstanbul", "iPhone" gibi terimleri arar
2. **Benzer Veri Satırları**: En yakın semantik eşleşmeleri bulur  
3. **Bağlamsal Analiz**: LLM ile genel bir analiz yapar
4. **Sınırlı Matematik**: Kesin hesaplamalar yerine genel değerlendirme

## ⚠️ Beklenen Davranış

Bu zorlu sorularda sistem:
- ✅ İlgili veri satırlarını bulabilir
- ✅ Genel trendleri açıklayabilir
- ✅ Örnek müşteri profillerini gösterebilir
- ❌ Kesin matematik hesapları yapamayabilir
- ❌ Karmaşık filtrelemeler tam olmayabilir
- ❌ İstatistiksel analiz sınırlı olabilir

## 🔄 Test Senaryoları

Bu soruları sistemde test ederken:

1. **Kısmi Başarı Bekleyin**: Tam olmasa da ilgili bilgiler verecektir
2. **Alternatif Soru Deneyin**: Aynı konuyu farklı şekilde sorabilirsiniz
3. **Adım Adım Bölebilirsiniz**: Karmaşık soruları parçalara ayırın

---

Bu sorular, embedding tabanlı sistemin hem gücünü hem de sınırlarını test etmek için tasarlanmıştır.
