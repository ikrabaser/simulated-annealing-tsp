"""
README için görselleri üretir (gorseller/ klasörüne PNG olarak kaydeder).

  1) el_hesabi_izi.png      : 5 şehirli el hesabında her iterasyonun sonucu
  2) kabul_olasiligi.png    : exp(-delta/T) eğrileri ve gözlenen kabul oranı
  3) yakinsama.png          : 20 şehirli örnekte uzunluğun soğutmayla değişimi
  4) turlar.png             : başlangıç, en yakın komşu + 2-opt ve SA turları
  5) tohum_karsilastirma.png: 10 tohumda SA ve salt tırmanma sonuçları
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import sa
import sa_el_hesabi as el

KLASOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gorseller")
os.makedirs(KLASOR, exist_ok=True)

# Renkler (referans palet, açık tema)
YUZEY = "#fcfcfb"
METIN = "#0b0b0b"
METIN2 = "#52514e"
IZGARA = "#e4e3df"
MAVI = "#2a78d6"
TURUNCU = "#eb6834"
AQUA = "#1baf7a"
GRI = "#8a8985"

plt.rcParams.update({
    "figure.facecolor": YUZEY, "axes.facecolor": YUZEY, "savefig.facecolor": YUZEY,
    "axes.edgecolor": IZGARA, "axes.labelcolor": METIN2, "text.color": METIN,
    "xtick.color": METIN2, "ytick.color": METIN2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": IZGARA, "grid.linewidth": 0.8,
    "axes.axisbelow": True, "font.size": 10, "axes.titlesize": 11,
    "axes.titleweight": "bold", "axes.titlelocation": "left",
    "legend.frameon": False, "figure.dpi": 100,
})


def kaydet(fig, ad):
    yol = os.path.join(KLASOR, ad)
    fig.savefig(yol, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("kaydedildi:", yol)


# ------------------------------------------------------------------ 1) el hesabı izi
def el_hesabi_izi():
    satirlar, _, _ = el.calistir()
    opt_L, _ = el.gercek_optimum()
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    k = [0] + [s["k"] for s in satirlar]
    L = [el.tur_uzunlugu(el.BASLANGIC_TUR)] + [s["L_sonraki"] for s in satirlar]
    ax.step(k, L, where="post", color=MAVI, linewidth=2, zorder=2)
    ax.axhline(opt_L, color=GRI, linestyle="--", linewidth=1.2, zorder=1)
    ax.text(12.1, opt_L + 0.6, f"gerçek optimum = {opt_L}", color=METIN2, ha="right", va="bottom", fontsize=9)
    for s in satirlar:
        x = s["k"]
        if s["kabul"] and s["delta"] < 0:
            ax.plot(x, s["L_sonraki"], "o", color=MAVI, markersize=8, markeredgecolor=YUZEY, markeredgewidth=2, zorder=4)
        elif s["kabul"] and s["delta"] > 0:
            ax.plot(x, s["L_sonraki"], "^", color=TURUNCU, markersize=10, markeredgecolor=YUZEY, markeredgewidth=2, zorder=4)
        elif s["kabul"]:
            ax.plot(x, s["L_sonraki"], "s", color=GRI, markersize=7, markeredgecolor=YUZEY, markeredgewidth=2, zorder=4)
        else:
            ax.plot(x, s["L_aday"], "x", color=METIN2, markersize=8, markeredgewidth=2, zorder=3)
    ax.set_xlabel("iterasyon")
    ax.set_ylabel("tur uzunluğu")
    ax.set_xticks(range(0, 13))
    ax.set_ylim(18, 44)
    ax.set_title("5 şehirli el hesabı: her iterasyonda ne oldu?")
    ax.legend(handles=[
        Line2D([], [], color=MAVI, marker="o", linestyle="", markersize=7, label="daha iyi aday kabul"),
        Line2D([], [], color=TURUNCU, marker="^", linestyle="", markersize=8, label="daha kötü aday kabul (u < P)"),
        Line2D([], [], color=GRI, marker="s", linestyle="", markersize=6, label="eşit aday kabul"),
        Line2D([], [], color=METIN2, marker="x", linestyle="", markersize=7, label="aday reddedildi (aday uzunluğu gösterilir)"),
    ], loc="upper right", fontsize=9)
    kaydet(fig, "el_hesabi_izi.png")


# ------------------------------------------------------------------ 2) kabul olasılığı
def kabul_olasiligi(gecmis):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    T = np.logspace(-1, 2, 300)
    for delta, renk in [(2, MAVI), (5, TURUNCU), (10, AQUA)]:
        ax1.plot(T, np.exp(-delta / T), color=renk, linewidth=2, label=f"Δ = {delta}")
    ax1.set_xscale("log")
    ax1.set_xlim(0.1, 100)
    ax1.set_ylim(0, 1.05)
    ax1.set_xlabel("sıcaklık T (log ölçek)")
    ax1.set_ylabel("kabul olasılığı  exp(−Δ/T)")
    ax1.set_title("Kötüleşme kabul olasılığı")
    ax1.legend(loc="upper left", fontsize=9)

    T_g = np.array(gecmis["T"])
    oran = np.array(gecmis["kabul_orani"])
    pencere = 25
    yumusak = np.convolve(oran, np.ones(pencere) / pencere, mode="valid")
    ax2.plot(T_g, oran, color=MAVI, alpha=0.25, linewidth=1, label="her adım")
    ax2.plot(T_g[pencere - 1:], yumusak, color=MAVI, linewidth=2.2, label=f"{pencere} adımlık ortalama")
    ax2.set_xscale("log")
    ax2.invert_xaxis()
    ax2.set_ylim(0, 1.02)
    ax2.set_xlabel("sıcaklık T (log ölçek, soğuma soldan sağa)")
    ax2.set_ylabel("kabul edilen hamle oranı")
    ax2.set_title("20 şehirli örnekte gözlenen kabul oranı (tohum 6)")
    ax2.legend(loc="upper right", fontsize=9)
    kaydet(fig, "kabul_olasiligi.png")


# ------------------------------------------------------------------ 3) yakınsama
def yakinsama(D, gecmis, gecmis_tirmanma, L_nn_2opt):
    fig, (ax, az) = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={"width_ratios": [1.15, 1]})
    n = len(gecmis["T"])
    adim = np.arange(n)
    L_sa = gecmis["en_iyi_L"][-1]
    L_t = gecmis_tirmanma["en_iyi_L"][-1]

    # Sol: tüm aralık
    ax.plot(adim, gecmis["mevcut_L"], color=MAVI, alpha=0.30, linewidth=1, label="SA mevcut tur")
    ax.plot(adim, gecmis["en_iyi_L"], color=MAVI, linewidth=2.2, label="SA en iyi")
    ax.plot(adim, gecmis_tirmanma["en_iyi_L"], color=TURUNCU, linewidth=2.2, label="salt tırmanma")
    ax.set_yscale("log")
    ax.set_yticks([400, 600, 1000, 1500])
    ax.set_yticklabels(["400", "600", "1000", "1500"])
    ax.set_xlabel("soğutma adımı (her adımda 100 komşu denenir)")
    ax.set_ylabel("tur uzunluğu (log ölçek)")
    ax.set_title("Tüm süreç")
    ax.legend(loc="upper right", fontsize=9)

    # Sağ: yakınlaştırma
    bas = 300
    az.plot(adim[bas:], gecmis["mevcut_L"][bas:], color=MAVI, alpha=0.30, linewidth=1)
    az.plot(adim[bas:], gecmis["en_iyi_L"][bas:], color=MAVI, linewidth=2.2)
    az.plot(adim[bas:], gecmis_tirmanma["en_iyi_L"][bas:], color=TURUNCU, linewidth=2.2)
    az.axhline(L_nn_2opt, color=GRI, linestyle="--", linewidth=1.2)
    az.set_ylim(350, 460)
    az.set_xlim(bas, n + 330)
    az.text(n + 15, L_sa - 1.5, f"SA: {L_sa:.2f}", color=METIN2, va="top", fontsize=9)
    az.text(n + 15, L_t, f"salt tırmanma: {L_t:.2f}", color=METIN2, va="center", fontsize=9)
    az.text(1200, L_nn_2opt + 1.5, f"en yakın komşu + 2-opt = {L_nn_2opt:.2f}", color=METIN2, va="bottom", fontsize=9)
    az.set_xlabel("soğutma adımı")
    az.set_ylabel("tur uzunluğu")
    az.set_title("Yakınlaştırma (adım 300 sonrası)")
    kaydet(fig, "yakinsama.png")


# ------------------------------------------------------------------ 4) turlar
def tur_ciz(ax, xy, tur, baslik, renk):
    t = list(tur) + [tur[0]]
    ax.plot(xy[t, 0], xy[t, 1], color=renk, linewidth=1.6, zorder=1)
    ax.scatter(xy[:, 0], xy[:, 1], s=34, color=METIN, zorder=2, edgecolor=YUZEY, linewidth=1.2)
    ax.scatter(*xy[tur[0]], s=90, facecolor=YUZEY, edgecolor=METIN, linewidth=2, zorder=3)
    ax.set_title(baslik)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for yon in ("left", "bottom"):
        ax.spines[yon].set_visible(False)
    ax.set_aspect("equal")


def turlar(xy, D, tur_rast, L_rast, tur_t, L_t, tur_nn2, L_nn2, tur_sa, L_sa):
    fig, eksenler = plt.subplots(1, 4, figsize=(16, 4.3))
    tur_ciz(eksenler[0], xy, tur_rast, f"Başlangıç (rastgele): {L_rast:.1f}", GRI)
    tur_ciz(eksenler[1], xy, tur_t, f"Salt tırmanma: {L_t:.1f}", TURUNCU)
    tur_ciz(eksenler[2], xy, tur_nn2, f"En yakın komşu + 2-opt: {L_nn2:.1f}", GRI)
    tur_ciz(eksenler[3], xy, tur_sa, f"Benzetim tavlama: {L_sa:.1f}", MAVI)
    kaydet(fig, "turlar.png")


# ------------------------------------------------------------------ 5) tohum karşılaştırması
def tohum_karsilastirma(sonuc_sa, sonuc_tirmanma, L_nn2):
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    tohumlar = np.arange(10)
    ax.axhline(L_nn2, color=GRI, linestyle="--", linewidth=1.2)
    ax.plot(tohumlar, sonuc_tirmanma, "o", color=TURUNCU, markersize=9, markeredgecolor=YUZEY, markeredgewidth=2)
    ax.plot(tohumlar, sonuc_sa, "o", color=MAVI, markersize=9, markeredgecolor=YUZEY, markeredgewidth=2)
    ax.set_xticks(tohumlar)
    ax.set_xlabel("tohum (aynı başlangıç turu her iki yöntemde de kullanıldı)")
    ax.set_ylabel("bulunan en iyi tur uzunluğu")
    ax.set_ylim(350, 410)
    ax.set_title("10 tohumda bulunan en iyi tur uzunluğu")
    ax.legend(handles=[
        Line2D([], [], color=MAVI, marker="o", linestyle="", markersize=8, label="benzetim tavlama"),
        Line2D([], [], color=TURUNCU, marker="o", linestyle="", markersize=8, label="salt tırmanma"),
        Line2D([], [], color=GRI, linestyle="--", linewidth=1.2, label=f"en yakın komşu + 2-opt = {L_nn2:.2f}"),
    ], loc="upper left", fontsize=9)
    kaydet(fig, "tohum_karsilastirma.png")


GOSTERIM_TOHUMU = 6   # salt tırmanmanın yerel optimuma takıldığı tohum (sa.py çıktısındaki 399.32)


def main():
    xy = sa.sehirler_uret(20, tohum=1)
    D = sa.mesafe_matrisi(xy)

    # baz yöntemler
    tur_nn, _ = sa.en_yakin_komsu(D)
    tur_nn2, L_nn2 = sa.iki_opt_yerel_arama(D, tur_nn)

    # gösterim tohumu: SA ve salt tırmanma aynı rastgele başlangıç turundan başlar
    rng0 = np.random.default_rng(GOSTERIM_TOHUMU)
    tur_rast = list(rng0.permutation(len(D)))
    L_rast = sa.tur_uzunlugu(tur_rast, D)
    tur_sa, L_sa, gecmis = sa.benzetim_tavlama(D, tohum=GOSTERIM_TOHUMU)
    tur_t, L_t, gecmis_t = sa.benzetim_tavlama(D, tohum=GOSTERIM_TOHUMU, kotulesme_kabul=False)
    print(f"tohum {GOSTERIM_TOHUMU}: başlangıç {L_rast:.2f}, SA {L_sa:.2f}, salt tırmanma {L_t:.2f}")

    # 10 tohum
    sonuc_sa, sonuc_t = [], []
    for tohum in range(10):
        sonuc_sa.append(sa.benzetim_tavlama(D, tohum=tohum)[1])
        sonuc_t.append(sa.benzetim_tavlama(D, tohum=tohum, kotulesme_kabul=False)[1])

    el_hesabi_izi()
    kabul_olasiligi(gecmis)
    yakinsama(D, gecmis, gecmis_t, L_nn2)
    turlar(xy, D, tur_rast, L_rast, tur_t, L_t, tur_nn2, L_nn2, tur_sa, L_sa)
    tohum_karsilastirma(sonuc_sa, sonuc_t, L_nn2)


if __name__ == "__main__":
    main()
