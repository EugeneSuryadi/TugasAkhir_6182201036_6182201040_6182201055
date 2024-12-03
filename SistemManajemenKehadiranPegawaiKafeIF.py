import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyodbc
from datetime import datetime, timedelta
from tkcalendar import Calendar
from tkinter import Canvas, Frame, Scrollbar


# Database connection string
connectionString = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=LAPTOP-CGSVR75B\\SQLEXPRESS;'
    'DATABASE=DatabaseManpro;'  # Ganti dengan nama database yang benar
    'Trusted_Connection=yes;'
    'TrustServerCertificate=yes;'
)

def setup_database():
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    
    # Create tables if they do not exist
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Kecamatan' AND xtype='U')
    CREATE TABLE Kecamatan(
        idKecamatan int IDENTITY(1,1) PRIMARY KEY,
        namaKecamatan varchar(100) NOT NULL
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Kelurahan' AND xtype='U')
    CREATE TABLE Kelurahan(
        idKelurahan int IDENTITY(1,1) PRIMARY KEY,
        namaKelurahan varchar(100) NOT NULL,
        idKecamatan int FOREIGN KEY REFERENCES Kecamatan(idKecamatan)
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pemilik' AND xtype='U')
    CREATE TABLE Pemilik(
        username varchar(50) NOT NULL PRIMARY KEY,
        email varchar(50) NOT NULL,
        password varchar(50) NOT NULL
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Jabatan' AND xtype='U')
    CREATE TABLE Jabatan(
        idJabatan int PRIMARY KEY,
        namaJabatan varchar(100) NOT NULL,
        satuanGaji int NOT NULL
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pegawai' AND xtype='U')
    CREATE TABLE Pegawai(
        idPegawai int IDENTITY(1,1) NOT NULL PRIMARY KEY,
        nama varchar(255) NOT NULL,
        NomorTelepon varchar(15) NOT NULL,
        email varchar(255) NOT NULL,
        Alamat varchar(100) NOT NULL,
        idKelurahan int NOT NULL FOREIGN KEY REFERENCES Kelurahan(idKelurahan),
        idJabatan int NOT NULL FOREIGN KEY REFERENCES Jabatan(idJabatan)
    )""")
    
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Absensi' AND xtype='U')
    CREATE TABLE Absensi (
        idAbsensi int IDENTITY(1,1) PRIMARY KEY,
        idPegawai int NOT NULL,
        waktuMasuk TIME,
        waktuKeluar TIME,
        tanggalAbsensi DATE DEFAULT CAST(GETDATE() AS DATE),
        Durasi TIME,
        WeeklyHours INT DEFAULT 0,
        FOREIGN KEY (idPegawai) REFERENCES Pegawai(idPegawai)
    )""")
    
    # Insert initial data into Pemilik table
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM Pemilik WHERE username='Owner')
    INSERT INTO Pemilik (username, email, password) VALUES
    ('Owner', 'Owner@mail.com', '12345')
    """)
    
    # Insert initial data into Jabatan table
    jabatan_data = [
        (1, 'Manajer', 200000),
        (2, 'Koki', 150000),
        (3, 'Bartender', 120000),
        (4, 'Pelayan', 100000),
        (5, 'Kasir', 100000)
    ]
    for jabatan in jabatan_data:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Jabatan WHERE idJabatan=?)
        INSERT INTO Jabatan (idJabatan, namaJabatan, satuanGaji) VALUES (?, ?, ?)
        """, (jabatan[0], jabatan[0], jabatan[1], jabatan[2]))
    
    # Insert initial data into Kecamatan table
    kecamatan_data = [
        'Andir', 'Astana Anyar', 'Antapani', 'Arcamanik', 'Babakan Ciparay',
        'Bandung Kidul', 'Bandung Kulon', 'Batununggal', 'Bojongloa Kaler', 'Bojongloa Kidul'
    ]
    for kecamatan in kecamatan_data:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Kecamatan WHERE namaKecamatan=?)
        INSERT INTO Kecamatan (namaKecamatan) VALUES (?)
        """, (kecamatan, kecamatan))
    
    # Insert initial data into Kelurahan table
    kelurahan_data = [
        ('Ciroyom', 1), ('Kebon Jeruk', 1), ('Maleber', 1), ('Dungus Cariang', 1), ('Campaka', 1),
        ('Karang Anyar', 2), ('Nyengseret', 2), ('Panjunan', 2), ('Cibadak', 2), ('Karasak', 2),
        ('Antapani Kidul', 3), ('Antapani Tengah', 3), ('Antapani Wetan', 3), ('Antapani Kulon', 3),
        ('Cisaranten Kulon', 4), ('Cisaranten Bina Harapan', 4), ('Cisaranten Endah', 4),
        ('Sukamiskin', 4), ('Sindang Jaya', 4), ('Babakan Ciparay', 5), ('Sukahaji', 5),
        ('Margahayu Utara', 5), ('Babakan', 5), ('Warung Muncang', 5), ('Mengger', 6),
        ('Wates', 6), ('Batununggal', 6), ('Kujangsari', 6), ('Kebon Gedang', 6),
        ('Cijerah', 7), ('Gempol Sari', 7), ('Caringin', 7), ('Warung Muncang', 7),
        ('Cigondewah Rahayu', 7), ('Kebon Gedang', 8), ('Kacapiring', 8), ('Binong', 8),
        ('Gumuruh', 8), ('Cibangkong', 8), ('Jamika', 9), ('Sukahaji', 9), ('Cibuntu', 9),
        ('Cibaduyut', 9), ('Kebon Lega', 9), ('Kebon Lega', 10), ('Mekarwangi', 10),
        ('Situsaeur', 10), ('Cibaduyut Kidul', 10), ('Cibaduyut', 10)
    ]
    for kelurahan in kelurahan_data:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM Kelurahan WHERE namaKelurahan=? AND idKecamatan=?)
        INSERT INTO Kelurahan (namaKelurahan, idKecamatan) VALUES (?, ?)
        """, (kelurahan[0], kelurahan[1], kelurahan[0], kelurahan[1]))
    
    conn.commit()
    conn.close()
    
# Fetch Kecamatan and Kelurahan data from the database
def fetch_kecamatan_kelurahan():
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    
    cursor.execute("SELECT idKecamatan, namaKecamatan FROM Kecamatan")
    kecamatan_data = cursor.fetchall()
    
    # Ubah query untuk mendapatkan semua data kelurahan
    cursor.execute("""
        SELECT k.idKelurahan, k.namaKelurahan, k.idKecamatan 
        FROM Kelurahan k
        ORDER BY k.idKecamatan, k.namaKelurahan
    """)
    kelurahan_data = cursor.fetchall()
    
    conn.close()
    
    kecamatan_dict = {row[1]: row[0] for row in kecamatan_data}  # {namaKecamatan: idKecamatan}
    
    # Buat dictionary kelurahan yang dikelompokkan berdasarkan idKecamatan
    kelurahan_by_kecamatan = {}
    for row in kelurahan_data:
        id_kelurahan, nama_kelurahan, id_kecamatan = row
        if id_kecamatan not in kelurahan_by_kecamatan:
            kelurahan_by_kecamatan[id_kecamatan] = []
        kelurahan_by_kecamatan[id_kecamatan].append((nama_kelurahan, id_kelurahan))
    
    return kecamatan_dict, kelurahan_by_kecamatan

def fetch_jabatan():
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    
    cursor.execute("SELECT idJabatan, namaJabatan FROM Jabatan")
    jabatan_data = cursor.fetchall()
    
    conn.close()
    
    jabatan_dict = {row[1]: row[0] for row in jabatan_data}  # {namaJabatan: idJabatan}
    
    return jabatan_dict

def fetch_weekly_hours_and_gaji(id_pegawai):
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    start_of_week = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
    end_of_week = (datetime.now() + timedelta(days=6 - datetime.now().weekday())).strftime('%Y-%m-%d')

    query = """
    SELECT 
        SUM(DATEDIFF(HOUR, waktuMasuk, waktuKeluar)) AS WeeklyHours,
        SUM(DATEDIFF(HOUR, waktuMasuk, waktuKeluar) * j.satuanGaji) AS WeeklyGaji
    FROM 
        Absensi a
    JOIN
        Pegawai p ON a.idPegawai = p.idPegawai
    JOIN
        Jabatan j ON p.idJabatan = j.idJabatan
    WHERE
        a.idPegawai = ? AND
        a.tanggalAbsensi BETWEEN ? AND ?
    """
    cursor.execute(query, (id_pegawai, start_of_week, end_of_week))
    result = cursor.fetchone()
    
    conn.close()
    
    weekly_hours = result.WeeklyHours if result.WeeklyHours else 0
    weekly_gaji = result.WeeklyGaji if result.WeeklyGaji else 0
    
    return weekly_hours, weekly_gaji

class ScrollableFrame(ttk.Frame):
    """
    A scrollable frame that can be used to contain other widgets.
    """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class AbsensiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Kehadiran Pegawai Kafe IF")
        self.geometry("600x500")  # Increased size for better scrollability
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label dan tombol di atas gambar latar belakang
        tk.Label(self, text="Sistem Manajemen", font=("Helvetica", 20), fg="White", bg="green").place(relx=0.5, rely=0.2, anchor="center")
        tk.Label(self, text="Kehadiran Pegawai Kafe Asep Cikidiw", font=("Helvetica", 20), fg="White", bg="green").place(relx=0.5, rely=0.3, anchor="center")

        # Tombol di tengah
        tk.Button(self, text="Pemilik", command=self.show_pemilik_login, background="black", fg="white", width=20).place(relx=0.5, rely=0.5, anchor="center")
        tk.Button(self, text="Pegawai", command=self.show_pegawai_login, background="black", fg="white", width=20).place(relx=0.5, rely=0.6, anchor="center")

        # Tambahkan tombol untuk keluar dari fullscreen
        tk.Button(self, text="Keluar", command=self.destroy, background="red", fg="white", width=10).place(relx=0.95, rely=0.05, anchor="ne")

    def show_pemilik_login(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label untuk judul di atas gambar latar belakang
        tk.Label(self, text="Login to Continue", font=("Helvetica", 18), fg="White", bg="green").place(relx=0.5, rely=0.1, anchor="center")

        # Label dan Entry untuk Username
        tk.Label(self, text="Username:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.25, anchor="center")
        username_entry = tk.Entry(self, width=30)
        username_entry.place(relx=0.5, rely=0.3, anchor="center")

        # Label dan Entry untuk Email
        tk.Label(self, text="Email:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.35, anchor="center")
        email_entry = tk.Entry(self, width=30)
        email_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Label dan Entry untuk Password
        tk.Label(self, text="Password:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.45, anchor="center")
        password_entry = tk.Entry(self, show='*', width=30)
        password_entry.place(relx=0.5, rely=0.5, anchor="center")

        # Fungsi untuk menangani login
        def submit_login():
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()

            try:
                conn = pyodbc.connect(connectionString)  # Ganti `connectionString` dengan string koneksi Anda
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM Pemilik WHERE username=? AND email=? AND password=?", (username, email, password))
                row = cursor.fetchone()
                if row:
                    self.show_pemilik_menu()
                else:
                    if not cursor.execute("SELECT * FROM Pemilik WHERE username=?", (username,)).fetchone():
                        messagebox.showerror("Error", "Incorrect username.")
                    elif not cursor.execute("SELECT * FROM Pemilik WHERE username=? AND email=?", (username, email)).fetchone():
                        messagebox.showerror("Error", "Incorrect email.")
                    else:
                        messagebox.showerror("Error", "Incorrect password.")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Tombol Login dan Back diatur di tengah
        tk.Button(self, text="Login", command=submit_login, width=15, height=1, background="blue", fg="white").place(relx=0.5, rely=0.6, anchor="center")
        tk.Button(self, text="Back", command=self.create_main_menu, width=10, height=1, background="red", fg="white").place(relx=0.5, rely=0.7, anchor="center")

        # Tombol untuk keluar dari fullscreen
        tk.Button(self, text="Keluar", command=self.destroy, width=10, height=1, background="red", fg="white").place(relx=0.95, rely=0.05, anchor="ne")

    def show_pemilik_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label di atas gambar latar belakang
        tk.Label(self, text="Hello, Owner!", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.1, anchor="center")
        tk.Label(self, text="Select to Continue", font=("Helvetica", 18), fg="white", bg="green").place(relx=0.5, rely=0.2, anchor="center")

        # Tombol Registrasi Pegawai Baru
        tk.Button(self, text="Registrasi Pegawai Baru", command=self.pegawai_baru, width=25, height=2, background="brown", fg="white").place(relx=0.5, rely=0.3, anchor="center")

        # Tombol Laporan Absensi
        tk.Button(self, text="Laporan Absensi", command=self.laporan_kehadiran, width=25, height=2, background="brown", fg="white").place(relx=0.5, rely=0.4, anchor="center")

        # Tombol Laporan Gaji
        tk.Button(self, text="Laporan Gaji", command=self.laporan_gaji, width=25, height=2, background="brown", fg="white").place(relx=0.5, rely=0.5, anchor="center")

        # Tombol Back
        tk.Button(self, text="Back", command=self.create_main_menu, width=20, height=1, background="red", fg="white").place(relx=0.5, rely=0.6, anchor="center")

        # Tombol untuk keluar dari fullscreen
        tk.Button(self, text="Keluar", command=self.destroy, width=10, height=1, background="red", fg="white").place(relx=0.95, rely=0.05, anchor="ne")


    def show_pegawai_login(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label di atas gambar latar belakang
        tk.Label(self, text="Login Pegawai", font=("Arial", 18), fg="white", bg="green").place(relx=0.5, rely=0.1, anchor="center")

        # Input untuk Nomor Telepon
        tk.Label(self, text="Nomor Telepon:", font=("Arial", 12), fg="white", bg="green").place(relx=0.5, rely=0.25, anchor="center")
        nomor_telepon_entry = tk.Entry(self, width=30)
        nomor_telepon_entry.place(relx=0.5, rely=0.3, anchor="center")

        # Fungsi untuk submit login
        def submit_login():
            nomor_telepon = nomor_telepon_entry.get()

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()

                cursor.execute("SELECT idPegawai FROM Pegawai WHERE NomorTelepon=?", (nomor_telepon,))
                row = cursor.fetchone()
                if row:
                    self.id_pegawai = row[0]
                    self.show_pegawai_menu()
                else:
                    messagebox.showerror("Error", "Nomor telepon tidak ditemukan.")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Tombol Login dan Back
        tk.Button(self, text="Login", command=submit_login, width=15, height=1, background="blue", fg="white").place(relx=0.5, rely=0.4, anchor="center")
        tk.Button(self, text="Back", command=self.create_main_menu, width=15, height=1, background="red", fg="white").place(relx=0.5, rely=0.5, anchor="center")

        # Tombol untuk keluar dari fullscreen
        tk.Button(self, text="Keluar", command=self.destroy, width=10, height=1, background="red", fg="white").place(relx=0.95, rely=0.05, anchor="ne")


    def show_pegawai_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label di atas gambar latar belakang
        tk.Label(self, text="Select to Continue", font=("Arial", 18), fg="white", bg="green").place(relx=0.5, rely=0.1, anchor="center")

        # Tombol Absensi
        tk.Button(self, text="Absensi", command=self.absensi, width=15, height=2, background="brown", fg="white").place(relx=0.5, rely=0.2, anchor="center")

        # Tombol Gaji
        tk.Button(self, text="Gaji", command=self.gaji, width=15, height=2, background="brown", fg="white").place(relx=0.5, rely=0.3, anchor="center")

        # Tombol Back
        tk.Button(self, text="Back", command=self.create_main_menu, width=10, height=1, background="red", fg="white").place(relx=0.5, rely=0.4, anchor="center")

        # Tombol untuk keluar dari fullscreen
        tk.Button(self, text="Keluar", command=self.destroy, width=10, height=1, background="red", fg="white").place(relx=0.95, rely=0.05, anchor="ne")

    def pegawai_baru(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label di atas gambar latar belakang
        tk.Label(self, text="Registrasi Pegawai Baru", font=("Helvetica", 18), fg="white", bg="green").place(relx=0.5, rely=0.05, anchor="center")

        # Input fields di tengah
        tk.Label(self, text="Nama:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.15, anchor="center")
        nama_entry = tk.Entry(self, width=40)
        nama_entry.place(relx=0.5, rely=0.2, anchor="center")

        tk.Label(self, text="Nomor Telepon:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.25, anchor="center")
        nomor_telepon_entry = tk.Entry(self, width=40)
        nomor_telepon_entry.place(relx=0.5, rely=0.3, anchor="center")

        tk.Label(self, text="Email:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.35, anchor="center")
        email_entry = tk.Entry(self, width=40)
        email_entry.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(self, text="Alamat:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.45, anchor="center")
        alamat_entry = tk.Entry(self, width=40)
        alamat_entry.place(relx=0.5, rely=0.5, anchor="center")

        # Kecamatan Dropdown
        tk.Label(self, text="Kecamatan:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.55, anchor="center")
        kecamatan_var = tk.StringVar()
        kecamatan_dropdown = ttk.Combobox(self, textvariable=kecamatan_var, values=list(kecamatan_dict.keys()), width=37)
        kecamatan_dropdown.place(relx=0.5, rely=0.6, anchor="center")

        # Kelurahan Dropdown
        tk.Label(self, text="Kelurahan:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.65, anchor="center")
        kelurahan_var = tk.StringVar()
        kelurahan_dropdown = ttk.Combobox(self, textvariable=kelurahan_var, values=[], width=37)
        kelurahan_dropdown.place(relx=0.5, rely=0.7, anchor="center")

        # Update kelurahan based on kecamatan selection
        def update_kelurahan(*args):
            selected_kecamatan = kecamatan_var.get()
            selected_kecamatan_id = kecamatan_dict.get(selected_kecamatan)
            
            if selected_kecamatan_id:
                # Dapatkan daftar kelurahan untuk kecamatan yang dipilih
                kelurahan_list = [k[0] for k in kelurahan_by_kecamatan.get(selected_kecamatan_id, [])]
                kelurahan_dropdown['values'] = kelurahan_list
                kelurahan_var.set('')  # Reset pilihan kelurahan

        # Bind kecamatan_var dengan fungsi update_kelurahan
        kecamatan_var.trace('w', update_kelurahan)

        # Jabatan Dropdown
        tk.Label(self, text="Nama Jabatan:", font=("Helvetica", 12), fg="white", bg="green").place(relx=0.5, rely=0.75, anchor="center")
        jabatan_var = tk.StringVar()
        jabatan_dropdown = ttk.Combobox(self, textvariable=jabatan_var, values=list(jabatan_dict.keys()), width=37)
        jabatan_dropdown.place(relx=0.5, rely=0.8, anchor="center")

        # Tombol Submit dan Back
        def submit_pegawai():
            nama = nama_entry.get().strip()
            nomor_telepon = nomor_telepon_entry.get().strip()
            email = email_entry.get().strip()
            alamat = alamat_entry.get().strip()
            kecamatan = kecamatan_var.get().strip()
            kelurahan = kelurahan_var.get().strip()
            nama_jabatan = jabatan_var.get().strip()

            if not all([nama, nomor_telepon, email, alamat, kecamatan, kelurahan, nama_jabatan]):
                messagebox.showerror("Error", "Semua field harus diisi.")
                return

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM Pegawai WHERE NomorTelepon = ?", (nomor_telepon,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "Nomor Telepon sudah terdaftar.")
                    return

                selected_kelurahan_id = kelurahan_dict.get(kelurahan)
                if not selected_kelurahan_id:
                    messagebox.showerror("Error", "Kelurahan tidak valid.")
                    return

                id_jabatan = jabatan_dict.get(nama_jabatan)
                if not id_jabatan:
                    messagebox.showerror("Error", "Jabatan tidak valid.")
                    return

                SQL_QUERY_Pegawai = """
                    INSERT INTO Pegawai (
                        nama,
                        NomorTelepon,
                        email,
                        Alamat,
                        idKelurahan,
                        idJabatan
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(SQL_QUERY_Pegawai, (nama, nomor_telepon, email, alamat, selected_kelurahan_id, id_jabatan))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Pegawai baru berhasil ditambahkan.")
                self.show_pemilik_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self, text="Submit", command=submit_pegawai, width=15, height=2, background="blue", fg="white").place(relx=0.5, rely=0.85, anchor="center")
        tk.Button(self, text="Back", command=self.show_pemilik_menu, width=10, height=1, background="red", fg="white").place(relx=0.5, rely=0.9, anchor="center")

        # Tombol untuk keluar dari fullscreen
        tk.Button(self, text="Keluar", command=self.destroy, width=10, height=1, background="red", fg="white").place(relx=0.95, rely=0.05, anchor="ne")

    def absensi(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label di atas gambar latar belakang
        tk.Label(self, text="Absensi", font=("Arial", 18), fg="white", bg="green").place(relx=0.5, rely=0.05, anchor="center")

        # Label dan dropdown di tengah
        tk.Label(self, text="Apakah ini waktu masuk atau keluar? (masuk/keluar):", font=("Arial", 12), fg="white", bg="green").place(relx=0.5, rely=0.15, anchor="center")
        action_var = tk.StringVar()
        action_dropdown = ttk.Combobox(self, textvariable=action_var, values=["masuk", "keluar"], width=20)
        action_dropdown.place(relx=0.5, rely=0.2, anchor="center")

        # Label dan entry nomor telepon di tengah
        tk.Label(self, text="Masukkan nomor telepon untuk check-in/check-out:", font=("Arial", 12), fg="white", bg="green").place(relx=0.5, rely=0.25, anchor="center")
        nomor_telepon_entry = tk.Entry(self, width=30)
        nomor_telepon_entry.place(relx=0.5, rely=0.3, anchor="center")

        def submit_absensi():
            action = action_var.get().strip().lower()
            nomor_telepon = nomor_telepon_entry.get().strip()

            if action not in ["masuk", "keluar"]:
                messagebox.showerror("Error", "Tindakan tidak valid. Masukkan 'masuk' atau 'keluar'.")
                return

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()

                cursor.execute("SELECT idPegawai FROM Pegawai WHERE NomorTelepon = ?", (nomor_telepon,))
                row = cursor.fetchone()
                if row:
                    id_pegawai = row[0]
                else:
                    raise ValueError("Pegawai dengan nomor telepon tersebut tidak ditemukan.")

                current_time = datetime.now().strftime('%H:%M:%S')
                current_date = datetime.now().strftime('%Y-%m-%d')

                if action == "masuk":
                    SQL_QUERY_Absensi = """
                        INSERT INTO Absensi (
                            idPegawai,
                            waktuMasuk,
                            tanggalAbsensi
                        )
                        VALUES (?, ?, ?)
                    """
                    cursor.execute(SQL_QUERY_Absensi, (id_pegawai, current_time, current_date))
                elif action == "keluar":
                    cursor.execute("""
                        SELECT waktuMasuk
                        FROM Absensi
                        WHERE idPegawai = ? AND tanggalAbsensi = ? AND waktuKeluar IS NULL
                    """, (id_pegawai, current_date))
                    row = cursor.fetchone()

                    if row:
                        waktu_masuk = row[0]
                        waktu_keluar = datetime.strptime(current_time, '%H:%M:%S')
                        waktu_masuk = datetime.strptime(waktu_masuk.strftime('%H:%M:%S'), '%H:%M:%S')

                        durasi = waktu_keluar - waktu_masuk
                        durasi_str = str(durasi)
                        weekly_hours = int(durasi.total_seconds() // 3600)

                        SQL_QUERY_Absensi = """
                            UPDATE Absensi
                            SET waktuKeluar = ?, Durasi = ?, WeeklyHours = WeeklyHours + ?
                            WHERE idPegawai = ? AND tanggalAbsensi = ? AND waktuKeluar IS NULL
                        """
                        cursor.execute(SQL_QUERY_Absensi, (current_time, durasi_str, weekly_hours, id_pegawai, current_date))
                    else:
                        raise ValueError("Tidak ditemukan waktu masuk untuk pegawai ini hari ini.")

                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Absensi berhasil diperbarui.")
                self.show_pegawai_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Tombol Submit dan Back di tengah
        tk.Button(self, text="Submit", command=submit_absensi, width=15, height=2, background="black", fg="white").place(relx=0.5, rely=0.35, anchor="center")
        tk.Button(self, text="Back", command=self.show_pegawai_menu, width=10, height=1, background="red", fg="white").place(relx=0.5, rely=0.4, anchor="center")

        # Tombol untuk keluar dari fullscreen
        tk.Button(self, text="Keluar", command=self.destroy, width=10, height=1, background="red", fg="white").place(relx=0.95, rely=0.05, anchor="ne")


    def gaji(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label di atas gambar latar belakang
        tk.Label(self, text="Gaji Mingguan", font=("Arial", 18), fg="white", bg="brown").place(relx=0.5, rely=0.05, anchor="center")

        try:
            weekly_hours, weekly_gaji = fetch_weekly_hours_and_gaji(self.id_pegawai)
            tk.Label(self, text=f"Total Jam Kerja: {weekly_hours} jam", font=("Arial", 12), fg="white", bg="green").place(relx=0.5, rely=0.2, anchor="center")
            tk.Label(self, text=f"Total Gaji: Rp {weekly_gaji}", font=("Arial", 12), fg="white", bg="green").place(relx=0.5, rely=0.3, anchor="center")
        except Exception as e:
            messagebox.showerror("Error", str(e))

        # Tombol Details dan Back di tengah
        tk.Button(self, text="Details", command=self.gaji_details, width=20, height=2, background="black", fg="white").place(relx=0.5, rely=0.4, anchor="center")
        tk.Button(self, text="Back", command=self.show_pegawai_menu, width=10, height=1, background="red", fg="white").place(relx=0.5, rely=0.5, anchor="center")

        # Tombol untuk keluar dari fullscreen
        tk.Button(self, text="Keluar", command=self.destroy, width=10, height=1, background="red", fg="white").place(relx=0.95, rely=0.05, anchor="ne")


    def gaji_details(self):
        # Create a new window for details
        details_window = tk.Toplevel(self)
        details_window.title("Detail Gaji")
        details_window.geometry("800x600")

        # Create a scrollable frame in the new window
        scroll_frame = ScrollableFrame(details_window)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        frame = scroll_frame.scrollable_frame

        tk.Label(frame, text="Detail Gaji Mingguan", font=("Arial", 16)).pack(pady=(20, 10))

        # Fetch detailed salary data
        try:
            conn = pyodbc.connect(connectionString)
            cursor = conn.cursor()

            # Define the current week range
            start_of_week = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
            end_of_week = (datetime.now() + timedelta(days=6 - datetime.now().weekday())).strftime('%Y-%m-%d')

            query = """
            SELECT 
                DATENAME(WEEKDAY, a.tanggalAbsensi) AS Hari,
                a.tanggalAbsensi AS Tanggal,
                a.waktuMasuk AS Masuk,
                a.waktuKeluar AS Keluar,
                j.namaJabatan AS Jabatan,
                CASE 
                    WHEN a.waktuKeluar IS NOT NULL THEN DATEDIFF(HOUR, a.waktuMasuk, a.waktuKeluar) * j.satuanGaji
                    ELSE 0
                END AS TotalGaji
            FROM 
                Absensi a
            JOIN 
                Pegawai p ON a.idPegawai = p.idPegawai
            JOIN 
                Jabatan j ON p.idJabatan = j.idJabatan
            WHERE 
                a.idPegawai = ? AND 
                a.tanggalAbsensi BETWEEN ? AND ?
            ORDER BY 
                a.tanggalAbsensi
            """
            cursor.execute(query, (self.id_pegawai, start_of_week, end_of_week))
            results = cursor.fetchall()
            columns = [column[0] for column in cursor.description]

            if not results:
                tk.Label(frame, text="Tidak ada data gaji untuk minggu ini.", font=("Arial", 12)).pack(pady=10)
                return

            # Create Treeview
            tree = ttk.Treeview(frame, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, minwidth=0, width=100, anchor='center')
            tree.pack(fill=tk.BOTH, expand=True, pady=10)

            # Insert data into Treeview
            for row in results:
                # Format date and time
                hari = row.Hari
                tanggal = row.Tanggal.strftime('%Y-%m-%d')
                masuk = row.Masuk.strftime('%H:%M:%S') if row.Masuk else 'N/A'
                keluar = row.Keluar.strftime('%H:%M:%S') if row.Keluar else 'N/A'
                jabatan = row.Jabatan
                total_gaji = f"Rp {row.TotalGaji}" if row.TotalGaji else 'Rp 0'
                tree.insert('', tk.END, values=(hari, tanggal, masuk, keluar, jabatan, total_gaji))

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def laporan_gaji(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label di atas gambar latar belakang
        tk.Label(self, text="Laporan Gaji", font=("Arial", 18), fg="white", bg="green").place(relx=0.5, rely=0.05, anchor="center")

        # Input Nama Pegawai
        tk.Label(self, text="Nama Pegawai (Opsional):", font=("Arial", 12), fg="white", bg="green").place(relx=0.5, rely=0.12, anchor="center")
        name_entry = tk.Entry(self, width=40)
        name_entry.place(relx=0.5, rely=0.18, anchor="center")

        # Pilih Tanggal Mulai
        tk.Label(self, text="Pilih tanggal mulai:", font=("Arial", 10), fg="white", bg="green").place(relx=0.5, rely=0.25, anchor="center")
        start_date_button = tk.Button(self, text="Pilih Tanggal Mulai", fg="gray", command=lambda: show_start_calendar())
        start_date_button.place(relx=0.5, rely=0.3, anchor="center")
        start_date_calendar = Calendar(self, date_pattern="yyyy-mm-dd")

        # Pilih Tanggal Akhir
        tk.Label(self, text="Pilih tanggal akhir:", font=("Arial", 10), fg="white", bg="green").place(relx=0.5, rely=0.35, anchor="center")
        end_date_button = tk.Button(self, text="Pilih Tanggal Akhir", fg="gray", command=lambda: show_end_calendar())
        end_date_button.place(relx=0.5, rely=0.4, anchor="center")
        end_date_calendar = Calendar(self, date_pattern="yyyy-mm-dd")

        # Fungsi untuk menampilkan kalender dan menambahkan event pada pemilihan tanggal
        def show_start_calendar():
            start_date_calendar.place(relx=0.65, rely=0.4, anchor="center")
            start_date_calendar.bind("<<CalendarSelected>>", set_start_date)  # Event binding

        def show_end_calendar():
            end_date_calendar.place(relx=0.65, rely=0.5, anchor="center")
            end_date_calendar.bind("<<CalendarSelected>>", set_end_date)  # Event binding

        # Fungsi untuk menyimpan tanggal yang dipilih
        def set_start_date(event):
            start_date = start_date_calendar.get_date()  # Mendapatkan tanggal yang dipilih
            start_date_button.config(text=f"Mulai: {start_date}")  # Menampilkan tanggal pada tombol
            start_date_calendar.place_forget()  # Menyembunyikan kalender setelah memilih tanggal
            start_date_calendar.unbind("<<CalendarSelected>>")  # Unbind event agar tidak memicu lagi

        def set_end_date(event):
            end_date = end_date_calendar.get_date()  # Mendapatkan tanggal yang dipilih
            end_date_button.config(text=f"Akhir: {end_date}")  # Menampilkan tanggal pada tombol
            end_date_calendar.place_forget()  # Menyembunyikan kalender setelah memilih tanggal
            end_date_calendar.unbind("<<CalendarSelected>>")  # Unbind event agar tidak memicu lagi

        def submit_laporan_gaji():
            start_date = start_date_button.cget("text").replace("Mulai: ", "")
            end_date = end_date_button.cget("text").replace("Akhir: ", "")
            name = name_entry.get().strip()

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()

                query = """
                SELECT 
                    p.nama AS Nama_Pegawai,
                    j.namaJabatan AS Nama_Jabatan,
                    j.satuanGaji AS SatuanGaji,
                    SUM(DATEDIFF(HOUR, a.waktuMasuk, a.waktuKeluar)) AS TotalJamKerja,
                    SUM(DATEDIFF(HOUR, a.waktuMasuk, a.waktuKeluar) * j.satuanGaji) AS Laporan_Gaji
                FROM 
                    Pegawai p
                JOIN 
                    Absensi a ON p.idPegawai = a.idPegawai
                JOIN 
                    Jabatan j ON p.idJabatan = j.idJabatan
                WHERE
                    a.tanggalAbsensi BETWEEN ? AND ?
                """
                params = [start_date, end_date]
                if name:
                    query += " AND p.nama LIKE ?"
                    params.append(f"%{name}%")
                query += " GROUP BY p.nama, j.namaJabatan, j.satuanGaji"

                cursor.execute(query, params)
                columns = [column[0] for column in cursor.description]
                results = cursor.fetchall()

                # Clear previous Treeview if exists
                for widget in self.winfo_children():
                    if isinstance(widget, ttk.Treeview):
                        widget.destroy()

                if not results:
                    tk.Label(self, text="Tidak ada data gaji untuk kriteria tersebut.", font=("Arial", 12), fg="white", bg="brown").pack(pady=10)
                    return

                result_window = tk.Toplevel(self)
                result_window.title("Laporan Gaji")
                result_window.geometry("800x600")

                scroll_result = ScrollableFrame(result_window)
                scroll_result.pack(fill=tk.BOTH, expand=True)

                result_frame = scroll_result.scrollable_frame

                tk.Label(result_frame, text="Laporan Gaji", font=("Arial", 16), fg="white", bg="brown").pack(pady=(10, 10))

                tree = ttk.Treeview(result_frame, columns=columns, show='headings')
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, minwidth=0, width=120, anchor='center')
                tree.pack(fill=tk.BOTH, expand=True, pady=10)

                for row in results:
                    tree.insert('', tk.END, values=row)

                conn.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Tombol Submit
        tk.Button(self, text="Submit", command=submit_laporan_gaji, width=15, height=2, background="blue", fg="white").place(relx=0.5, rely=0.55, anchor="center")
        
        # Tombol Back
        tk.Button(self, text="Back", command=self.show_pemilik_menu, width=10, height=1, background="red", fg="white").place(relx=0.5, rely=0.65, anchor="center")

    def laporan_kehadiran(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Menentukan jendela menjadi full screen
        self.attributes('-fullscreen', True)

        # Membuka gambar latar belakang
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        bg_image = Image.open("t.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Sesuaikan dengan ukuran layar
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Membuat Label dengan gambar sebagai latar belakang
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo  # Simpan referensi agar gambar tidak dihapus oleh garbage collector
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Menambahkan Label di tengah
        tk.Label(self, text="Laporan Absensi", font=("Arial", 18), fg="white", bg="green").place(relx=0.5, y=40, anchor="center")

        # Input Nama Pegawai
        tk.Label(self, text="Nama Pegawai (Opsional):", font=("Arial", 12), fg="white", bg="green").place(relx=0.5, y=90, anchor="center")
        name_entry = tk.Entry(self, width=40)
        name_entry.place(relx=0.5, y=120, anchor="center")

        # Pilih Tanggal Mulai
        tk.Label(self, text="Pilih tanggal mulai:", font=("Arial", 10), fg="white", bg="green").place(relx=0.5, y=180, anchor="center")
        start_date_button = tk.Button(self, text="Pilih Tanggal Mulai", fg="gray", command=lambda: show_start_calendar())
        start_date_button.place(relx=0.5, y=210, anchor="center")
        start_date_calendar = Calendar(self, date_pattern="yyyy-mm-dd")

        # Pilih Tanggal Akhir
        tk.Label(self, text="Pilih tanggal akhir:", font=("Arial", 10), fg="white", bg="green").place(relx=0.5, y=260, anchor="center")
        end_date_button = tk.Button(self, text="Pilih Tanggal Akhir", fg="gray", command=lambda: show_end_calendar())
        end_date_button.place(relx=0.5, y=290, anchor="center")
        end_date_calendar = Calendar(self, date_pattern="yyyy-mm-dd")

        # Fungsi untuk menampilkan kalender dan menambahkan event pada pemilihan tanggal
        def show_start_calendar():
            start_date_calendar.place(relx=0.65,rely=0.4, anchor="center")
            start_date_calendar.bind("<<CalendarSelected>>", set_start_date)  # Event binding

        def show_end_calendar():
            end_date_calendar.place(relx=0.65, rely=0.4, anchor="center")
            end_date_calendar.bind("<<CalendarSelected>>", set_end_date)  # Event binding

        # Fungsi untuk menyimpan tanggal yang dipilih
        def set_start_date(event):
            start_date = start_date_calendar.get_date()  # Mendapatkan tanggal yang dipilih
            start_date_button.config(text=f"Mulai: {start_date}")  # Menampilkan tanggal pada tombol
            start_date_calendar.place_forget()  # Menyembunyikan kalender setelah memilih tanggal
            start_date_calendar.unbind("<<CalendarSelected>>")  # Unbind event agar tidak memicu lagi

        def set_end_date(event):
            end_date = end_date_calendar.get_date()  # Mendapatkan tanggal yang dipilih
            end_date_button.config(text=f"Akhir: {end_date}")  # Menampilkan tanggal pada tombol
            end_date_calendar.place_forget()  # Menyembunyikan kalender setelah memilih tanggal
            end_date_calendar.unbind("<<CalendarSelected>>")  # Unbind event agar tidak memicu lagi

        # Fungsi submit untuk laporan kehadiran
        def submit_laporan_kehadiran():
            start_date = start_date_button.cget("text").replace("Mulai: ", "")
            end_date = end_date_button.cget("text").replace("Akhir: ", "")
            name = name_entry.get().strip()

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()

                query = """
                SELECT 
                    p.nama AS Nama_Pegawai,
                    DATENAME(WEEKDAY, a.tanggalAbsensi) AS Hari,
                    a.tanggalAbsensi AS Tanggal,
                    a.waktuMasuk AS Masuk,
                    a.waktuKeluar AS Keluar,
                    j.namaJabatan AS Jabatan,
                    CASE 
                        WHEN a.waktuKeluar IS NOT NULL THEN DATEDIFF(HOUR, a.waktuMasuk, a.waktuKeluar)
                        ELSE 0
                    END AS TotalJamKerja
                FROM 
                    Pegawai p
                JOIN 
                    Absensi a ON p.idPegawai = a.idPegawai
                JOIN 
                    Jabatan j ON p.idJabatan = j.idJabatan
                WHERE
                    a.tanggalAbsensi BETWEEN ? AND ?
                """
                params = [start_date, end_date]
                if name:
                    query += " AND p.nama LIKE ?"
                    params.append(f"%{name}%")
                query += " ORDER BY p.nama, a.tanggalAbsensi"

                cursor.execute(query, params)
                columns = [column[0] for column in cursor.description]
                results = cursor.fetchall()

                # Clear previous Treeview if exists
                for widget in self.winfo_children():
                    if isinstance(widget, ttk.Treeview):
                        widget.destroy()

                if not results:
                    tk.Label(self, text="Tidak ada data absensi untuk kriteria tersebut.", font=("Arial", 12), fg="white", bg="brown").place(relx=0.5, y=350, anchor="center")
                    return

                result_window = tk.Toplevel(self)
                result_window.title("Laporan Absensi")
                result_window.geometry("900x600")

                scroll_result = ScrollableFrame(result_window)
                scroll_result.pack(fill=tk.BOTH, expand=True)

                result_frame = scroll_result.scrollable_frame

                tk.Label(result_frame, text="Laporan Absensi", font=("Arial", 16), fg="white").pack(pady=(10, 10))

                tree = ttk.Treeview(result_frame, columns=columns, show='headings')
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, minwidth=0, width=120, anchor='center')
                tree.pack(fill=tk.BOTH, expand=True, pady=10)

                for row in results:
                    hari = row.Hari
                    tanggal = row.Tanggal.strftime('%Y-%m-%d')
                    masuk = row.Masuk.strftime('%H:%M:%S') if row.Masuk else 'N/A'
                    keluar = row.Keluar.strftime('%H:%M:%S') if row.Keluar else 'N/A'
                    jabatan = row.Jabatan
                    total_jam = row.TotalJamKerja
                    tree.insert('', tk.END, values=(row.Nama_Pegawai, hari, tanggal, masuk, keluar, jabatan, total_jam))

                conn.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Tombol Submit
        tk.Button(self, text="Submit", command=submit_laporan_kehadiran, width=15, height=2, background="blue", fg="white").place(relx=0.5, y=370, anchor="center")

        # Tombol Back
        tk.Button(self, text="Back", command=self.show_pemilik_menu, width=10, height=1, background="red", fg="white").place(relx=0.5, y=450, anchor="center")

if __name__ == "__main__":
    setup_database()
    kecamatan_dict, kelurahan_by_kecamatan = fetch_kecamatan_kelurahan()  # Updated variable name
    jabatan_dict = fetch_jabatan()
    app = AbsensiApp()
    app.mainloop()