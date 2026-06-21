import streamlit as st
import pandas as pd
import datetime
import os

# Sayfa Genişliği ve Ayarları
st.set_page_config(page_title="Başarı Takip", layout="wide")

# --- Kalıcı Veri Yönetimi ---
DATA_FILE = "veri_kayitlari.csv"

COLUMNS = [
    "Tarih", "Başlangıç", "Bitiş", "Süre (dk)",
    "Ad Soyad", "Konu", "Hedef (Saat)", "Başarı (%)"
]

def veri_yukle():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Eski dosyalarla uyum: eksik sütunları tamamla
        for c in COLUMNS:
            if c not in df.columns:
                df[c] = None
        return df[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)

def veri_kaydet(df):
    df.to_csv(DATA_FILE, index=False)

def sure_metni(dk):
    """Dakikayı 'Xs Ydk' biçiminde yazar."""
    try:
        dk = int(round(float(dk)))
    except (ValueError, TypeError):
        return "0dk"
    saat, dakika = divmod(dk, 60)
    return f"{saat}s {dakika}dk" if saat else f"{dakika}dk"

# --- Motivasyon Sözleri ---
motivasyon_sozleri = [
    "Başarının yolu, denemekten geçer.", "Küçük adımlar, büyük hedeflere götürür.",
    "Bugün, dünden daha fazlasını yapabilirsin.", "Başarı, hazırlık ve fırsatın buluşmasıdır.",
    "Kendine inan, her şeyin yarısını başarmışsın demektir.", "Asla pes etme, büyük şeyler zaman alır.",
    "Zorluklar, başarının değerini artıran süslerdir.", "Dün yaptıklarınla yetiniyorsan, henüz hiçbir şey yapmamışsın demektir."
]

# --- Kullanıcı ve Resim Eşleşmeleri ---
kullanici_sozlugu = {
    "Gizem": "Gizem.png",
    "Gülin": "Gülin.png",
    "Kevser": "Kevser.png",
    "Melek": "melek.png",
    "Tayfun": "tayfun.png"
}

# --- CSS Stilleri ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .soz-kutusu { background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3; font-style: italic; color: #0d47a1; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #4CAF50; color: white; border-radius: 20px; }
    .gun-baslik { background-color: #ffffff; padding: 10px 15px; border-radius: 8px; border-left: 5px solid #4CAF50; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Başarı ve Zaman Yönetimi")

# --- Dinamik Söz Alanı ---
gun_index = datetime.date.today().timetuple().tm_yday % len(motivasyon_sozleri)
st.markdown(f'<div class="soz-kutusu">🌟 <b>Günün Sözü:</b> {motivasyon_sozleri[gun_index]}</div>', unsafe_allow_html=True)
st.markdown("---")

# Verileri dosyadan yükle (oturum başına bir kez)
if 'veri_listesi' not in st.session_state:
    st.session_state.veri_listesi = veri_yukle()
if 'aktif' not in st.session_state:
    st.session_state.aktif = None  # çalışan kronometre bilgisi

# --- Canlı sayaç (her saniye kendini yeniler) ---
@st.fragment(run_every="1s")
def canli_sayac():
    aktif = st.session_state.get("aktif")
    if aktif:
        gecen = datetime.datetime.now() - aktif["baslangic"]
        toplam = int(gecen.total_seconds())
        s, kalan = divmod(toplam, 3600)
        d, sn = divmod(kalan, 60)
        st.metric("⏱️ Geçen Süre", f"{s:02d}:{d:02d}:{sn:02d}")

# --- Sidebar: Kronometre ---
with st.sidebar:
    st.header("⏱️ Çalışma Kronometresi")

    if st.session_state.aktif is None:
        # Kronometre durmuş → yeni çalışma başlat
        isim = st.selectbox("Ad Soyad", list(kullanici_sozlugu.keys()))
        if isim in kullanici_sozlugu and os.path.exists(kullanici_sozlugu[isim]):
            st.image(kullanici_sozlugu[isim], width=100)

        konu = st.text_input("Konu Başlığı")
        hedef_saat = st.number_input("Hedef (Saat) – opsiyonel", min_value=0.0, step=0.5)

        if st.button("BAŞLAT ▶️"):
            if konu.strip() == "":
                st.error("Lütfen konu başlığını doldurunuz.")
            else:
                st.session_state.aktif = {
                    "baslangic": datetime.datetime.now(),
                    "isim": isim,
                    "konu": konu,
                    "hedef": hedef_saat,
                }
                st.rerun()
    else:
        # Kronometre çalışıyor → canlı süre + durdur
        aktif = st.session_state.aktif
        if aktif["isim"] in kullanici_sozlugu and os.path.exists(kullanici_sozlugu[aktif["isim"]]):
            st.image(kullanici_sozlugu[aktif["isim"]], width=100)

        st.info(f"**{aktif['isim']}** çalışıyor\n\n📚 Konu: **{aktif['konu']}**")
        canli_sayac()

        if st.button("DURDUR ⏹️ ve KAYDET"):
            bitis = datetime.datetime.now()
            sure_sn = (bitis - aktif["baslangic"]).total_seconds()
            sure_dk = round(sure_sn / 60, 1)
            sure_saat = sure_sn / 3600
            hedef = aktif["hedef"]
            basari = round((sure_saat / hedef * 100) if hedef > 0 else 0, 2)

            yeni_satir = pd.DataFrame([{
                "Tarih": aktif["baslangic"].strftime("%Y-%m-%d"),
                "Başlangıç": aktif["baslangic"].strftime("%H:%M:%S"),
                "Bitiş": bitis.strftime("%H:%M:%S"),
                "Süre (dk)": sure_dk,
                "Ad Soyad": aktif["isim"],
                "Konu": aktif["konu"],
                "Hedef (Saat)": hedef,
                "Başarı (%)": basari,
            }])
            st.session_state.veri_listesi = pd.concat(
                [st.session_state.veri_listesi, yeni_satir], ignore_index=True
            )
            veri_kaydet(st.session_state.veri_listesi)   # kalıcı kayıt
            st.session_state.aktif = None
            st.success(f"Kaydedildi! Bugün {sure_metni(sure_dk)} çalıştın, {aktif['isim']}! 🌟")
            st.rerun()

# --- Ana Panel: Gün Gün Kayıt Listesi ---
st.subheader("📊 Çalışma Kayıtları (Gün Gün)")

df = st.session_state.veri_listesi

if df.empty:
    st.info("Henüz kayıt yok. Soldan bir çalışma başlatıp durdurduğunda burada gün gün listelenecek.")
else:
    # Tarihleri en yeniden eskiye doğru sırala
    tarihler = sorted(df["Tarih"].dropna().unique(), reverse=True)

    for t in tarihler:
        grup = df[df["Tarih"] == t]
        gunluk_dk = pd.to_numeric(grup["Süre (dk)"], errors="coerce").fillna(0).sum()

        st.markdown(
            f'<div class="gun-baslik">📅 <b>{t}</b> &nbsp;—&nbsp; '
            f'{len(grup)} kayıt &nbsp;|&nbsp; Toplam: <b>{sure_metni(gunluk_dk)}</b></div>',
            unsafe_allow_html=True
        )

        for _, row in grup.iterrows():
            cols = st.columns([1, 6])
            isim_row = row["Ad Soyad"]
            with cols[0]:
                if isim_row in kullanici_sozlugu and os.path.exists(kullanici_sozlugu[isim_row]):
                    st.image(kullanici_sozlugu[isim_row], width=45)
            with cols[1]:
                st.write(
                    f"🕘 {row['Başlangıç']} – {row['Bitiş']}  |  "
                    f"**{isim_row}** — {row['Konu']}  |  "
                    f"⏱️ {sure_metni(row['Süre (dk)'])}"
                )
                try:
                    hedef = float(row["Hedef (Saat)"])
                    basari = float(row["Başarı (%)"])
                    if hedef > 0:
                        st.progress(min(basari / 100, 1.0))
                except (ValueError, TypeError):
                    pass

    st.divider()

    # Tüm kayıtlar tek tabloda + indirme (silmeden saklanır)
    with st.expander("📋 Tüm kayıtları tablo olarak gör / indir"):
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Tüm Verileri İndir (CSV) 📥", csv, "hedef_takip.csv", "text/csv")
