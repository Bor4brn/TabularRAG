# Modelin Zorlanabileceği Sorular

Bu sorular Excel dosyasındaki verilerle ilgili olmasına rağmen, karmaşık analizler gerektirdiği için model zorlanabilir:

## 1. Karmaşık İstatistiksel Analiz
**Soru**: "5G aboneliği olan müşterilerin son 6 aylık fatura ortalaması ile 5G aboneliği olmayan müşterilerin fatura ortalaması arasındaki farkın standart sapması nedir ve bu fark hangi şehirlerde en belirgin şekilde görülüyor?"

**Zorluk**: Bu soru çoklu gruplandırma, standart sapma hesaplaması ve şehir bazında karşılaştırma gerektiriyor.

## 2. Çok Koşullu Filtreleme ve Oransal Analiz
**Soru**: "5G destekli cihaz kullanan ancak 5G aboneliği olmayan müşterilerin fatura ortalamasını hesapla, ardından bunları şehirlere göre grupla ve her şehirde bu durumda olan müşteri sayısının toplam müşteri sayısına oranını yüzde olarak göster, sonuçları fatura ortalamasına göre azalan sırada sırala"

**Zorluk**: Çoklu koşul, gruplandırma, oransal hesaplama ve sıralama işlemlerini birlikte yapması gerekiyor.

## 3. Zaman Bazlı Cihaz Değişikliği Analizi
**Soru**: "Mayıs ayından Haziran ayına cihaz markası değiştiren müşterilerin Türkcell tenürü ortalaması ile cihaz markası değiştirmeyen müşterilerin tenür ortalaması arasında anlamlı bir fark var mı? Bu farkı şehir bazında analiz et."

**Zorluk**: İki farklı zaman aralığındaki cihaz bilgilerini karşılaştırma ve istatistiksel analiz gerektiriyor.

## 4. Çoklu Değişken Korelasyon Analizi
**Soru**: "Müşterinin cihazı kullanma süresi, Türkcell tenürü ve son 6 aylık fatura ortalaması arasında nasıl bir korelasyon var? Bu korelasyonu 5G abonelik durumuna göre farklılaştır."

**Zorluk**: Korelasyon hesaplama ve gruplandırılmış korelasyon analizi gerektiriyor.

## 5. Karmaşık Kategorik Analiz
**Soru**: "Her şehirde, en popüler ödeme yöntemi ile en az popüler ödeme yöntemini kullanan müşterilerin fatura ortalamaları arasındaki fark nedir? Bu farkın en yüksek olduğu şehirleri listele."

**Zorluk**: Kategorik verilerde popülerlik hesaplama, gruplandırma ve karşılaştırma işlemleri gerektiriyor.

## 6. Nested Gruplama ve Yüzdelik Analiz
**Soru**: "Fatura yöntemine göre gruplandır, her grup içinde 5G cihaz desteği olan müşterilerin yüzdesini hesapla, sonra bu yüzdelerin şehir bazında dağılımını göster ve en yüksek yüzdeye sahip şehir-fatura yöntemi kombinasyonunu bul."

**Zorluk**: İç içe gruplandırma, yüzdelik hesaplama ve çoklu seviye analiz gerektiriyor.

## 7. Temporal Pattern Analysis
**Soru**: "Mayıs ayında Apple kullanan ama Haziran ayında Samsung'a geçen müşterilerin profil analizi: Bu müşterilerin ortalama tenürleri, fatura ortalamaları ve şehir dağılımları nasıl? Diğer marka değişikliklerinden farkı nedir?"

**Zorluk**: Spesifik marka değişikliği paterni ve karşılaştırmalı analiz gerektiriyor.

## 8. Outlier Detection ve Analiz
**Soru**: "Son 6 aylık fatura ortalaması açısından aykırı değerlere sahip müşterileri tespit et (Q1-1.5*IQR altında veya Q3+1.5*IQR üstünde). Bu aykırı müşterilerin cihaz kullanım süreleri, tenürleri ve 5G abonelik durumları normal müşterilerden nasıl farklılaşıyor?"

**Zorluk**: İstatistiksel aykırı değer tespiti ve karşılaştırmalı profil analizi gerektiriyor.

## 9. Temporal Multi-Device Analysis
**Soru**: "Mayıs ayında iPhone 13 kullanan ama Haziran'da Galaxy S24 Ultra'ya geçen müşterilerin, cihaz değiştirdikleri tarihteki fatura artış oranları ile aynı dönemde Samsung'dan Apple'a geçen müşterilerin fatura değişim oranları arasında anlamlı bir korelasyon var mı? Bu korelasyonu şehir ve tenür seviyelerine göre segmentlere ayırarak analiz et."

**Zorluk**: Çoklu temporal analiz, spesifik model geçişleri, korelasyon hesaplama ve çok boyutlu segmentasyon.

## 10. Advanced Statistical Profiling
**Soru**: "5G aboneliği olan müşterilerin fatura dağılımının çarpıklık (skewness) ve basıklık (kurtosis) değerlerini hesapla. Bu dağılımın normal dağılımdan ne kadar saptığını Shapiro-Wilk testi ile kontrol et. Ardından bu dağılım parametrelerini 5G aboneliği olmayan müşterilerle karşılaştırarak hangi şehirlerde en büyük istatistiksel farklar olduğunu tespit et."

**Zorluk**: İleri düzey istatistiksel hesaplamalar, normallik testleri ve karşılaştırmalı dağılım analizi.

## 11. Complex Nested Conditional Analysis
**Soru**: "Turkcell tenürü 50+ ay olan müşteriler arasında, Mayıs'ta Apple kullanıp Haziran'da Android'e geçenlerle, her iki ayda da aynı markayı kullananları karşılaştır. Fakat sadece 5G destekli cihaz kullanan ve fatura ortalaması şehir ortalamasının üstünde olan müşterileri dahil et. Bu kriterlere uyan müşteri gruplarının cihaz kullanım süresi dağılımlarını box-plot analizi için gerekli Q1, Q3, median ve outlier değerleriyle birlikte sun."

**Zorluk**: Çoklu iç içe filtreleme, conditional logic, aggregation ve istatistiksel dağılım analizi.

## 12. Cross-Dimensional Correlation Matrix
**Soru**: "Müşteri davranış matrisi oluştur: Turkcell tenürü, cihaz kullanım süresi, fatura ortalaması, 5G abonelik durumu ve cihaz değiştirme sıklığı (Mayıs-Haziran arası) arasındaki korelasyon matrisini hesapla. Bu matriste 0.7'den yüksek korelasyona sahip değişken çiftlerini tespit et ve bu çiftlerin hangi şehirlerde en güçlü olduğunu belirle."

**Zorluk**: Korelasyon matrisi hesaplama, threshold filtering ve şehir bazında karşılaştırmalı analiz.

## Neden Bu Sorular Zor?

1. **Çoklu işlem gerektirme**: Filtreleme, gruplandırma, hesaplama ve sıralama işlemlerini birlikte yapma
2. **Karmaşık pandas syntax**: İç içe fonksiyon çağrıları ve method chaining
3. **İstatistiksel hesaplamalar**: Standart sapma, korelasyon, aykırı değer tespiti
4. **Temporal analiz**: Farklı zaman periyodlarındaki verileri karşılaştırma
5. **Çoklu koşullu filtreleme**: Birden fazla koşulu AND/OR ile birleştirme
6. **Nested gruplandırma**: Bir grup içinde başka gruplandırma yapma
