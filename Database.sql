-- Insert initial data into Jabatan table
INSERT INTO Jabatan (idJabatan, namaJabatan, satuanGaji) VALUES
(1, 'Manajer', 200000),
(2, 'Koki', 150000),
(3, 'Bartender', 120000),
(4, 'Pelayan', 100000),
(5, 'Kasir', 100000);

-- Insert initial data into Kecamatan and Kelurahan
INSERT INTO Kecamatan (namaKecamatan) VALUES
('Andir'), ('Astana Anyar'), ('Antapani'), ('Arcamanik'), ('Babakan Ciparay'),
('Bandung Kidul'), ('Bandung Kulon'), ('Batununggal'), ('Bojongloa Kaler'), ('Bojongloa Kidul');

INSERT INTO Kelurahan (namaKelurahan, idKecamatan) VALUES
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
('Situsaeur', 10), ('Cibaduyut Kidul', 10), ('Cibaduyut', 10);