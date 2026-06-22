# info_penyakit.py

disease_info = {
    "BrownSpot": {
        "nama": "Brown Spot (Bercak Cokelat Daun)",
        "penyebab": "Jamur Bipolaris oryzae (disebut juga Helminthosporium oryzae). Jamur ini sangat menyukai lingkungan yang lembap dan sering menyerang tanaman padi yang kekurangan zat hara atau ditanam di tanah yang kurang subur.",
        "gejala": "Muncul bercak-bercak berbentuk bulat hingga oval berwarna cokelat tua di permukaan daun, mirip seperti bintik-bintik karat. Pada serangan yang parah, bercak-bercak ini akan menyatu sehingga menyebabkan daun mengering dari ujung dan tampak seperti terbakar.",
        "dampak_tanaman": "Karena daunnya dipenuhi bercak dan mengering, proses memasak makanan (fotosintesis) tanaman menjadi terganggu. Akibatnya, tanaman menjadi kerdil, pertumbuhan terhambat, dan kualitas gabah (padi) menurun drastis—banyak gabah yang menjadi hampa atau berwarna hitam (kusam).",
        "solusi": "Lakukan pemupukan yang berimbang. Pastikan tanaman tidak kekurangan unsur kalium (K) dan nitrogen (N). Jika serangan sudah terlihat menyebar, segera lakukan penyemprotan fungisida pada area yang bergejala.",
        "cara_pencegahan": "Gunakan selalu benih yang bersertifikat dan sehat. Sebelum ditanam, benih bisa direndam terlebih dahulu dengan larutan fungisida dosis rendah (seed treatment) untuk membunuh spora jamur yang menempel pada kulit gabah.",
        "obat": "Fungisida kontak atau sistemik berbahan aktif Mankozeb atau Propineb (Contoh komersial: Dithane M-45, Antracol 70 WP).",
        "cara_penggunaan_fungisida": "Larutkan 2-3 gram bubuk fungisida per 1 liter air bersih ke dalam tangki semprot. Semprotkan secara merata ke seluruh bagian daun yang bergejala pada pagi hari (jam 06.00 - 09.00) atau sore hari saat cuaca cerah dan angin tenang.",
        "tingkat_bahaya": "Sedang (Dapat menurunkan hasil panen secara signifikan jika tanah kurus/kurang pupuk)"
    },

    "LeafBlast": {
        "nama": "Leaf Blast (Penyakit Blas Daun)",
        "penyebab": "Jamur Pyricularia oryzae (Magnaporthe oryzae). Ini adalah salah satu penyakit paling ditakuti petani karena penyebarannya sangat cepat melalui bantuan angin dan percikan air, terutama pada musim hujan dengan kelembapan tinggi.",
        "gejala": "Bercak pada daun berbentuk khas menyerupai belah ketupat atau mata, lebar di tengah dan meruncing di kedua ujungnya. Bagian tengah bercak biasanya berwarna abu-abu keputihan dengan pinggiran berwarna cokelat kemerahan.",
        "dampak_tanaman": "Penyakit ini sangat merusak. Jika jamur ini bermutasi menyerang leher malai (tangkai padi) pada fase generatif, ia akan memicu patah leher (Neck Blast), yang menyebabkan aliran makanan ke bulir padi terputus total sehingga padi menjadi hampa (puso/gagal panen).",
        "solusi": "Segera kurangi penggunaan pupuk Nitrogen (seperti Urea) karena pupuk N yang berlebihan membuat jaringan daun menjadi terlalu lunak dan disukai jamur. Gunakan fungisida sistemik yang kuat untuk menghentikan penyebaran jaringan jamur di dalam daun.",
        "cara_pencegahan": "Gunakan varietas padi yang tahan terhadap penyakit blas (misalnya Inpari 32 atau varietas lokal yang tangguh). Atur jarak tanam agar tidak terlalu rapat (seperti sistem Jajar Legowo) supaya udara dan sinar matahari bisa masuk ke sela-sela tanaman.",
        "obat": "Fungisida sistemik berbahan aktif Tebukonazol, Trifloxistrobin, atau Trisiklazol (Contoh komersial: Nativo 75 WG, Blast 200 SC).",
        "cara_penggunaan_fungisida": "Gunakan dosis sesuai petunjuk kemasan (misalnya 100-150 gram per hektar atau sekitar 0.5 - 1 gram per liter air). Penyemprotan sebaiknya dilakukan secara preventif (pencegahan) saat fase anakan maksimum dan saat padi mulai keluar malai (bunting).",
        "tingkat_bahaya": "Tinggi (Sangat Berbahaya, berpotensi memicu gagal panen total jika menyerang tangkai buah)"
    },

    "LeafSmut": {
        "nama": "Leaf Smut (Penyakit Gosong Daun)",
        "penyebab": "Jamur Entyloma oryzae. Penyakit ini umumnya tergolong penyakit sekunder atau minor yang muncul pada akhir musim tanam, menjelang masa panen saat kondisi lingkungan sangat lembap.",
        "gejala": "Muncul bintik-bintik kecil, sedikit timbul, dan berwarna hitam pekat pada kedua sisi permukaan daun. Jika bintik hitam ini digosok dengan jari, akan meninggalkan bekas jelaga hitam (kumpulan spora jamur).",
        "dampak_tanaman": "Secara umum, penyakit ini tidak terlalu mematikan bagi tanaman padi karena biasanya muncul saat daun kelopak sudah tua. Namun, jika serangannya meluas pada awal pertumbuhan, daun dapat menguning dan mati lebih cepat, yang sedikit mengurangi bobot pengisian gabah.",
        "solusi": "Lakukan sanitasi lahan dengan membersihkan sisa-sisa tanaman yang terinfeksi setelah panen agar spora jamur tidak bertahan di tanah untuk musim tanam berikutnya.",
        "cara_pencegahan": "Terapkan rotasi (pergiliran) tanaman dengan tanaman non-padi (seperti palawija) sesekali waktu. Hindari memberikan air secara digenang terus-menerus; gunakan sistem pengairan berselang (intermittent irrigation) agar permukaan tanah sempat mengering.",
        "obat": "Fungisida berbahan aktif Mankozeb atau Tembaga Hidroksida (Contoh komersial: Mancozeb kuning/biru, Fungisida Tembaga).",
        "cara_penggunaan_fungisida": "Cukup disemprotkan jika intensitas serangan meningkat di lapangan. Campurkan 2 gram per liter air, lalu aplikasikan secara merata pada tanaman padi yang terinfeksi.",
        "tingkat_bahaya": "Rendah (Umumnya tidak membutuhkan penanganan kimia yang masif kecuali serangan meluas di awal musim)"
    },

    "Healthy": {
        "nama": "Sehat (Tanaman Normal)",
        "penyebab": "Tidak ada patogen atau serangan penyakit. Kondisi lingkungan, hara tanah, dan sistem pengairan berjalan dengan sangat baik dan ideal.",
        "gejala": "Daun tanaman padi tampak berdiri tegak, berwarna hijau segar, permukaan mulus bersih tanpa adanya bercak-bercak aneh atau bintik hitam pekat.",
        "dampak_tanaman": "Proses fotosintesis berjalan 100% optimal. Batang padi tumbuh dengan kokoh, pembentukan anakan maksimal, dan pengisian bulir padi dapat berlangsung dengan sempurna sehingga berpotensi menghasilkan panen yang melimpah.",
        "solusi": "Lanjutkan pola perawatan yang sedang berjalan. Jaga kebersihan pematang dari gulma/rumput liar yang bisa menjadi sarang hama pembawa penyakit.",
        "cara_pencegahan": "Tetap lakukan pengamatan (monitoring) secara berkala minimal seminggu sekali untuk memastikan tidak ada serangan hama atau penyakit baru yang masuk ke area sawah.",
        "obat": "Tidak diperlukan pemberian obat-obatan atau fungisida kimia. Tanaman sehat tidak perlu dibebani zat kimia agar ekosistem sawah tetap terjaga.",
        "cara_penggunaan_fungisida": "Tidak perlu diaplikasikan fungisida apa pun. Hemat biaya operasional Anda.",
        "tingkat_bahaya": "Aman (Kondisi Optimal)"
    }
}