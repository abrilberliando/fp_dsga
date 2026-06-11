# 🧪 Skenario Pengujian Risiko Food Waste

Berikut adalah 10 skenario pengujian komprehensif yang telah disesuaikan dengan 5 input terbaru di aplikasi. Anda dapat langsung menyalin nilai-nilai ini ke formulir untuk melihat bagaimana AI mendeteksi berbagai jenis bahaya.

---

## 🟢 Kategori: AMAN (Risiko Rendah)

### Skenario 1: Kondisi Sempurna (Barang Baru)
Produk baru masuk dengan suhu yang tepat dan margin harga wajar.
- **Jenis Produk:** Roti & Kue (Bakery)
- **Kondisi Suhu Penyimpanan:** Suhu Ruang Ber-AC (20°C)
- **Sisa hari sebelum kadaluarsa:** 10
- **Harga modal:** 10.000
- **Harga jual:** 15.000
> **Ekspektasi Hasil:** **Aman**. AI mendeteksi siklus penjualan roti normal.

### Skenario 2: Aman Jangka Panjang (Long Expiry)
Minuman awet yang disiapkan untuk dijual dalam jangka waktu lama.
- **Jenis Produk:** Minuman (Beverages)
- **Kondisi Suhu Penyimpanan:** Suhu Ruang Biasa (25°C)
- **Sisa hari sebelum kadaluarsa:** 120
- **Harga modal:** 5.000
- **Harga jual:** 8.000
> **Ekspektasi Hasil:** **Sangat Aman**. Algoritma *Long Expiry Safeguard* akan mengesampingkan potensi pembusukan karena waktunya masih berbulan-bulan.

---

## 🟡 Kategori: WASPADA (Risiko Sedang)

### Skenario 3: Mendekati Masa Kritis
Sayuran mulai beranjak layu dan batas kadaluarsa tinggal beberapa hari lagi.
- **Jenis Produk:** Sayur & Buah Segar (Produce)
- **Kondisi Suhu Penyimpanan:** Chiller / Kulkas (4°C)
- **Sisa hari sebelum kadaluarsa:** 4
- **Harga modal:** 20.000
- **Harga jual:** 25.000
> **Ekspektasi Hasil:** **Waspada**. Sistem mendeteksi sisa hari < 5 dan akan mulai merekomendasikan diskon ringan agar cepat laku.

### Skenario 4: Panas Ekstrem di Gudang
Penyimpanan yang salah menaikkan peluang pembusukan lebih cepat.
- **Jenis Produk:** Roti & Kue (Bakery)
- **Kondisi Suhu Penyimpanan:** Panas (>28°C)
- **Sisa hari sebelum kadaluarsa:** 8
- **Harga modal:** 10.000
- **Harga jual:** 14.000
> **Ekspektasi Hasil:** **Waspada/Berbahaya**. Suhu > 25°C langsung memicu penalti risiko dari *Business Guard*.

---

## 🔴 Kategori: BERBAHAYA (Tindakan Segera)

### Skenario 5: Kesalahan Penyimpanan Fatal (Produk Beku Mencair)
Kesalahan fatal staf toko meletakkan makanan beku di rak biasa.
- **Jenis Produk:** Makanan Beku (Frozen Meals)
- **Kondisi Suhu Penyimpanan:** Suhu Ruang Biasa (25°C)
- **Sisa hari sebelum kadaluarsa:** 360
- **Harga modal:** 40.000
- **Harga jual:** 55.000
> **Ekspektasi Hasil:** **Sangat Berbahaya (>90%)**. Walaupun kadaluarsanya masih 1 TAHUN lagi, makanan beku di suhu ruang akan busuk/mencair dalam hitungan jam!

### Skenario 6: Daging Mentah Salah Suhu
Sama halnya dengan Skenario 5, namun untuk komoditas mentah.
- **Jenis Produk:** Daging Mentah (Meat)
- **Kondisi Suhu Penyimpanan:** Suhu Ruang Ber-AC (20°C)
- **Sisa hari sebelum kadaluarsa:** 14
- **Harga modal:** 80.000
- **Harga jual:** 100.000
> **Ekspektasi Hasil:** **Sangat Berbahaya (>90%)**. Daging segar tidak boleh diletakkan di suhu 20°C. 

### Skenario 7: Kadaluarsa Hari Ini (Besok Basi)
Waktu benar-benar sudah habis. Jika hari ini toko tutup tanpa terjual, maka besok terbuang.
- **Jenis Produk:** Susu & Olahannya (Dairy)
- **Kondisi Suhu Penyimpanan:** Chiller / Kulkas (4°C)
- **Sisa hari sebelum kadaluarsa:** 0
- **Harga modal:** 15.000
- **Harga jual:** 18.000
> **Ekspektasi Hasil:** **Berbahaya Kritis (>70%)**. Hukuman eksponensial karena sisa waktu tinggal 0 hari. Sistem akan meminta "Flash Sale" besar-besaran.

### Skenario 8: Harga Terlalu Mahal (Overpriced)
Barang awet tapi dijual dengan margin keuntungan selangit.
- **Jenis Produk:** Makanan Siap Saji (Ready to Eat)
- **Kondisi Suhu Penyimpanan:** Chiller / Kulkas (4°C)
- **Sisa hari sebelum kadaluarsa:** 10
- **Harga modal:** 10.000
- **Harga jual:** 35.000
> **Ekspektasi Hasil:** **Berbahaya/Waspada**. Mark-up harga mencapai 250%. Karena terlampau mahal, pembeli enggan melirik, menyebabkan barang tertahan lama di rak dan berisiko basi.

### Skenario 9: Seafood Kritis
Kategori yang paling berisiko tinggi membusuk di ambang waktu kadaluarsa.
- **Jenis Produk:** Makanan Laut (Seafood)
- **Kondisi Suhu Penyimpanan:** Freezer (-18°C)
- **Sisa hari sebelum kadaluarsa:** 1
- **Harga modal:** 50.000
- **Harga jual:** 60.000
> **Ekspektasi Hasil:** **Berbahaya**. 

### Skenario 10: Kombinasi Buruk
Sudah mau kadaluarsa, diletakkan di tempat panas, dan dijual terlalu mahal.
- **Jenis Produk:** Daging Olahan & Keju (Deli)
- **Kondisi Suhu Penyimpanan:** Panas (>28°C)
- **Sisa hari sebelum kadaluarsa:** 1
- **Harga modal:** 20.000
- **Harga jual:** 45.000
> **Ekspektasi Hasil:** **Sangat Berbahaya (Mendekati 99%)**. Semua faktor penalti *food waste* terpicu secara bersamaan.
