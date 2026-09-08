# PRD — Personal Bookkeeping

## 1. Informasi Produk
* **Nama Produk:** Personal Bookkeeping
* **Status:** Draft / MVP
* **Jenis:** Web Application (Responsive Desktop & Mobile)
* **Target Pengguna:** Penggunaan pribadi

---

## 2. Ringkasan & Tujuan
Personal Bookkeeping adalah aplikasi web untuk mencatat, memantau, dan mengelola arus kas pribadi berdasarkan tempat penyimpanan uang (*wallet/account*).

### Tujuan Utama
1. Memantau saldo real-time di setiap tempat penyimpanan.
2. Menampilkan total kekayaan kas (*net cash*) secara otomatis.
3. Mencatat arus Pemasukan, Pengeluaran, dan Transfer antar akun.
4. Memisahkan akun tabungan dengan akun operasional sehari-hari.
5. Menyajikan riwayat transaksi yang terstruktur.

---

## 3. Konsep Tempat Penyimpanan (*Storage/Wallet*)

Setiap tempat penyimpanan memiliki saldo independen dan sifat transaksi (*capabilities*) tertentu.

### Matrix Akses Transaksi (MVP)

| Tempat Penyimpanan | Kategori | Pemasukan | Pengeluaran | Transfer (Keluar/Masuk) |
| :--- | :--- | :---: | :---: | :---: |
| **Dompet** | Operasional (Cash) | Ya | Ya | Ya |
| **DANA** | Operasional (E-Wallet) | Ya | Ya | Ya |
| **Wondr BNI** | Operasional (Bank) | Ya | Ya | Ya |
| **SeaBank** | Tabungan (*Savings*) | Ya | **Tidak** | Ya |

> **Catatan Kunci:** SeaBank diset sebagai tempat tabungan. Untuk MVP, tidak diizinkan pengeluaran langsung dari SeaBank. Jika uang SeaBank ingin dipakai belanja, pengguna harus melakukan **Transfer** terlebih dahulu ke Wondr/DANA/Dompet.

---

## 4. Jenis Transaksi

Sistem hanya menggunakan **3 Jenis Transaksi Utama** untuk menjaga integritas saldo:

### 4.1 Pemasukan (*Income*)
Mencatat uang masuk dari luar sistem (Gaji, kiriman, *freelance*).
* **Efek Saldo:** Saldo tempat tujuan **(+)** | Total Uang **(+)**
* **Field Data:** Tanggal, Nominal, Tempat Tujuan, Keterangan.

### 4.2 Pengeluaran (*Expense*)
Mencatat uang keluar dari sistem untuk konsumsi/kebutuhan (Makan, tagihan, belanja).
* **Efek Saldo:** Saldo tempat sumber **(-)** | Total Uang **(-)**
* **Field Data:** Tanggal, Nominal, Tempat Sumber, Keterangan.

### 4.3 Transfer (*Internal Transfer*)
Mencatat perpindahan uang antar tempat penyimpanan milik sendiri (termasuk tarik tunai dari BNI ke Dompet, atau menabung ke SeaBank).
* **Efek Saldo:** Saldo tempat asal **(-)** | Saldo tempat tujuan **(+)** | Total Uang **(Tetap/Tidak Berubah)**
* **Field Data:** Tanggal, Nominal, Tempat Asal, Tempat Tujuan, Keterangan.

---

## 5. Perhitungan Saldo & Aturan Bisnis (*Business Rules*)

### Formula Saldo
Saldo Akhir = Saldo Awal + Total Pemasukan + Total Transfer Masuk - Total Pengeluaran - Total Transfer Keluar

### Aturan Bisnis
1. **Nominal > 0:** Transaksi hanya sah jika nominal lebih besar dari Rp0.
2. **Validasi Saldo Cukup:** Pengeluaran dan Transfer Keluar tidak boleh melebihi saldo berjalan pada tempat sumber (*no negative balance*).
3. **Transfer Asal != Tujuan:** Tempat asal dan tempat tujuan transfer tidak boleh sama.
4. **Proteksi Akun Tabungan:** Tempat dengan tipe *Tabungan* (seperti SeaBank) menolak form Pengeluaran Langsung.
5. **Imutabilitas Total pada Transfer:** Transaksi Transfer tidak boleh memicu perubahan pada indikator Total Uang Keseluruhan.
6. **Kalkulasi Ulang Otomatis:** Setiap penambahan, pengeditan, atau penghapusan transaksi harus memicu kalkulasi ulang saldo real-time.

---

## 6. Arsitektur Halaman & UI/UX

### 6.1 Dashboard (Halaman Utama)
* **Total Uang:** Card utama menampilkan akumulasi seluruh saldo tempat penyimpanan.
* **Daftar Tempat:** Grid/List tempat penyimpanan beserta saldonya masing-masing.
* **Quick Actions:** Tombol cepat `[+ Pemasukan]`, `[- Pengeluaran]`, `[⇄ Transfer]`.
* **Ringkasan Bulan Ini:** Total Pemasukan, Total Pengeluaran, dan Total Net Savings (Transfer ke Tabungan).

### 6.2 Detail Tempat Penyimpanan
Menampilkan riwayat khusus tempat tersebut dan tombol aksi yang relevan (misal: SeaBank hanya menampilkan tombol *+ Pemasukan* dan *⇄ Transfer*).

### 6.3 Halaman / Modal Manajemen Transaksi
* Form input sederhana sesuai jenis transaksi.
* Tabel/List Riwayat Transaksi lengkap dengan indikator warna (Hijau: Pemasukan, Merah: Pengeluaran, Biru: Transfer).
* Aksi: Edit & Hapus transaksi (dilengkapi konfirmasi).

### 6.4 Tambah Tempat Penyimpanan Baru
Form pembuatan tempat baru:
* Nama Tempat (Contoh: "BCA Utama")
* Saldo Awal (Default: 0)
* Izinkan Pengeluaran Langsung? (Toggle: Ya / Tidak)

---

## 7. Scope MVP vs Post-MVP

### Scope MVP (Wajib Ada)
* [x] Dashboard (Total Uang & Breakdown Saldo per Tempat).
* [x] Manajemen Tempat Penyimpanan Default (Dompet, DANA, Wondr BNI, SeaBank).
* [x] Tambah Tempat Penyimpanan Baru (beserta atribut Saldo Awal & Akses Pengeluaran).
* [x] Pencatatan 3 Transaksi: Pemasukan, Pengeluaran, Transfer.
* [x] Validasi Saldo & Aturan Bisnis.
* [x] Riwayat Transaksi (List, Edit, & Hapus Transaksi).
* [x] Perhitungan saldo otomatis & real-time.

### Scope Post-MVP
* [ ] Filter Transaksi (Berdasarkan Kategori, Rentang Tanggal, & Tempat).
* [ ] Kategori Pengeluaran (Makanan, Transportasi, Tagihan, dll.).
* [ ] Grafik Visualisasi Arus Kas (Chart.js).
* [ ] Authentication System (Login/Register).
* [ ] Target / Goal Tabungan SeaBank.
* [ ] Export Data ke CSV/Excel.
* [ ] Dark Mode support.

---

## 8. Rekomendasi Tech Stack MVP

* **Backend:** Python (Flask)
* **Database:** SQLite (Relational DB cocok untuk integritas data keuangan)
* **Frontend:** HTML5, CSS (Tailwind CSS via CDN), Vanilla JavaScript
* **Environment:** Localhost Execution

---

## 9. Rencana Pengerjaan Bertahap (Implementation Roadmap)

*Instruksi ke AI Agent: Kerjakan fitur secara berurutan dari Tahap 1 hingga Tahap 6. Pastikan setiap tahap diuji dan berjalan dengan baik sebelum lanjut ke tahap berikutnya.*

### 🛠️ Tahap 1: Inisialisasi Proyek & Database
- Buat struktur folder Flask (app.py, templates/, static/, models.py/database.py).
- Setup skema SQLite untuk 2 tabel utama:
  1. `wallets` (id, name, initial_balance, allow_expense).
  2. `transactions` (id, type, amount, date, source_wallet_id, destination_wallet_id, description).
- Buat skrip *seed data* untuk tempat penyimpanan default: Dompet, DANA, Wondr BNI, SeaBank (allow_expense=False).

### 🎨 Tahap 2: UI Dashboard Static & Wallet Management
- Buat template HTML/Tailwind sederhana untuk Dashboard.
- Tampilkan card "Total Uang" dan grid card untuk daftar tempat penyimpanan beserta saldonya.
- Buat fitur/form sederhana untuk **Menambah Tempat Penyimpanan Baru** (Nama, Saldo Awal, Toggle Boleh Pengeluaran).

### 💸 Tahap 3: Logika Pencatatan Transaksi Pemasukan & Pengeluaran
- Buat modal/form untuk **Pemasukan** (Pilih Wallet Tujuan, Nominal, Tanggal, Keterangan).
- Buat modal/form untuk **Pengeluaran** (Pilih Wallet Sumber, Nominal, Tanggal, Keterangan).
- Tambahkan **validasi backend/frontend**:
  - Wallet tipe tabungan (SeaBank) tidak boleh muncul di dropdown Pengeluaran.
  - Saldo wallet sumber tidak boleh kurang dari nominal pengeluaran.
- Hubungkan pencatatan ke database dan buat fungsi kalkulasi saldo otomatis.

### 🔄 Tahap 4: Logika Transaksi Transfer Antar Akun
- Buat modal/form untuk **Transfer** (Wallet Asal, Wallet Tujuan, Nominal, Tanggal, Keterangan).
- Tambahkan validasi: Wallet Asal dan Wallet Tujuan tidak boleh sama, serta saldo Wallet Asal harus mencukupi.
- Pastikan transaksi transfer memotong saldo Wallet Asal, menambah saldo Wallet Tujuan, namun **Total Uang tetap sama**.

### 📜 Tahap 5: Riwayat Transaksi & Fitur Edit/Hapus
- Buat tabel/list Riwayat Transaksi di Dashboard.
- Beri pembeda visual (warna/icon) untuk Pemasukan (Hijau), Pengeluaran (Merah), dan Transfer (Biru).
- Buat fitur **Hapus Transaksi** dan **Edit Transaksi**.
- Pastikan saat transaksi dihapus/diedit, saldo akun yang berdampak langsung terkalkulasi ulang secara akurat.

### 🔍 Tahap 6: Detail Halaman Tempat Penyimpanan & Polish UI
- Buat halaman khusus detail tiap tempat penyimpanan (menampilkan saldo & khusus transaksi akun tersebut).
- Sesuaikan tombol aksi di halaman detail (Sembunyikan tombol Pengeluaran jika tempat tersebut bertipe Tabungan).
- Recheck seluruh validasi dan perbaiki tampilan antarmuka agar responsif di mobile & desktop.