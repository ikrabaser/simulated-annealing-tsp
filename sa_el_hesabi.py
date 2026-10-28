"""
Benzetim Tavlama (Simulated Annealing) - 5 şehirli TSP için EL HESABI.

Elle takip edilebilmesi için rassal sayılar önceden sabitlenmiştir:
  - Komşu çözüm: turdaki iki şehrin yerini değiştirme (swap). 0. şehir sabit kalır.
  - Kabul testi: u ~ U(0,1) sayıları da sabit.

Kabul kuralı:
  delta = yeni_uzunluk - mevcut_uzunluk
  delta <= 0  -> yeni çözüm kabul (daha iyi ya da eşit)
  delta  > 0  -> P = exp(-delta / T) hesaplanır, u < P ise kabul (kötüleşme de kabul edilebilir)

Soğutma: T_(k+1) = alpha * T_k   (geometrik)
"""
import itertools
import math

ŞEHİRLER = ["A", "B", "C", "D", "E"]

# Simetrik mesafe matrisi (A, B, C, D, E)
D = [
    [0, 3, 8, 9, 6],
    [3, 0, 4, 7, 9],
    [8, 4, 0, 5, 8],
    [9, 7, 5, 0, 3],
    [6, 9, 8, 3, 0],
]

T0 = 10.0
ALFA = 0.8

BASLANGIC_TUR = [0, 2, 4, 1, 3]

# Her iterasyon için yer değiştirilecek iki konum (konum 0 sabit; 1..4 arası)
SWAP_CIFTLERI = [
    (1, 3), (2, 4), (1, 2), (3, 4), (1, 4), (2, 3),
    (1, 3), (2, 4), (1, 2), (3, 4), (1, 4), (2, 3),
]
# Her iterasyon için kabul testinde kullanılan sabit rassal sayılar
U_SAYILARI = [
    0.62, 0.15, 0.80, 0.07, 0.45, 0.30,
    0.91, 0.22, 0.58, 0.12, 0.70, 0.05,
]


def tur_uzunlugu(tur):
    return sum(D[tur[i]][tur[(i + 1) % len(tur)]] for i in range(len(tur)))


def tur_yaz(tur):
    return "-".join(ŞEHİRLER[c] for c in tur) + "-" + ŞEHİRLER[tur[0]]


def gercek_optimum():
    """Şehir sayısı küçük olduğu için tüm turları deneyerek optimumu bulur."""
    en_iyi = None
    for perm in itertools.permutations(range(1, len(D))):
        tur = [0] + list(perm)
        L = tur_uzunlugu(tur)
        if en_iyi is None or L < en_iyi[0]:
            en_iyi = (L, tur)
    return en_iyi


def calistir():
    tur = BASLANGIC_TUR[:]
    L = tur_uzunlugu(tur)
    en_iyi_tur, en_iyi_L = tur[:], L
    T = T0
    satirlar = []
    for k, ((i, j), u) in enumerate(zip(SWAP_CIFTLERI, U_SAYILARI), start=1):
        aday = tur[:]
        aday[i], aday[j] = aday[j], aday[i]
        L_aday = tur_uzunlugu(aday)
        delta = L_aday - L
        if delta <= 0:
            p = 1.0
            kabul = True
        else:
            p = math.exp(-delta / T)
            kabul = u < p
        satirlar.append(dict(
            k=k, T=T, mevcut=tur[:], L=L, swap=(i, j), aday=aday[:], L_aday=L_aday,
            delta=delta, p=p, u=u, kabul=kabul,
        ))
        if kabul:
            tur, L = aday, L_aday
            if L < en_iyi_L:
                en_iyi_tur, en_iyi_L = tur[:], L
        satirlar[-1]["sonraki"] = tur[:]
        satirlar[-1]["L_sonraki"] = L
        satirlar[-1]["en_iyi_L"] = en_iyi_L
        T = ALFA * T
    return satirlar, en_iyi_tur, en_iyi_L


def main():
    opt_L, opt_tur = gercek_optimum()
    print(f"Başlangıç turu : {tur_yaz(BASLANGIC_TUR)}  L = {tur_uzunlugu(BASLANGIC_TUR)}")
    print(f"T0 = {T0}, alfa = {ALFA}")
    print(f"Gerçek optimum (tüm turlar denenerek): L = {opt_L}  ({tur_yaz(opt_tur)})")
    print()
    satirlar, en_iyi_tur, en_iyi_L = calistir()
    for s in satirlar:
        print(f"--- İterasyon {s['k']}  (T = {s['T']:.4f}) ---")
        print(f"  mevcut : {tur_yaz(s['mevcut'])}  L = {s['L']}")
        i, j = s["swap"]
        print(f"  swap   : konum {i} <-> konum {j}")
        print(f"  aday   : {tur_yaz(s['aday'])}  L = {s['L_aday']}")
        print(f"  delta  : {s['delta']:+d}")
        if s["delta"] <= 0:
            print("  delta <= 0 -> kabul")
        else:
            print(f"  P = exp(-{s['delta']}/{s['T']:.4f}) = {s['p']:.4f},  u = {s['u']:.2f}  ->  "
                  + ("u < P: kabul (kötüleşme kabul edildi)" if s["kabul"] else "u >= P: red"))
        print(f"  sonuç  : {tur_yaz(s['sonraki'])}  L = {s['L_sonraki']}   (şimdiye kadarki en iyi = {s['en_iyi_L']})")
    print()
    print(f"En iyi tur: {tur_yaz(en_iyi_tur)}  L = {en_iyi_L}")


if __name__ == "__main__":
    main()
