# Benzetim Tavlama (Simulated Annealing) ile Gezgin Satıcı Problemi

Türkçe | [English](README.en.md)

Benzetim tavlama algoritmasının adım adım el hesabı, aynı hesabı tekrar eden Python kodu ve NumPy ile 20 şehirli genel bir uygulama.

Bu klasördeki tüm sayılar ve görseller kodun çıktısından üretilmiştir.

## Algoritma nedir?

Benzetim tavlama, metalin yavaş soğutularak (tavlanarak) kararlı bir yapıya kavuşmasından esinlenen bir arama yöntemidir. Fikir şudur:

- Her adımda mevcut çözümün küçük bir değişikliği (**komşu çözüm**) denenir.
- Komşu daha iyiyse **her zaman kabul** edilir.
- Komşu daha kötüyse **yine de bir olasılıkla** kabul edilir. Bu olasılık sıcaklığa bağlıdır, sıcaklık yüksekken büyük, düştükçe küçüktür.
- Sıcaklık yavaşça düşürülür. Başta algoritma çok gezinir (yerel optimumlardan çıkabilir), sonda neredeyse yalnızca iyileşmeleri kabul eder.

**Kabul kuralı.** Mevcut çözümün uzunluğu L, adayınki L' olsun ve Δ = L' − L olsun.

- Δ ≤ 0 ise aday kabul edilir.
- Δ > 0 ise P = exp(−Δ / T) hesaplanır. [0,1) aralığında rassal bir u seçilir. **u < P ise kabul**, değilse red.

**Soğutma (geometrik).** T(k+1) = α · T(k)

**Adımlar**

1. Başlangıç turunu ve T₀ sıcaklığını belirle.
2. Mevcut turdan bir komşu tur üret.
3. Δ'yı hesapla, yukarıdaki kurala göre kabul/red kararını ver.
4. Şimdiye kadarki en iyi turu güncelle.
5. T ← α · T.
6. Durma koşulu (iterasyon sayısı ya da T çok küçük) sağlanana kadar 2'ye dön.

## 1. El hesabı: 5 şehirli TSP

Dosya: [`sa_el_hesabi.py`](sa_el_hesabi.py)

### Problem

Şehirler A, B, C, D, E. Simetrik mesafe matrisi:

| | A | B | C | D | E |
|---|---|---|---|---|---|
| **A** | 0 | 3 | 8 | 9 | 6 |
| **B** | 3 | 0 | 4 | 7 | 9 |
| **C** | 8 | 4 | 0 | 5 | 8 |
| **D** | 9 | 7 | 5 | 0 | 3 |
| **E** | 6 | 9 | 8 | 3 | 0 |

- Başlangıç turu: `A-C-E-B-D-A`, d(A,C)=8 + d(C,E)=8 + d(E,B)=9 + d(B,D)=7 + d(D,A)=9 = **41**
- T₀ = 10, α = 0.8, toplam 12 iterasyon
- Komşu: turda iki şehrin yerini değiştirme (swap). A şehri 0. konumda sabit kalır, yer değiştirilecek konumlar 1–4 arasındadır.
- Rassal sayılar elle takip edilebilsin diye **önceden sabitlenmiştir** (hangi iki konumun değişeceği ve kabul testindeki u değerleri kodun başında listelidir).
- Şehir sayısı küçük olduğu için tüm turlar denenerek **gerçek optimum** bulundu: L = 21 (`A-B-C-D-E-A`).

### Ayrıntılı örnek iterasyonlar

#### İterasyon 1 (T = 10.0000)

- Mevcut tur: `A-C-E-B-D-A`, L = 41
- Komşu: 1. ve 3. konumdaki şehirler (C ile B) yer değiştirir → `A-B-E-C-D-A`
- Aday uzunluğu: d(A,B)=3 + d(B,E)=9 + d(E,C)=8 + d(C,D)=5 + d(D,A)=9 = **34**
- Δ = 34 − 41 = **−7**
- Δ ≤ 0 olduğu için aday doğrudan **kabul** edilir.

#### İterasyon 3 (T = 6.4000)

- Mevcut tur: `A-B-D-C-E-A`, L = 29
- Komşu: 1. ve 2. konumdaki şehirler (B ile D) yer değiştirir → `A-D-B-C-E-A`
- Aday uzunluğu: d(A,D)=9 + d(D,B)=7 + d(B,C)=4 + d(C,E)=8 + d(E,A)=6 = **34**
- Δ = 34 − 29 = **+5**
- Δ > 0 olduğu için olasılık hesaplanır: P = exp(−5 / 6.4000) = **0.4578**
- Sabit rassal sayı u = 0.80. u ≥ P olduğundan aday **reddedilir**, tur değişmez.

#### İterasyon 6 (T = 3.2768)

- Mevcut tur: `A-C-D-E-B-A`, L = 28
- Komşu: 2. ve 3. konumdaki şehirler (D ile E) yer değiştirir → `A-C-E-D-B-A`
- Aday uzunluğu: d(A,C)=8 + d(C,E)=8 + d(E,D)=3 + d(D,B)=7 + d(B,A)=3 = **29**
- Δ = 29 − 28 = **+1**
- Δ > 0 olduğu için olasılık hesaplanır: P = exp(−1 / 3.2768) = **0.7370**
- Sabit rassal sayı u = 0.30. u < P olduğundan daha kötü olmasına rağmen aday **kabul** edilir.

#### İterasyon 8 (T = 2.0972)

- Mevcut tur: `A-D-E-C-B-A`, L = 27
- Komşu: 2. ve 4. konumdaki şehirler (E ile B) yer değiştirir → `A-D-B-C-E-A`
- Aday uzunluğu: d(A,D)=9 + d(D,B)=7 + d(B,C)=4 + d(C,E)=8 + d(E,A)=6 = **34**
- Δ = 34 − 27 = **+7**
- Δ > 0 olduğu için olasılık hesaplanır: P = exp(−7 / 2.0972) = **0.0355**
- Sabit rassal sayı u = 0.22. u ≥ P olduğundan aday **reddedilir**, tur değişmez.


### Tüm iterasyonlar

| k | T | mevcut tur (L) | swap | aday tur (L) | Δ | P = exp(−Δ/T) | u | karar | yeni L |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 10.0000 | A-C-E-B-D-A (41) | 1↔3 | A-B-E-C-D-A (34) | −7 | 1 (Δ ≤ 0) | – | kabul | 34 |
| 2 | 8.0000 | A-B-E-C-D-A (34) | 2↔4 | A-B-D-C-E-A (29) | −5 | 1 (Δ ≤ 0) | – | kabul | 29 |
| 3 | 6.4000 | A-B-D-C-E-A (29) | 1↔2 | A-D-B-C-E-A (34) | +5 | 0.4578 | 0.80 | red (u ≥ P) | 29 |
| 4 | 5.1200 | A-B-D-C-E-A (29) | 3↔4 | A-B-D-E-C-A (29) | 0 | 1 (Δ ≤ 0) | – | kabul | 29 |
| 5 | 4.0960 | A-B-D-E-C-A (29) | 1↔4 | A-C-D-E-B-A (28) | −1 | 1 (Δ ≤ 0) | – | kabul | 28 |
| 6 | 3.2768 | A-C-D-E-B-A (28) | 2↔3 | A-C-E-D-B-A (29) | +1 | 0.7370 | 0.30 | kabul (u < P) | 29 |
| 7 | 2.6214 | A-C-E-D-B-A (29) | 1↔3 | A-D-E-C-B-A (27) | −2 | 1 (Δ ≤ 0) | – | kabul | 27 |
| 8 | 2.0972 | A-D-E-C-B-A (27) | 2↔4 | A-D-B-C-E-A (34) | +7 | 0.0355 | 0.22 | red (u ≥ P) | 27 |
| 9 | 1.6777 | A-D-E-C-B-A (27) | 1↔2 | A-E-D-C-B-A (21) | −6 | 1 (Δ ≤ 0) | – | kabul | 21 |
| 10 | 1.3422 | A-E-D-C-B-A (21) | 3↔4 | A-E-D-B-C-A (28) | +7 | 0.0054 | 0.12 | red (u ≥ P) | 21 |
| 11 | 1.0737 | A-E-D-C-B-A (21) | 1↔4 | A-B-D-C-E-A (29) | +8 | 0.0006 | 0.70 | red (u ≥ P) | 21 |
| 12 | 0.8590 | A-E-D-C-B-A (21) | 2↔3 | A-E-C-D-B-A (29) | +8 | 0.0001 | 0.05 | red (u ≥ P) | 21 |

### Sonuç

- 12 iterasyon sonunda bulunan en iyi tur: `A-E-D-C-B-A`, L = **21**
- Gerçek optimum 21. Bu tur, `A-B-C-D-E-A` optimum turunun ters yönde dolaşılmış hâlidir, uzunluğu aynıdır.
- İterasyon 6'da daha kötü bir aday (Δ > 0) olasılıkla kabul edildi. Reddedilen kötüleşmeler: iterasyon 3, 8, 10, 11, 12.
- En iyi değer (21) iterasyon 9'da bulundu.

![El hesabı izi](gorseller/el_hesabi_izi.png)

> Not: Bu örnekte sabit sayılar optimuma 9 iterasyonda götürdü. Gerçek bir çalıştırmada rassal sayılar farklı olacağından yol farklı olur. Bu nedenle algoritmanın genel davranışı aşağıdaki 20 şehirli testte birden çok tohumla ölçüldü.

> Yuvarlama: Ekrandaki olasılıklar 4 ondalığa yuvarlanmıştır, hesap tam hassasiyetle yapılır. Elle yuvarlayarak giderseniz son hanelerde küçük farklar çıkabilir.

## 2. Genel uygulama: 20 şehirli TSP

Dosya: [`sa.py`](sa.py)

- Şehirler 100×100 karede rassal üretilir (`sehirler_uret(20, tohum=1)`).
- Komşu: **2-opt hamlesi** (turun bir parçasını ters çevirmek). Δ, yalnızca değişen 2 kenardan O(1)'de hesaplanır.
- T₀ = 100, α = 0.995, her sıcaklıkta 100 komşu denenir, T < 0.001 olunca durur.
- Karşılaştırma yöntemleri: rastgele tur, en yakın komşu, en yakın komşu + 2-opt yerel arama ve **salt tırmanma** (aynı kod, ama kötüleşme kabulü kapalı).

### Sonuçlar (tek şehir örneği, 10 tohum)

| yöntem | tur uzunluğu |
|---|---|
| rastgele tur | 1104.76 |
| en yakın komşu | 445.79 |
| en yakın komşu + 2-opt | 366.67 |
| SA, 10 tohum ortalaması | 361.07 |
| SA, en iyi / en kötü | 361.07 / 361.07 |
| salt tırmanma, 10 tohum ortalaması | 370.34 |
| salt tırmanma, en iyi / en kötü | 361.07 / 399.32 |

Her tohumda SA ve salt tırmanma **aynı rastgele başlangıç turundan** başlar:

| tohum | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| SA | 361.07 | 361.07 | 361.07 | 361.07 | 361.07 | 361.07 | 361.07 | 361.07 | 361.07 | 361.07 |
| salt tırmanma | 361.07 | 361.07 | 370.40 | 366.67 | 361.07 | 366.67 | 399.32 | 385.62 | 370.40 | 361.07 |

- SA 10 tohumun hepsinde aynı değere ulaştı (361.07), en yakın komşu + 2-opt'un bulduğundan daha kısa.
- Salt tırmanma 10 tohumdan 4 tanesinde aynı değere ulaştı, diğerlerinde yerel optimuma takıldı (en kötüsü 399.32).
- 361.07'in gerçek optimum olduğunu **kanıtlamadım**. Yalnızca bu tek şehir örneğinde denenen yöntemlerin en iyisi.

### Görseller

Aşağıdaki ilk üç görselde (kabul oranı, yakınsama, turlar) tohum 6 kullanıldı: rastgele başlangıç turu 1065.59, SA sonunda 361.07, salt tırmanma 399.32.

![Kabul olasılığı](gorseller/kabul_olasiligi.png)

Sol grafik: aynı Δ için sıcaklık düştükçe kötüleşmenin kabul olasılığı hızla azalır. Sağ grafik: koddaki gerçek çalıştırmada kabul edilen hamle oranı sıcaklıkla birlikte düşer.

![Yakınsama](gorseller/yakinsama.png)

SA'nın mevcut turu başta kötüleşmeleri kabul ettiği için dalgalanır, soğudukça sakinleşir. Salt tırmanma çok hızlı iner ama ilk yerel optimumda kalır.

![Turlar](gorseller/turlar.png)

![Tohum karşılaştırması](gorseller/tohum_karsilastirma.png)

## Parametrelerin etkisi

- **T₀ (başlangıç sıcaklığı):** Çok düşükse algoritma baştan salt tırmanmaya benzer. Çok yüksekse ilk bölüm boşa gider (rastgele gezinme).
- **α (soğutma oranı):** 1'e yakın olması yavaş soğutma demektir, daha iyi sonuç verir ama daha uzun sürer.
- **Her sıcaklıktaki adım sayısı:** Sıcaklık değişmeden önce çözüm uzayının ne kadar gezileceğini belirler.

Bu depodaki testlerde bu parametreler değiştirilerek karşılaştırma **yapılmadı**, yukarıdaki yorum algoritmanın genel mantığıdır.

## Çalıştırma

```bash
pip install -r requirements.txt

python sa_el_hesabi.py     # 5 şehirli el hesabının adım adım çıktısı
python sa.py               # 20 şehirli test (yaklaşık 30 saniye)
python gorseller_uret.py   # gorseller/ klasörünü yeniden üretir (yaklaşık 35 saniye)
```

## Dosyalar

| dosya | içerik |
|---|---|
| `sa_el_hesabi.py` | 5 şehirli TSP için sabit rassal sayılarla adım adım hesap |
| `sa.py` | genel SA, referans yöntemler ve test |
| `gorseller_uret.py` | README'deki görselleri üretir |
| `gorseller/` | PNG görseller |
