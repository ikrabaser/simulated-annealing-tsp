"""
Benzetim Tavlama (Simulated Annealing) ile Gezgin Satıcı Problemi - genel uygulama.

- Komşu çözüm: 2-opt hamlesi (turun bir parçasını ters çevirme)
- Soğutma: geometrik, T <- alfa * T
- Kabul: delta <= 0 ise kabul, delta > 0 ise exp(-delta/T) olasılığıyla kabul

Karşılaştırma için referans yöntemler:
  rastgele tur, en yakın komşu, 2-opt yerel arama, ve "sıcaklıksız" SA
  (yalnızca iyileşmeleri kabul eden tırmanma, yani kötüleşme kabulü kapalı).
"""
import math
import numpy as np


def sehirler_uret(n=20, tohum=1):
    rng = np.random.default_rng(tohum)
    return rng.uniform(0, 100, size=(n, 2))


def mesafe_matrisi(xy):
    fark = xy[:, None, :] - xy[None, :, :]
    return np.sqrt((fark ** 2).sum(axis=2))


def tur_uzunlugu(tur, D):
    return float(sum(D[tur[i], tur[(i + 1) % len(tur)]] for i in range(len(tur))))


def iki_opt_delta(tur, i, j, D):
    """tur[i..j] parçasını ters çevirmenin uzunluk farkı (O(1))."""
    n = len(tur)
    a, b = tur[i - 1], tur[i]
    c, d = tur[j], tur[(j + 1) % n]
    return D[a, c] + D[b, d] - D[a, b] - D[c, d]


def benzetim_tavlama(D, T0=100.0, alfa=0.995, T_min=1e-3, adim_basina=100,
                     tohum=0, kotulesme_kabul=True, baslangic=None):
    """
    Her sıcaklıkta `adim_basina` komşu denenir, sonra T <- alfa*T.
    Döndürür: en_iyi_tur, en_iyi_L, geçmiş (sözlük: T, mevcut_L, en_iyi_L, kabul_orani)
    """
    rng = np.random.default_rng(tohum)
    n = len(D)
    tur = list(rng.permutation(n)) if baslangic is None else list(baslangic)
    L = tur_uzunlugu(tur, D)
    en_iyi_tur, en_iyi_L = tur[:], L
    T = T0
    gecmis = dict(T=[], mevcut_L=[], en_iyi_L=[], kabul_orani=[])
    while T > T_min:
        kabul_sayisi = 0
        for _ in range(adim_basina):
            i, j = sorted(rng.choice(np.arange(1, n), size=2, replace=False))
            delta = iki_opt_delta(tur, i, j, D)
            if delta <= 0:
                kabul = True
            elif kotulesme_kabul:
                kabul = rng.random() < math.exp(-delta / T)
            else:
                kabul = False
            if kabul:
                tur[i:j + 1] = tur[i:j + 1][::-1]
                L += delta
                kabul_sayisi += 1
                if L < en_iyi_L - 1e-12:
                    en_iyi_tur, en_iyi_L = tur[:], L
        gecmis["T"].append(T)
        gecmis["mevcut_L"].append(L)
        gecmis["en_iyi_L"].append(en_iyi_L)
        gecmis["kabul_orani"].append(kabul_sayisi / adim_basina)
        T *= alfa
    return en_iyi_tur, tur_uzunlugu(en_iyi_tur, D), gecmis


# ---------------- Referans yöntemler ----------------

def rastgele_tur(D, tohum=0):
    rng = np.random.default_rng(tohum)
    tur = list(rng.permutation(len(D)))
    return tur, tur_uzunlugu(tur, D)


def en_yakin_komsu(D, baslangic=0):
    n = len(D)
    gezildi = [baslangic]
    kalan = set(range(n)) - {baslangic}
    while kalan:
        sonraki = min(kalan, key=lambda c: D[gezildi[-1], c])
        gezildi.append(sonraki)
        kalan.remove(sonraki)
    return gezildi, tur_uzunlugu(gezildi, D)


def iki_opt_yerel_arama(D, tur):
    tur = list(tur)
    n = len(tur)
    iyilesti = True
    while iyilesti:
        iyilesti = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if iki_opt_delta(tur, i, j, D) < -1e-10:
                    tur[i:j + 1] = tur[i:j + 1][::-1]
                    iyilesti = True
    return tur, tur_uzunlugu(tur, D)


def main():
    xy = sehirler_uret(20, tohum=1)
    D = mesafe_matrisi(xy)

    _, L_rast = rastgele_tur(D, tohum=0)
    tur_nn, L_nn = en_yakin_komsu(D)
    _, L_2opt = iki_opt_yerel_arama(D, tur_nn)

    print("20 şehir, tek örnek (şehir tohumu = 1)")
    print(f"  rastgele tur            : {L_rast:8.2f}")
    print(f"  en yakın komşu          : {L_nn:8.2f}")
    print(f"  en yakın komşu + 2-opt  : {L_2opt:8.2f}")

    sonuclar_sa, sonuclar_tirmanma = [], []
    for tohum in range(10):
        _, L, _ = benzetim_tavlama(D, tohum=tohum)
        sonuclar_sa.append(L)
        _, L_t, _ = benzetim_tavlama(D, tohum=tohum, kotulesme_kabul=False)
        sonuclar_tirmanma.append(L_t)

    print("\nSA (T0=100, alfa=0.995, 100 adım/sıcaklık), 10 tohum:")
    print("  " + "  ".join(f"{x:.2f}" for x in sonuclar_sa))
    print(f"  ortalama {np.mean(sonuclar_sa):.2f}, en iyi {min(sonuclar_sa):.2f}, en kötü {max(sonuclar_sa):.2f}")
    print("\nKötüleşme kabulü kapalı (salt tırmanma), aynı başlangıçlar, 10 tohum:")
    print("  " + "  ".join(f"{x:.2f}" for x in sonuclar_tirmanma))
    print(f"  ortalama {np.mean(sonuclar_tirmanma):.2f}, en iyi {min(sonuclar_tirmanma):.2f}, en kötü {max(sonuclar_tirmanma):.2f}")


if __name__ == "__main__":
    main()
