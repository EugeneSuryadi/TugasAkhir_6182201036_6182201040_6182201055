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