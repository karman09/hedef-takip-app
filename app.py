import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Başarı Takip", layout="wide")

DATA_FILE = "veri_kayitlari.csv"

COLUMNS = [
    "Tarih", "Başlangıç", "Bitiş", "Süre (dk)",
    "Ad Soyad", "Konu", "Hedef (Saat)", "Başarı (%)"
]

def veri_yukle():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        for c in COLUMNS:
            if c not in df.columns:
                df[c] = None
        return df[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)

def veri_kaydet(df):
    df.to_csv(DATA_FILE, index=False)

def veri_ekle(yeni_satir_df):
    dosya_var = os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0
    yeni_satir_df.reindex(columns=COLUMNS).to_csv(
        DATA_FILE, mode="a", header=not dosya_var, index=False, encoding="utf-8"
    )

def sure_metni(dk):
    try:
        dk = int(round(float(dk)))
    except (ValueError, TypeError):
        return "0dk"
    saat, dakika = divmod(dk, 60)
    return f"{saat}s {dakika}dk" if saat else f"{dakika}dk"

motivasyon_sozleri = [
    "Başarının yolu, denemekten geçer.", "Küçük adımlar, büyük hedeflere götürür.",
    "Bugün, dünden daha fazlasını yapabilirsin.", "Başarı, hazırlık ve fırsatın buluşmasıdır.",
    "Kendine inan, her şeyin yarısını başarmışsın demektir.", "Asla pes etme, büyük şeyler zaman alır.",
    "Zorluklar, başarının değerini artıran süslerdir.", "Dün yaptıklarınla yetiniyorsan, henüz hiçbir şey yapmamışsın demektir."
]

kullanici_sozlugu = {
    "Gizem": "Gizem.png",
    "Gülin": "Gülin.png",
    "Kevser": "Kevser.png",
    "Melek": "melek.png",
    "Tayfun": "tayfun.png"
}

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

    :root {
        --bg: #EEF1F6;
        --surface: #FFFFFF;
        --ink: #17213C;
        --text: #323C54;
        --muted: #6E778D;
        --accent: #D29333;
        --accent-soft: #FBF2DF;
        --brand: #1E7C70;
        --brand-dark: #155F55;
        --border: #E2E7F0;
    }

    .stApp { background-color: var(--bg); }
    html, body, [class*="css"], .stMarkdown, p, label, input, textarea, select, .stApp { font-family: 'Inter', sans-serif; }
    .stApp h1, .stApp h2, .stApp h3 { font-family: 'Sora', sans-serif; color: var(--ink); letter-spacing: -0.01em; }
    .block-container { padding-top: 2.2rem; max-width: 1100px; }

    .app-altbaslik { color: var(--muted); font-size: 0.98rem; margin: -0.4rem 0 1.1rem 0; font-weight: 500; }

    .soz-kutusu {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 14px;
        padding: 16px 22px;
        margin: 6px 0 22px 0;
        box-shadow: 0 4px 18px rgba(23, 33, 60, 0.05);
        text-align: center;
    }
    .soz-etiket { display: block; color: var(--accent); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 6px; }
    .soz-metin { font-style: italic; color: var(--ink); font-size: 1.06rem; line-height: 1.5; }

    .gun-baslik {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 4px solid var(--ink);
        border-radius: 12px;
        padding: 12px 18px;
        margin: 18px 0 8px 0;
        box-shadow: 0 2px 10px rgba(23, 33, 60, 0.04);
        color: var(--text);
        font-size: 0.95rem;
    }
    .gun-baslik b:first-child { color: var(--ink); font-size: 1.02rem; }
    .gun-toplam { color: var(--brand); font-weight: 700; }

    div.stButton > button {
        background-color: var(--brand);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.1rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 8px rgba(30, 124, 112, 0.25);
        transition: transform 0.12s ease, background-color 0.12s ease, box-shadow 0.12s ease;
    }
    div.stButton > button:hover { background-color: var(--brand-dark); transform: translateY(-1px); box-shadow: 0 4px 14px rgba(30, 124, 112, 0.32); }
    div.stButton > button:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
    div.stButton > button:disabled { background-color: #B9C2CF; box-shadow: none; transform: none; }

    [data-testid="stSidebar"] { background-color: var(--surface); border-right: 1px solid var(--border); }
    [data-testid="stSidebar"] h2 { font-size: 1.1rem; }

    [data-testid="stMetric"] {
        background: var(--accent-soft);
        border: 1px solid #F0E2C2;
        border-radius: 12px;
        padding: 10px 16px;
    }
    [data-testid="stMetricValue"] { font-family: 'Sora', sans-serif; color: var(--ink); }
    [data-testid="stMetricLabel"] { color: var(--muted); }

    .stTextInput input, .stNumberInput input, .stDateInput input, .stTimeInput input {
        border-radius: 9px !important;
    }
    .stProgress > div > div > div > div { background-color: var(--brand) !important; }

    @media (prefers-reduced-motion: reduce) {
        div.stButton > button { transition: none; }
        div.stButton > button:hover { transform: none; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Başarı ve Zaman Yönetimi")
st.markdown('<div class="app-altbaslik">Odaklı çalışma sürelerini başlat, kaydet ve gün gün takip et.</div>', unsafe_allow_html=True)

# Günün sözü veya resmi kısmı
bugun = datetime.date.today()
ozel_tarih = datetime.date(2026, 6, 25) # 

if bugun == ozel_tarih:
    st.markdown('<div class="soz-kutusu">', unsafe_allow_html=True)
    st.image("tebrik.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    gun_index = bugun.timetuple().tm_yday % len(motivasyon_sozleri)
    st.markdown(
        f'<div class="soz-kutusu">'
        f'<span class="soz-etiket">★ Günün Sözü</span>'
        f'<span class="soz-metin">{motivasyon_sozleri[gun_index]}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

st.session_state.veri_listesi = veri_yukle().reindex(columns=COLUMNS)
if 'aktif' not in st.session_state:
    st.session_state.aktif = None

@st.fragment(run_every="1s")
def canli_sayac():
    aktif = st.session_state.get("aktif")
    if aktif:
        gecen = datetime.datetime.now() - aktif["baslangic"]
        toplam = int(gecen.total_seconds())
        s, kalan = divmod(toplam, 3600)
        d, sn = divmod(kalan, 60)
        st.metric("⏱️ Geçen Süre", f"{s:02d}:{d:02d}:{sn:02d}")

with st.sidebar:
    st.header("⏱️ Çalışma Kronometresi")

    if st.session_state.aktif is None:
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
            veri_ekle(yeni_satir)
            st.session_state.aktif = None
            st.success(f"Kaydedildi! Bugün {sure_metni(sure_dk)} çalıştın, {aktif['isim']}! 🌟")
            st.rerun()

    st.markdown("---")
    with st.expander("➕ Manuel Kayıt Ekle"):
        with st.form("manuel_kayit", clear_on_submit=True):
            m_isim = st.selectbox("Ad Soyad", list(kullanici_sozlugu.keys()), key="m_isim")
            m_tarih = st.date_input("Tarih", datetime.date.today(), key="m_tarih")
            sc1, sc2 = st.columns(2)
            m_bas = sc1.time_input("Başlangıç", datetime.time(9, 0), key="m_bas")
            m_bit = sc2.time_input("Bitiş", datetime.time(10, 0), key="m_bit")
            m_konu = st.text_input("Konu Başlığı", key="m_konu")
            m_hedef = st.number_input("Hedef (Saat) – opsiyonel", min_value=0.0, step=0.5, key="m_hedef")
            m_ekle = st.form_submit_button("Kaydet ➕")

        if m_ekle:
            if m_konu.strip() == "":
                st.error("Lütfen konu başlığını doldurunuz.")
            else:
                bas_dt = datetime.datetime.combine(m_tarih, m_bas)
                bit_dt = datetime.datetime.combine(m_tarih, m_bit)
                m_sure_sn = (bit_dt - bas_dt).total_seconds()
                if m_sure_sn <= 0:
                    st.error("Bitiş saati başlangıçtan sonra olmalı.")
                else:
                    m_sure_dk = round(m_sure_sn / 60, 1)
                    m_basari = round((m_sure_sn / 3600 / m_hedef * 100) if m_hedef > 0 else 0, 2)
                    m_satir = pd.DataFrame([{
                        "Tarih": m_tarih.strftime("%Y-%m-%d"),
                        "Başlangıç": m_bas.strftime("%H:%M:%S"),
                        "Bitiş": m_bit.strftime("%H:%M:%S"),
                        "Süre (dk)": m_sure_dk,
                        "Ad Soyad": m_isim,
                        "Konu": m_konu,
                        "Hedef (Saat)": m_hedef,
                        "Başarı (%)": m_basari,
                    }])
                    veri_ekle(m_satir)
                    st.success(f"Manuel kayıt eklendi: {m_isim} — {sure_metni(m_sure_dk)} ✅")
                    st.rerun()

st.subheader("📊 Çalışma Kayıtları (Gün Gün)")

df = st.session_state.veri_listesi

if df.empty:
    st.info("Henüz kayıt yok. Soldan bir çalışma başlatıp durdurduğunda burada gün gün listelenecek.")
else:
    tarihler = sorted(df["Tarih"].dropna().unique(), reverse=True)

    for t in tarihler:
        grup = df[df["Tarih"] == t]
        gunluk_dk = pd.to_numeric(grup["Süre (dk)"], errors="coerce").fillna(0).sum()

        st.markdown(
            f'<div class="gun-baslik">📅 <b>{t}</b> &nbsp;—&nbsp; '
            f'{len(grup)} kayıt &nbsp;|&nbsp; Toplam: <span class="gun-toplam">{sure_metni(gunluk_dk)}</span></div>',
            unsafe_allow_html=True
        )

        for _, row in grup.iterrows():
            cols = st.columns([1, 6])
            isim_row = row["Ad Soyad"]
            with cols[0]:
                if isim_row in kullanici_sozlugu and os.path.exists(kullanici_sozlugu[isim_row]):
                    st.image(kullanici_sozlugu[isim_row], width=45)
            with cols[1]:
                bas_g = row["Başlangıç"] if pd.notna(row["Başlangıç"]) else "—"
                bit_g = row["Bitiş"] if pd.notna(row["Bitiş"]) else "—"
                st.write(
                    f"🕘 {bas_g} – {bit_g}  |  "
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

    with st.expander("🗑️ Kayıt Sil"):
        st.caption("Silmek istediğin kayıtların 'Sil' kutusunu işaretleyip butona bas.")
        sil_df = df.copy()
        sil_df.insert(0, "Sil", False)
        duzenlenen = st.data_editor(
            sil_df,
            use_container_width=True,
            hide_index=True,
            column_config={"Sil": st.column_config.CheckboxColumn("Sil")},
            disabled=[c for c in sil_df.columns if c != "Sil"],
            key="sil_editor",
        )
        secili = int(duzenlenen["Sil"].sum())
        if st.button(f"Seçilenleri Sil 🗑️ ({secili})", disabled=secili == 0):
            kalan = duzenlenen[~duzenlenen["Sil"]].drop(columns=["Sil"])
            veri_kaydet(kalan.reindex(columns=COLUMNS))
            st.success(f"{secili} kayıt silindi.")
            st.rerun()

    with st.expander("📋 Tüm kayıtları tablo olarak gör / indir"):
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Tüm Verileri İndir (CSV) 📥", csv, "hedef_takip.csv", "text/csv")
