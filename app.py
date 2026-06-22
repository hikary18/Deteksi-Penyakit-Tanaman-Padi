import os
import numpy as np
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
from tensorflow.keras.models import load_model
import info_penyakit as di

# ==========================================
# CONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="RiceGuard AI - Deteksi Penyakit Padi",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS (Tema Pertanian Modern)
# ==========================================
st.markdown("""
    <style>
    /* Mengubah warna dasar */
    .stApp {
        background-color: #f9fbf7;
    }
    /* Kustomisasi Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e3f20;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Kustomisasi Card */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #2e7d32;
        margin-bottom: 15px;
    }
    .danger-badge {
        background-color: #ffebee;
        color: #c62828 !important;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .success-badge {
        background-color: #e8f5e9;
        color: #2e7d32 !important;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SAFE PATH & LOAD MODEL
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "rice_model.h5")

@st.cache_resource
def load_rice_model():
    return load_model(MODEL_PATH)

try:
    model = load_rice_model()
    model_status = "🟢 Ready"
except Exception as e:
    model_status = f"🔴 Error: {str(e)}"

# Urutan kelas sesuai keinginan tampilan layout Anda
classes = ["BrownSpot", "LeafBlast", "LeafSmut", "Healthy"]

# ==========================================
# SIDEBAR PROFESIONAL
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 28px;'>🌾 RiceGuard AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>Sistem Cerdas Proteksi Tanaman Padi Menuju Ketahanan Pangan</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("📊 Status Sistem")
    st.markdown(f"**Model CNN:** {model_status}")
    st.markdown("**Arsitektur:** Keras Sequential (CNN)")
    st.markdown(f"**Jumlah Kelas Deteksi:** {len(classes)} Kelas")
    
    st.markdown("---")
    st.subheader("📋 Daftar Kelas")
    for c in classes:
        st.markdown(f"- {c}")
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 12px;'>© 2026 - Pengembangan Sistem Cerdas</p>", unsafe_allow_html=True)

# ==========================================
# HEADER UTAMA
# ==========================================
st.markdown("<h1 style='color: #1e3f20;'>🌾 RiceGuard AI: Deteksi Penyakit Padi Modern</h1>", unsafe_allow_html=True)
st.markdown("Selamat datang di platform diagnosis penyakit tanaman padi berbasis komputer visi. Unggah foto daun padi untuk analisis instan.")
st.markdown("---")

# Menggunakan Tabs untuk memisahkan fitur Utama dan Chatbot AI
tab_deteksi, tab_chatbot = st.tabs(["🔍 Deteksi Penyakit", "💬 RiceGuard Chat Assistant"])

# ==========================================
# TAB 1: DETEKSI PENYAKIT (FITUR UTAMA)
# ==========================================
with tab_deteksi:
    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.markdown("### 📥 Input Gambar Daun")
        file = st.file_uploader("Pilih file gambar daun padi (JPG, JPEG, PNG)", type=["jpg", "png", "jpeg"])
        
        if file:
            image = Image.open(file)
            st.image(image, caption="Gambar yang Diunggah", use_container_width=True)
            
            # Perbaikan Preprocessing: Konversi ke RGB untuk menepis isu citra RGBA (4 channels)
            img = image.resize((224, 224)).convert('RGB')
            img = np.array(img) / 255.0
            img = np.expand_dims(img, axis=0)
            
            # Tombol Analisis
            btn_analisis = st.button("🚀 Mulai Deteksi AI", type="primary", use_container_width=True)

    with col_output:
        st.markdown("### 📊 Hasil Diagnosis AI")
        
        if file and btn_analisis:
            with st.spinner("Menganalisis karakteristik citra daun padi..."):
                # Prediksi mentah dari model (mengikuti urutan alfabetis internal .h5)
                raw_pred = model.predict(img)[0]
                
                # Petakan urutan internal h5 (Alfabetis) ke urutan variabel `classes` Anda
                # Urutan h5: BrownSpot (0), Healthy (1), LeafBlast (2), LeafSmut (3)
                h5_mapping = {
                    "BrownSpot": raw_pred[0],
                    "Healthy": raw_pred[1],
                    "LeafBlast": raw_pred[2],
                    "LeafSmut": raw_pred[3]
                }
                
                # Susun ulang nilai prediksi mengikuti susunan list `classes` Anda
                pred = np.array([[h5_mapping[c] for c in classes]])
                
                # Kalkulasi indeks dan keyakinan dari data yang sudah disinkronkan
                idx = np.argmax(pred[0])
                confidence = float(np.max(pred[0]))
                label = classes[idx]
                
                # Mengambil data dari info_penyakit.py
                info = di.disease_info.get(label, {})
            
            # --- TAMPILKAN METRIK UTAMA ---
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='margin:0; color:#555;'>Hasil Prediksi Tertinggi</h4>
                <h2 style='margin:5px 0; color:#2e7d32;'>{info.get('nama', label)}</h2>
                <p style='margin:0;'>Tingkat Bahaya: <span class='danger-badge'>{info.get('tingkat_bahaya', 'Sedang')}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.metric(label="Confidence Score", value=f"{confidence * 100:.2f}%")
            st.progress(confidence)
            
            # --- CHART PROBABILITAS SEMUA KELAS ---
            st.markdown("#### 📈 Grafik Probabilitas Semua Kelas")
            fig = go.Figure(go.Bar(
                x=[di.disease_info[c]['nama'] for c in classes],
                y=pred[0] * 100,
                marker_color=['#2e7d32' if i == idx else '#a5d6a7' for i in range(len(classes))],
                text=[f"{val*100:.1f}%" for val in pred[0]],
                textposition='auto',
            ))
            fig.update_layout(
                height=250, margin=dict(l=20, r=20, t=20, b=20),
                yaxis=dict(title='Probabilitas (%)', range=[0, 100]),
                xaxis=dict(title='Kategori')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # --- DETAIL INFORMASI PENYAKIT (DARI DATABASE) ---
            st.markdown("---")
            st.markdown("### 📝 Informasi & Penanganan Komprehensif")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**🦠 Penyebab:**\n{info.get('penyebab', '-')}")
                st.markdown(f"**🔍 Gejala Klinis:**\n{info.get('gejala', '-')}")
                st.markdown(f"**⚠️ Dampak Tanaman:**\n{info.get('dampak_tanaman', '-')}")
            with c2:
                st.markdown(f"**💡 Solusi Pengendalian:**\n{info.get('solusi', '-')}")
                st.markdown(f"**🛡️ Cara Pencegahan:**\n{info.get('cara_pencegahan', '-')}")
                st.markdown(f"**💊 Rekomendasi Obat/Fungisida:**\n{info.get('obat', '-')}")
            
            st.markdown("---")
            st.markdown(f"**ℹ️ Panduan Aplikasi Fungisida Umum:**\n{info.get('cara_penggunaan_fungisida', 'Gunakan sesuai dosis anjuran pada kemasan saat pagi atau sore hari ketika cuaca cerah.')}")
            
        elif file:
            st.info("💡 Klik tombol 'Mulai Deteksi AI' di bawah gambar untuk melihat hasil.")
        else:
            st.info("🍃 Silakan unggah gambar daun padi terlebih dahulu pada panel di sebelah kiri.")

# ==========================================
# TAB 2: CHATBOT AI (KNOWLEDGE BASE)
# ==========================================
with tab_chatbot:
    st.markdown("### 💬 RiceGuard Chat Assistant")
    st.markdown("Tanyakan hal terkait penyakit padi, pemupukan, pengendalian jamur, dan tips budidaya tanaman padi.")
    
    # Inisialisasi memory chat internal Streamlit
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Halo! Saya RiceGuard Assistant. Ada yang bisa saya bantu mengenai kesehatan tanaman padi Anda hari ini?"}
        ]
        
    # Render history chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Input dari user
    if user_query := st.chat_input("Ketik pertanyaan Anda di sini... (Contoh: Apa penyebab leaf blast? / Bagaimana pemupukan yang benar?)"):
        # Tampilkan pertanyaan user di UI
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # LOGIKA KNOWLEDGE BASE (Deteksi Kata Kunci Lebih Fleksibel)
        query_lower = user_query.lower()
        bot_response = ""
        
        # 1. Pertanyaan Seputar Brown Spot
        if any(x in query_lower for x in ["brown spot", "bercak cokelat", "bercak coklat"]):
            b_info = di.disease_info.get("BrownSpot", {})
            bot_response = f"**🌾 Mengenal Brown Spot (Bercak Cokelat Daun):**\n\n" \
                           f"* **Apa itu?** Penyakit ini menyerang daun padi dan disebabkan oleh jamur.\n" \
                           f"* **Penyebab Utama:** {b_info.get('penyebab', '-')}\n" \
                           f"* **Ciri/Gejala:** {b_info.get('gejala', '-')}\n" \
                           f"* **Dampak:** {b_info.get('dampak_tanaman', '-')}\n" \
                           f"* **Cara Mengatasi:** {b_info.get('solusi', '-')}"
            
        # 2. Pertanyaan Seputar Leaf Blast
        elif any(x in query_lower for x in ["leaf blast", "blas", "patah leher", "neck blast"]):
            bl_info = di.disease_info.get("LeafBlast", {})
            bot_response = f"**💥 Mengenal Leaf Blast / Blas Daun:**\n\n" \
                           f"* **Apa itu?** Ini salah satu penyakit paling berbahaya bagi padi karena penyebarannya sangat cepat lewat angin.\n" \
                           f"* **Penyebab Utama:** {bl_info.get('penyebab', '-')}\n" \
                           f"* **Ciri/Gejala:** {bl_info.get('gejala', '-')}\n" \
                           f"* **Bahaya Terbesar:** Jika menyerang tangkai/leher malai padi, tangkai bisa patah (Neck Blast) dan bulir padi menjadi hampa total (puso).\n" \
                           f"* **Cara Mengatasi:** {bl_info.get('solusi', '-')}"
            
        # 3. Pertanyaan Seputar Leaf Smut
        elif any(x in query_lower for x in ["leaf smut", "gosong daun", "bintik hitam", "noda hitam"]):
            s_info = di.disease_info.get("LeafSmut", {})
            bot_response = f"**⚫ Mengenal Leaf Smut (Gosong Daun):**\n\n" \
                           f"* **Apa itu?** Penyakit minor yang biasanya muncul di akhir musim tanam saat sawah sangat lembap.\n" \
                           f"* **Penyebab Utama:** {s_info.get('penyebab', '-')}\n" \
                           f"* **Ciri/Gejala:** {s_info.get('gejala', '-')}\n" \
                           f"* **Cara Mencegah:** {s_info.get('cara_pencegahan', '-')}"

        # 4. Pertanyaan Ciri Tanaman Sehat
        elif any(x in query_lower for x in ["tanaman sehat", "ciri padi sehat", "tanaman normal"]):
            h_info = di.disease_info.get("Healthy", {})
            bot_response = f"**🟢 Ciri-Ciri Tanaman Padi yang Sehat:**\n\n" \
                           f"1. {h_info.get('gejala', '-')}\n" \
                           f"2. Batang bagian bawah keras dan kokoh, tidak layu.\n" \
                           f"3. Pertumbuhannya seragam di seluruh petak sawah.\n" \
                           f"4. Akar tanaman berwarna putih kemerahan (menandakan akar aktif menyerap makanan), bukan hitam membusuk.\n\n" \
                           f"**Tips Menjaga:** {h_info.get('solusi', '-')}"

        # 5. Pertanyaan Fungsi Fungisida
        elif "fungsi fungisida" in query_lower:
            bot_response = "**🧪 Apa itu Fungisida & Fungsinya?**\n\n" \
                           "Fungisida adalah obat khusus pertanian yang digunakan untuk **membunuh, menghentikan, atau mencegah pertumbuhan jamur (fungi)**. \n\n" \
                           "Sebagian besar penyakit daun padi (seperti Bercak Cokelat, Blas, dan Gosong Daun) disebabkan oleh jamur, bukan oleh serangga. Oleh karena itu, belilah fungisida di toko pertanian, **bukan insektisida** (obat serangga), agar pengobatannya tepat sasaran."
            
        # 6. Pertanyaan Waktu Penyemprotan
        elif any(x in query_lower for x in ["waktu penyemprotan", "kapan menyemprot", "kapan penyemprotan"]):
            bot_response = "**⏱️ Waktu Paling Tepat untuk Menyemprot Obat Padi:**\n\n" \
                           "* **Pagi Hari (Jam 06.00 - 09.00):** Ini adalah waktu terbaik karena mulut daun (stomata) sedang terbuka lebar, sehingga obat cair akan langsung diserap sempurna oleh tanaman.\n" \
                           "* **Sore Hari (Jam 15.30 - 17.00):** Lapisan matahari sudah tidak terlalu terik, sehingga obat tidak gampang menguap sia-sia.\n" \
                           "* **⚠️ Larangan:** Jangan menyemprot pada siang bolong (obat menguap cepat dan daun bisa stres/terbakar) atau saat menjelang hujan (obat akan luntur tercuci air hujan)."

        # 7. Pertanyaan Pemupukan Padi
        elif any(x in query_lower for x in ["pemupukan", "pupuk", "pupuk padi"]):
            bot_response = "**🌾 Panduan Pemupukan Padi yang Benar (Untuk Orang Awam):**\n\n" \
                           "Aplikasi pupuk idealnya dibagi menjadi 3 tahap utama:\n" \
                           "1. **Tahap 1 (Usia 7-10 Hari Setelah Tanam / HST):** Berikan pupuk **Urea + NPK**. Ini berfokus untuk merangsang pertumbuhan daun baru dan memperbanyak anakan padi.\n" \
                           "2. **Tahap 2 (Usia 21-25 HST):** Berikan pupuk susulan kedua (Urea) untuk menjaga warna daun tetap hijau optimal proses fotosintesis.\n" \
                           "2. **Tahap 3 (Usia 30-35 HST / Fase Bunting):** Tambahkan pupuk **KCL**. Unsur Kalium sangat penting pada fase ini agar batang padi menjadi tegak kokoh (tidak roboh tertiup angin) serta membuat pengisian bulir padi menjadi padat bernas (tidak hampa).\n\n" \
                           "*Tips: Hindari kelebihan pupuk Urea (Nitrogen) saat musim hujan karena daun yang terlalu rimbun dan lunak sangat rawan diserang jamur Blas.*"

        # 8. Pertanyaan Meningkatkan Hasil Panen
        elif any(x in query_lower for x in ["meningkatkan hasil", "panen melimpah", "hasil panen", "meningkatkan panen"]):
            bot_response = "**🚀 4 Kunci Utama Meningkatkan Hasil Panen Padi:**\n\n" \
                           "1. **Pakai Benih Unggul Bersertifikat:** Jangan gunakan benih asalan dari sisa panen sebelumnya yang sudah turun kualitasnya.\n" \
                           "2. **Gunakan Sistem Jajar Legowo:** Pola tanam barisan renggang-rapat ini membuat semua tanaman padi mendapatkan sinar matahari secara merata serta memudahkan petani melakukan pemeliharaan.\n" \
                           "3. **Sistem Pengairan Berselang (Intermittent):** Jangan rendam sawah terus-menerus. Ada kalanya sawah harus dikeringkan sampai tanahnya retak rambut agar akar padi mendapatkan oksigen dan bertumbuh lebih dalam.\n" \
                           "4. **Gunakan Aplikasi Deteksi AI Ini:** Lakukan pengecekan rutin pada daun semenjak dini. Semakin cepat penyakit terdeteksi, semakin murah biaya pengobatan dan potensi gagal panen bisa dicegah!"
                           
        # 10. Pertanyaan Seputar Hama Wereng
        elif any(x in query_lower for x in ["wereng", "wereng coklat", "hama wereng"]):
            bot_response = "**🦟 Cara Mengatasi Hama Wereng Cokelat:**\n\n" \
                           "Wereng adalah salah satu hama pengisap cairan batang padi yang paling berbahaya karena bisa menyebabkan tanaman kering seperti terbakar (*hopperburn*).\n\n" \
                           "* **Langkah Pengendalian:**\n" \
                           "  1. **Keringkan Sawah:** Wereng sangat suka kondisi lembap dan rimbun. Segera keringkan air sawah secara berkala (irigasi berselang).\n" \
                           "  2. **Musuh Alami:** Jaga kelestarian laba-laba atau kepik permukaan air karena mereka adalah pemangsa alami wereng.\n" \
                           "  3. **Pestisida Tepat Pemukul:** Gunakan **Insektisida sistemik** berbahan aktif *Pimetrozin* atau *Imidakloprid*. Semprotkan tepat ke arah **pangkal batang padi** (bawah), bukan di atas daun, karena wereng bersembunyi di bawah dekat permukaan air."

        # 11. Pertanyaan Seputar Hama Tikus
        elif any(x in query_lower for x in ["tikus", "hama tikus", "mengatasi tikus"]):
            bot_response = "**🐀 Strategi Jitu Mengendalikan Hama Tikus Sawah:**\n\n" \
                           "Tikus adalah hama cerdas yang menyerang padi di segala usia, terutama saat fase bunting. Membasmi tikus tidak bisa sendirian, harus dilakukan serempak satu hamparan sawah.\n\n" \
                           "* **Cara Terbaik (Gropyokan & TBS):**\n" \
                           "  1. **Sanitasi Pematang:** Bersihkan pematang sawah dari rumput tinggi dan bongkar lubang-lubang aktif tempat tikus bersembunyi.\n" \
                           "  2. **Tanam Serempak:** Jadwal tanam dalam satu kelompok tani tidak boleh beda lebih dari 2 minggu agar makanan tikus tidak tersedia sepanjang tahun.\n" \
                           "  3. **Sistem TBS (Trap Barrier System):** Memasang pagar plastik mengelilingi petak sawah kecil yang dipasangi bubu perangkap di beberapa pintunya.\n" \
                           "  4. **Umpan Beracun:** Gunakan rodentisida (racun tikus) jenis *antikoagulan* yang efeknya lambat, agar tikus lain tidak curiga dan ikut memakan umpan tersebut."

        # 12. Pertanyaan Seputar Padi Roboh / Rebah
        elif any(x in query_lower for x in ["padi roboh", "padi rebah", "batang lemah"]):
            bot_response = "**🌪️ Mengapa Padi Mudah Roboh dan Bagaimana Mencegahnya?**\n\n" \
                           "Padi yang rebah menjelang panen sangat merugikan karena gabah bisa membusuk atau dimakan tikus akibat menyentuh tanah basah.\n\n" \
                           "* **Penyebab Utama:** Terlalu banyak pupuk Nitrogen (Urea) sehingga tanaman terlalu tinggi dan batangnya tipis/lunak, ditambah angin kencang atau hujan lebat.\n" \
                           "* **Solusi Pencegahan:**\n" \
                           "  1. **Kurangi Urea, Tambah KCL:** Pupuk Kalium (KCL) berfungsi mempertebal dinding sel sehingga batang tanaman menjadi keras dan tangguh.\n" \
                           "  2. **Gunakan Silika (Si):** Jika memungkinkan, berikan pupuk mikro yang mengandung unsur Silika untuk memberi efek 'baju zirah' atau pengaku pada batang padi.\n" \
                           "  3. **Pilih Varietas Berbatang Pendek:** Tanam benih yang karakteristik batangnya pendek dan kekar."

        # 13. Pertanyaan Seputar Tanah Masam / Menguning (Asem-aseman)
        elif any(x in query_lower for x in ["asem-aseman", "tanah masam", "daun menguning bawah"]):
            bot_response = "**🧪 Mengatasi Gejala Asem-Aseman (Tanah Terlalu Masam):**\n\n" \
                           "Gejala asem-aseman ditandai dengan pertumbuhan padi yang macet (kerdil), daun menguning kemerahan dari bawah/ujung, dan akar berwarna cokelat tua berbau busuk.\n\n" \
                           "* **Penyebab:** Pembusukan sisa jerami musim lalu yang belum selesai sempurna akibat sawah terus-menerus digenangi air tanpa jeda pengeringan.\n" \
                           "* **Solusi Cepat:**\n" \
                           "  1. **Keringkan Total:** Buang semua air di sawah agar racun gas di dalam tanah menguap dan akar mendapatkan oksigen.\n" \
                           "  2. **Taburkan Kapur Pertanian (Dolomit):** Taburkan dolomit untuk menaikkan pH tanah yang anjlok ke angka normal (pH ideal padi: 6 - 7).\n" \
                           "  3. **Tunda Pemupukan Urea:** Jangan beri pupuk Urea saat padi sedang asem-aseman, karena justru akan memperparah pembusukan akar."
            
            # Jawaban jika pertanyaan tidak dikenali
        else:
            bot_response = "🙏 **Maaf, saya belum memahami pertanyaan tersebut secara spesifik.**\n\n" \
                           "Asisten pintar kesehatan padi, Anda bisa mencoba mengetik pertanyaan seputar topik berikut agar saya dapat membantu dengan maksimal:\n\n" \
                           "* ❓ *'Bagaimana cara mengatasi hama wereng coklat?'*\n" \
                           "* ❓ *'Bagaimana mengendalikan hama tikus sawah?'*\n" \
                           "* ❓ *'Mengapa tanaman padi saya gampang roboh?'*\n" \
                           "* ❓ *'Apa obat untuk penyakit Leaf Blast?'*\n" \
                           "* ❓ *'Bagaimana solusi untuk padi yang kena asem-aseman?'*"
                           
        # Tampilkan jawaban bot di UI
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})