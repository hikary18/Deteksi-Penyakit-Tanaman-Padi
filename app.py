import os
import numpy as np
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import InputLayer, Layer
import info_penyakit as di

# ==========================================
# KONFIGURASI HALAMAN (PREMIUM)
# ==========================================
st.set_page_config(
    page_title="RiceGuard AI — Agroscience Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS (ECO-TECH PROFESSIONAL THEME)
# ==========================================
st.markdown("""
    <style>
    /* Mengubah font dan background dasar */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #F4F7F4; /* Soft Sage Clean Background */
    }
    
    /* Kustomisasi Sidebar Premium */
    [data-testid="stSidebar"] {
        background-color: #0E2E14; /* Deep Emerald */
        border-right: 1px solid #1C4424;
    }
    [data-testid="stSidebar"] * {
        color: #E2EFE4 !important;
    }
    
    /* Kustomisasi Card Hasil Diagnosis */
    .metric-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(14, 46, 20, 0.04);
        border: 1px solid #E1EBE2;
        border-left: 6px solid #1B5E20;
        margin-bottom: 20px;
    }
    
    /* Badge Status */
    .danger-badge {
        background-color: #FDF2F2;
        color: #9B1C1C !important;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #FDE8E8;
    }
    
    /* Mengubah Gaya Tab Streamlit agar Sinkron */
    button[data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 500;
        color: #555555 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1B5E20 !important;
        border-bottom-color: #1B5E20 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# JEMBATAN INKOMPATIBILITAS KERAS (ANTI ERROR)
# ==========================================
class SafeInputLayer(InputLayer):
    def __init__(self, *args, **kwargs):
        kwargs.pop('batch_shape', None)
        kwargs.pop('optional', None)
        # Saring jika ada argumen dtype berbentuk dict/Keras 3 policy
        if 'dtype' in kwargs and isinstance(kwargs['dtype'], dict):
            kwargs.pop('dtype')
        super().__init__(*args, **kwargs)

class SafeRescaling(Layer):
    def __init__(self, scale, offset=0.0, **kwargs):
        kwargs.pop('dtype', None) # Buang konfigurasi DTypePolicy yang memicu error
        super().__init__(**kwargs)
        self.scale = scale
        self.offset = offset
    def call(self, inputs):
        return inputs * self.scale + self.offset

# ==========================================
# SAFE PATH & LOAD MODEL
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "rice_model.h5")

@st.cache_resource
def load_rice_model():
    # Mendaftarkan 'InputLayer' dan 'Rescaling' kustom agar tidak memicu error DTypePolicy
    return load_model(
        MODEL_PATH, 
        custom_objects={
            'InputLayer': SafeInputLayer,
            'Rescaling': SafeRescaling
        }
    )

try:
    model = load_rice_model()
    model_status = "🟢 Online"
except Exception as e:
    model_status = f"🔴 Offline ({str(e)})"

# Deklarasi variabel utama agar terhindar dari NameError
classes = ["BrownSpot", "LeafBlast", "LeafSmut", "Healthy"]

# ==========================================
# SIDEBAR PROFESIONAL
# ==========================================
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 20px 0;'><h2 style='color: #FFFFFF; font-weight: 700; letter-spacing: 0.5px; margin: 0;'>RiceGuard AI</h2><p style='color: #A3C9A8; font-size: 13px; font-style: italic; margin-top: 5px;'>Sistem Pakar Komputer Visi Tanaman Padi</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("⚙️ Infrastruktur Sistem")
    st.markdown(f"**Status Core Engine:** {model_status}")
    st.markdown("**Arsitektur:** CNN - Sequential")
    st.markdown(f"**Target Analisis:** {len(classes)} Kategori")
    
    st.markdown("---")
    st.subheader("📋 Matriks Kelas")
    for c in classes:
        st.markdown(f"• {c}")
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 11px; color: #7FA984 !important;'>© 2026 — Universitas PGRI Sumatera Barat</p>", unsafe_allow_html=True)

# ==========================================
# HEADER UTAMA PLATFORM
# ==========================================
st.markdown("<h1 style='color: #0E2E14; font-weight: 700; margin-bottom: 5px;'>Platform Diagnosis Kesehatan Tanaman Padi</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #555555; font-size: 15px;'>Integrasi kecerdasan buatan berbasis visi komputer dan asisten pintar untuk ketahanan pangan nasional.</p>", unsafe_allow_html=True)
st.markdown("---")

# Menggunakan Tabs dengan ikon profesional (Lucide) dari Streamlit
tab_deteksi, tab_chatbot = st.tabs(["scan Deteksi Penyakit", "bot RiceGuard Chat Assistant"])

# ==========================================
# TAB 1: DETEKSI PENYAKIT (COMPUTER VISION)
# ==========================================
with tab_deteksi:
    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.subheader("Input Citra Digital")
        file = st.file_uploader("Unggah sampel foto daun padi (Format: JPG, JPEG, PNG)", type=["jpg", "png", "jpeg"])
        
        if file:
            image = Image.open(file)
            st.image(image, caption="Berkas sampel berhasil dimuat", use_container_width=True)
            
            img = image.resize((224, 224)).convert('RGB')
            img = np.array(img) / 255.0
            img = np.expand_dims(img, axis=0)
            
            btn_analisis = st.button("Jalankan Inferensi AI", type="primary", use_container_width=True)

    with col_output:
        st.subheader("Hasil Analisis Klinis")
        
        if file and 'model' in globals() and "Online" in model_status:
            if btn_analisis:
                with st.spinner("Mengomputasi matriks gambar dan mengekstrak fitur..."):
                    raw_pred = model.predict(img)[0]
                    h5_mapping = {
                        "BrownSpot": raw_pred[0], "Healthy": raw_pred[1],
                        "LeafBlast": raw_pred[2], "LeafSmut": raw_pred[3]
                    }
                    pred = np.array([[h5_mapping[c] for c in classes]])
                    idx = np.argmax(pred[0])
                    confidence = float(np.max(pred[0]))
                    label = classes[idx]
                    info = di.disease_info.get(label, {})
                
                # Render Metrik Profesional
                st.markdown(f"""
                <div class='metric-card'>
                    <span style='font-size: 12px; font-weight: 600; color: #666666; text-transform: uppercase; letter-spacing: 1px;'>Hasil Diagnosis Utama</span>
                    <h2 style='margin: 8px 0 12px 0; color: #0E2E14; font-weight: 700;'>{info.get('nama', label)}</h2>
                    <div><span class='danger-badge'>Tingkat Ancaman: {info.get('tingkat_bahaya', 'Sedang')}</span></div>
                </div>
                """, unsafe_allow_html=True)
                
                st.metric(label="Akurasi Keyakinan Model (Confidence Score)", value=f"{confidence * 100:.2f}%")
                st.progress(confidence)
                
                # Grafik Probabilitas Minimalis & Profesional
                st.markdown("<p style='font-weight: 600; font-size: 14px; margin-top: 15px;'>Distribusi Probabilitas Kelas</p>", unsafe_allow_html=True)
                fig = go.Figure(go.Bar(
                    x=[di.disease_info[c]['nama'] for c in classes],
                    y=pred[0] * 100,
                    marker_color=['#1B5E20' if i == idx else '#C8E6C9' for i in range(len(classes))],
                    text=[f"{val*100:.1f}%" for val in pred[0]],
                    textposition='auto',
                ))
                fig.update_layout(
                    height=220, margin=dict(l=10, r=10, t=10, b=10),
                    yaxis=dict(visible=False),
                    xaxis=dict(tickfont=dict(size=12)),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
                # Lembar Rekomendasi Terstruktur
                st.markdown("---")
                st.markdown("###  Dokumentasi Pengendalian Terpadu")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**🔬 Etiologi / Penyebab:**\n{info.get('penyebab', '-')}")
                    st.markdown(f"**🔍 Karakteristik Gejala:**\n{info.get('gejala', '-')}")
                    st.markdown(f"**📉 Proyeksi Dampak:**\n{info.get('dampak_tanaman', '-')}")
                with c2:
                    st.markdown(f"**💡 Tindakan Agromis (Solusi):**\n{info.get('solusi', '-')}")
                    st.markdown(f"**🛡️ Protokol Pencegahan:**\n{info.get('cara_pencegahan', '-')}")
                    st.markdown(f"**💊 Intervensi Kimiawi (Fungisida):**\n{info.get('obat', '-')}")
            else:
                st.info("Sistem siap. Silakan klik tombol 'Jalankan Inferensi AI' untuk memulai proses diagnosis.")
        else:
            st.info("Menunggu berkas diunggah. Silakan masukkan gambar daun padi pada panel kiri.")

# ==========================================
# TAB 2: CHATBOT AI (LARGE LANGUAGE MODEL)
# ==========================================
with tab_chatbot:
    st.subheader("Asisten Konsultasi Agronomi")
    st.markdown("<p style='color: #666; font-size: 14px;'>Saluran interaktif otomatis untuk berdiskusi seputar agronomi, manajemen hama, dan nutrisi padi.</p>", unsafe_allow_html=True)
    
    import google.generativeai as genai
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        llm_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                "Anda adalah pakar agronomi digital resmi dari platform RiceGuard AI. "
                "Berikan jawaban teknis ilmiah namun mudah dipahami oleh praktisi lapangan pertanian. "
                "Gunakan Bahasa Indonesia yang baku, profesional, dan solutif. Tolak pertanyaan non-pertanian."
            )
        )
    else:
        llm_model = None
        
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Selamat datang di pusat asistensi digital. Silakan deskripsikan kendala budidaya padi yang sedang Anda hadapi."}
        ]
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if user_query := st.chat_input("Masukkan query pertanyaan Anda teknis di sini..."):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        query_lower = user_query.lower()
        bot_response = ""
        
        # Saringan Basis Data Lokal Utama
        if any(x in query_lower for x in ["brown spot", "bercak cokelat", "bercak coklat"]):
            b_info = di.disease_info.get("BrownSpot", {})
            bot_response = f"**Analisis Teknis: Brown Spot (Bercak Cokelat Daun)**\n\n" \
                           f"* **Etiologi:** {b_info.get('penyebab', '-')}\n" \
                           f"* **Manifestasi Gejala:** {b_info.get('gejala', '-')}\n" \
                           f"* **Rekomendasi Penanganan:** {b_info.get('solusi', '-')}"
            
        elif any(x in query_lower for x in ["leaf blast", "blas", "patah leher"]):
            bl_info = di.disease_info.get("LeafBlast", {})
            bot_response = f"**Analisis Teknis: Leaf Blast / Blas Daun**\n\n" \
                           f"* **Etiologi:** {bl_info.get('penyebab', '-')}\n" \
                           f"* **Manifestasi Gejala:** {bl_info.get('gejala', '-')}\n" \
                           f"* **Rekomendasi Penanganan:** {bl_info.get('solusi', '-')}"
            
        elif any(x in query_lower for x in ["wereng", "hama wereng"]):
            bot_response = "**Rekomendasi Teknis Pengendalian Wereng Cokelat:**\n\nLakukan pengeringan berkala pada petakan sawah (irigasi berselang) untuk menurunkan kelembapan mikro. Jika populasi melewati ambang batas ekonomi, aplikasikan insektisida sistemik berbahan aktif *Pimetrozin* dengan nosel mengarah langsung ke area **pangkal batang bawah**."

        elif any(x in query_lower for x in ["tikus", "hama tikus"]):
            bot_response = "**Protokol Manajemen Hama Tikus Sawah:**\n\nTerapkan sanitasi berkala pada pematang sawah, gerakan gropyokan serentak di awal musim tanam, serta implementasikan sistem pagar plastik jebakan TBS (*Trap Barrier System*) pada petak emposan."

        elif any(x in query_lower for x in ["pemupukan", "pupuk"]):
            bot_response = "**Skema Pemupukan Berimbang Komoditas Padi:**\n\n1. **Fase Vegetatif Awal (7-10 HST):** Aplikasi Nitrogen (Urea) makro untuk memacu pertumbuhan vegetatif.\n2. **Fase Vegetatif Lanjut (21-25 HST):** Monitoring warna daun menggunakan Bagan Warna Daun (BWD) sebelum aplikasi Urea tambahan.\n3. **Fase Generatif / Bunting (30-35 HST):** Fokus pada unsur Kalium (KCl) tinggi untuk memperkuat dinding sel batang dan memaksimalkan pengisian bulir padi."

        # Lempar ke Generative AI jika di luar kamus lokal
        else:
            if llm_model:
                try:
                    with st.spinner("Menghubungkan ke pusat data agroscience..."):
                        response = llm_model.generate_content(user_query)
                        bot_response = response.text
                except Exception:
                    bot_response = "⚠️ Gagal melakukan handshake ke server AI. Mohon periksa stabilitas jaringan internet Anda."
            else:
                bot_response = "ℹ️ Fitur asisten cerdas berbasis LLM belum dikonfigurasi sepenuhnya pada backend cloud."
                               
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
