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