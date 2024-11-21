-- Create Kecamatan table
CREATE TABLE Kecamatan(
    idKecamatan int IDENTITY(1,1) PRIMARY KEY,
    namaKecamatan varchar(100) NOT NULL
);

-- Create Kelurahan table
CREATE TABLE Kelurahan(
    idKelurahan int IDENTITY(1,1) PRIMARY KEY,
    namaKelurahan varchar(100) NOT NULL,
    idKecamatan int FOREIGN KEY REFERENCES Kecamatan(idKecamatan)
);

-- Create Pemilik table
CREATE TABLE Pemilik(
    username varchar(50) NOT NULL PRIMARY KEY,
    email varchar(50) NOT NULL,
    password varchar(50) NOT NULL

);
-- Create Jabatan table
CREATE TABLE Jabatan(
    idJabatan int PRIMARY KEY,
    namaJabatan varchar(100) NOT NULL,
    satuanGaji int NOT NULL
);

-- Create Pegawai table
CREATE TABLE Pegawai(
    idPegawai int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    nama varchar(255) NOT NULL,
    NomorTelepon varchar(15) NOT NULL,
    email varchar(255) NOT NULL,
    Alamat varchar(100) NOT NULL,
    idKelurahan int NOT NULL FOREIGN KEY REFERENCES Kelurahan(idKelurahan),
    idJabatan int NOT NULL FOREIGN KEY REFERENCES Jabatan(idJabatan)
);

-- Create Absensi table with Durasi column
CREATE TABLE Absensi (
    idAbsensi int IDENTITY(1,1) PRIMARY KEY,
    idPegawai int NOT NULL,
    waktuMasuk TIME,
    waktuKeluar TIME,
    tanggalAbsensi DATE DEFAULT CAST(GETDATE() AS DATE),
    Durasi TIME,
    FOREIGN KEY (idPegawai) REFERENCES Pegawai(idPegawai)