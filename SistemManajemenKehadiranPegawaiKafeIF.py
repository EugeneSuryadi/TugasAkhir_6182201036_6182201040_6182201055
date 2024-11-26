def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Kehadiran Pegawai Kafe IF")
        self.geometry("400x300")
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("400x200")
        tk.Label(self, text="Sistem Manajemen", font=("Arial", 14)).pack(pady=(20, 0))
        tk.Label(self, text="Kehadiran Pegawai Kafe Asep Cikidiw", font=("Arial", 14)).pack(pady=(0, 20))

        
        tk.Button(self, text="Pemilik", command=self.show_pemilik_login, width=20).pack(pady=10)
        #tk.Button(self, text="Pegawai", command=self.show_pegawai_login, width=20).pack(pady=10)

        #tk.Label(self, text="Eugene Suryadi - 6182201036", font=("Arial", 8)).pack(pady=4)
        #tk.Label(self, text="Timothy Jason Tchandra - 6182201040", font=("Arial", 8)).pack(pady=3)
        #tk.Label(self, text="Albert Christian Lifen - 6182201055", font=("Arial", 8)).pack(pady=1)
        
    def show_pemilik_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("300x275")

        tk.Label(self, text="Login to Continue", font=("Arial", 14)).pack(pady=(20, 0))

        tk.Label(self, text="Username:").pack()
        username_entry = tk.Entry(self)
        username_entry.pack()

        tk.Label(self, text="Email:").pack()
        email_entry = tk.Entry(self)
        email_entry.pack()

        tk.Label(self, text="Password:").pack()
        password_entry = tk.Entry(self, show='*')
        password_entry.pack()

        def submit_login():
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()

            try:
                conn = pyodbc.connect(connectionString)
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
        tk.Button(self, text="Login", command=submit_login).pack(pady=10)
        tk.Button(self, text="Back", command=self.create_main_menu).pack(pady=10)

    def show_pemilik_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("300x250")

        tk.Label(self, text="Select to Continue", font=("Arial", 14)).pack(pady=(20, 0))
        tk.Button(self, text="Registrasi Pegawai Baru", command=self.pegawai_baru, width=20).pack(pady=10)
        tk.Button(self, text="Laporan Absensi", command=self.laporan_kehadiran, width=20).pack(pady=10)
        tk.Button(self, text="Laporan Gaji", command=self.laporan_gaji, width=20).pack(pady=10)
        tk.Button(self, text="Back", command=self.create_main_menu, width=20).pack(pady=10)
    def pegawai_baru(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("500x550")  # Adjust window size for better visibility

        tk.Label(self, text="Registrasi Pegawai Baru", font=("Arial", 14)).pack(pady=(20, 0))
        tk.Label(self, text="Nama:").pack(pady=(10))
        nama_entry = tk.Entry(self)
        nama_entry.pack()

        tk.Label(self, text="Nomor Telepon:").pack(pady=(10))
        nomor_telepon_entry = tk.Entry(self)
        nomor_telepon_entry.pack()

        tk.Label(self, text="Email:").pack(pady=(10))
        email_entry = tk.Entry(self)
        email_entry.pack()

        tk.Label(self, text="Alamat:").pack(pady=(10))
        alamat_entry = tk.Entry(self)
        alamat_entry.pack()

        tk.Label(self, text="Kecamatan:").pack(pady=(10))
        kecamatan_var = tk.StringVar()
        kecamatan_dropdown = ttk.Combobox(self, textvariable=kecamatan_var, values=list(kecamatan_dict.values()))
        kecamatan_dropdown.pack()

        tk.Label(self, text="Kelurahan:").pack(pady=(10))
        kelurahan_var = tk.StringVar()
        kelurahan_dropdown = ttk.Combobox(self, textvariable=kelurahan_var)
        kelurahan_dropdown.pack()

        def update_kelurahan(*args):
            selected_kecamatan = kecamatan_var.get()
            selected_kecamatan_id = [k for k, v in kecamatan_dict.items() if v == selected_kecamatan][0]
            kelurahan_list = [v[0] for k, v in kelurahan_dict.items() if v[1] == selected_kecamatan_id]
            kelurahan_dropdown['values'] = kelurahan_list
        
        kecamatan_var.trace('w', update_kelurahan)

        tk.Label(self, text="Nama Jabatan:").pack()
        jabatan_var = tk.StringVar()
        jabatan_dropdown = ttk.Combobox(self, textvariable=jabatan_var, values=list(jabatan_dict.values()))
        jabatan_dropdown.pack()

        def submit_pegawai():
            nama = nama_entry.get()
            nomor_telepon = nomor_telepon_entry.get()
            email = email_entry.get()
            alamat = alamat_entry.get()
            kecamatan = kecamatan_var.get()
            kelurahan = kelurahan_var.get()
            nama_jabatan = jabatan_var.get()
            
            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM Pegawai WHERE NomorTelepon = ?", (nomor_telepon,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "Nomor Telepon sudah terdaftar.")
                    return

                selected_kelurahan_id = [k for k, v in kelurahan_dict.items() if v[0] == kelurahan][0]
                id_jabatan = [k for k, v in jabatan_dict.items() if v == nama_jabatan][0]
                
                SQL_QUERY_Pegawai = """
                    INSERT INTO pegawai (
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
        
        tk.Button(self, text="Submit", command=submit_pegawai).pack(pady=10)
        tk.Button(self, text="Back", command=self.show_pemilik_menu).pack(pady=10)
        
    def laporan_kehadiran(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("300x275")

        tk.Label(self, text="Laporan Absensi", font=("Arial", 14)).pack(pady=(20, 0))   

        tk.Label(self, text="Masukkan tanggal mulai (YYYY-MM-DD):").pack(pady=(10))
        start_date_entry = tk.Entry(self)
        start_date_entry.pack()

        tk.Label(self, text="Masukkan tanggal akhir (YYYY-MM-DD):").pack(pady=(10))
        end_date_entry = tk.Entry(self)
        end_date_entry.pack()

        def submit_laporan_kehadiran():
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()

            try:
                conn = pyodbc.connect(connectionString)
                cursor = conn.cursor()
                
                query = """
                SELECT 
                    p.nama AS Nama_Pegawai,
                    CONVERT(VARCHAR, a.tanggalAbsensi, 23) AS Tanggal,
                    CONVERT(VARCHAR, a.waktuMasuk, 8) AS Waktu_Masuk,
                    CONVERT(VARCHAR, a.waktuKeluar, 8) AS Waktu_Keluar,
                    DATEDIFF(HOUR, a.waktuMasuk, a.waktuKeluar) AS TotalJamKerja
                FROM 
                    pegawai p
                JOIN 
                    Absensi a ON p.idPegawai = a.idPegawai
                WHERE
                    a.tanggalAbsensi BETWEEN ? AND ?
                ORDER BY
                    p.nama, a.tanggalAbsensi
                """
                cursor.execute(query, (start_date, end_date))
                columns = [column[0] for column in cursor.description]
                results = cursor.fetchall()
                
                result_window = tk.Toplevel(self)
                result_window.title("Laporan Kehadiran")
                
                tree = ttk.Treeview(result_window, columns=columns, show='headings')
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, minwidth=0, width=120)
                tree.pack(fill=tk.BOTH, expand=True)
                
                for row in results:
                    tree.insert('', tk.END, values=row)
                
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(self, text="Submit", command=submit_laporan_kehadiran).pack(pady=10)
        tk.Button(self, text="Back", command=self.show_pemilik_menu).pack(pady=10) 

