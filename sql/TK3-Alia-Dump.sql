CREATE TABLE PENGGUNA (
    email VARCHAR(100) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    salutation VARCHAR(10) NOT NULL,
    first_mid_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(5) NOT NULL,
    mobile_number VARCHAR(20) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    kewarganegaraan VARCHAR(50) NOT NULL
);

CREATE TABLE TIER (
    id_tier VARCHAR(10) PRIMARY KEY,
    nama VARCHAR(50) NOT NULL,
    minimal_frekuensi_terbang INT NOT NULL,
    minimal_tier_miles INT NOT NULL
);

CREATE TABLE MASKAPAI (
    kode_maskapai VARCHAR(10) PRIMARY KEY,
    nama_maskapai VARCHAR(100) NOT NULL
);

CREATE TABLE STAF (
    email VARCHAR(100) PRIMARY KEY,
    id_staf VARCHAR(20) NOT NULL UNIQUE,
    kode_maskapai VARCHAR(10) NOT NULL,
    FOREIGN KEY (email) REFERENCES PENGGUNA(email),
    FOREIGN KEY (kode_maskapai) REFERENCES MASKAPAI(kode_maskapai)
);


INSERT INTO TIER (id_tier, nama, minimal_frekuensi_terbang, minimal_tier_miles) VALUES
('T001', 'Bronze', 0, 0),
('T002', 'Silver', 5, 10000),
('T003', 'Gold', 15, 50000),
('T004', 'Diamond', 30, 150000);

INSERT INTO PENGGUNA (email, password, salutation, first_mid_name, last_name, country_code, mobile_number, tanggal_lahir, kewarganegaraan) VALUES
('ahmad.rahman@email.com', 'hashed_password_001', 'Mr.', 'Ahmad', 'Rahman', '+62', '081234567001', '1990-03-15', 'Indonesia'),
('siti.nurhaliza@email.com', 'hashed_password_002', 'Mrs.', 'Siti', 'Nurhaliza', '+62', '081234567002', '1992-07-22', 'Indonesia'),
('budi.santoso@email.com', 'hashed_password_003', 'Mr.', 'Budi', 'Santoso', '+62', '081234567003', '1988-11-10', 'Indonesia'),
('dewi.lestari@email.com', 'hashed_password_004', 'Ms.', 'Dewi', 'Lestari', '+62', '081234567004', '1995-05-18', 'Indonesia'),
('eka.putra@email.com', 'hashed_password_005', 'Mr.', 'Eka', 'Putra', '+62', '081234567005', '1991-09-25', 'Indonesia'),
('farah.yasmin@email.com', 'hashed_password_006', 'Ms.', 'Farah', 'Yasmin', '+62', '081234567006', '1993-01-30', 'Indonesia'),
('gunawan.setia@email.com', 'hashed_password_007', 'Mr.', 'Gunawan', 'Setia', '+62', '081234567007', '1987-12-05', 'Indonesia'),
('hana.widya@email.com', 'hashed_password_008', 'Mrs.', 'Hana', 'Widya', '+62', '081234567008', '1994-06-12', 'Indonesia'),
('indra.kusuma@email.com', 'hashed_password_009', 'Mr.', 'Indra', 'Kusuma', '+62', '081234567009', '1989-08-20', 'Indonesia'),
('jaka.sinopati@email.com', 'hashed_password_010', 'Mr.', 'Jaka', 'Sinopati', '+62', '081234567010', '1992-02-14', 'Indonesia'),
('karina.salsabila@email.com', 'hashed_password_011', 'Ms.', 'Karina', 'Salsabila', '+62', '081234567011', '1996-04-08', 'Indonesia'),
('luthfi.akbar@email.com', 'hashed_password_012', 'Mr.', 'Luthfi', 'Akbar', '+62', '081234567012', '1990-10-17', 'Indonesia'),
('maya.handoko@email.com', 'hashed_password_013', 'Ms.', 'Maya', 'Handoko', '+62', '081234567013', '1994-11-23', 'Indonesia'),
('nanda.pratama@email.com', 'hashed_password_014', 'Mr.', 'Nanda', 'Pratama', '+62', '081234567014', '1991-03-09', 'Indonesia'),
('only.wijaya@email.com', 'hashed_password_015', 'Mrs.', 'Only', 'Wijaya', '+62', '081234567015', '1988-05-27', 'Indonesia'),
('prima.sakti@email.com', 'hashed_password_016', 'Mr.', 'Prima', 'Sakti', '+62', '081234567016', '1993-07-14', 'Indonesia'),
('qiana.sofia@email.com', 'hashed_password_017', 'Ms.', 'Qiana', 'Sofia', '+62', '081234567017', '1995-12-21', 'Indonesia'),
('ridha.maulana@email.com', 'hashed_password_018', 'Mr.', 'Ridha', 'Maulana', '+62', '081234567018', '1989-09-03', 'Indonesia'),
('sinta.kusuma@email.com', 'hashed_password_019', 'Mrs.', 'Sinta', 'Kusuma', '+62', '081234567019', '1992-01-16', 'Indonesia'),
('taufik.mulya@email.com', 'hashed_password_020', 'Mr.', 'Taufik', 'Mulya', '+62', '081234567020', '1990-06-28', 'Indonesia'),
('ulfa.rahmawati@email.com', 'hashed_password_021', 'Ms.', 'Ulfa', 'Rahmawati', '+62', '081234567021', '1994-08-11', 'Indonesia'),
('viki.pratama@email.com', 'hashed_password_022', 'Mr.', 'Viki', 'Pratama', '+62', '081234567022', '1991-04-19', 'Indonesia'),
('wulan.sari@email.com', 'hashed_password_023', 'Mrs.', 'Wulan', 'Sari', '+62', '081234567023', '1993-10-06', 'Indonesia'),
('xandra.bella@email.com', 'hashed_password_024', 'Ms.', 'Xandra', 'Bella', '+62', '081234567024', '1996-02-24', 'Indonesia'),
('yanto.setiadi@email.com', 'hashed_password_025', 'Mr.', 'Yanto', 'Setiadi', '+62', '081234567025', '1988-12-15', 'Indonesia'),
('zara.aulia@email.com', 'hashed_password_026', 'Mrs.', 'Zara', 'Aulia', '+62', '081234567026', '1992-05-31', 'Indonesia'),
('aldi.wijaya@email.com', 'hashed_password_027', 'Mr.', 'Aldi', 'Wijaya', '+62', '081234567027', '1990-09-12', 'Indonesia'),
('andi.hermawan@email.com', 'hashed_password_028', 'Mr.', 'Andi', 'Hermawan', '+62', '081234567028', '1989-03-07', 'Indonesia'),
('anita.bulan@email.com', 'hashed_password_029', 'Ms.', 'Anita', 'Bulan', '+62', '081234567029', '1995-07-29', 'Indonesia'),
('bambang.irawan@email.com', 'hashed_password_030', 'Mr.', 'Bambang', 'Irawan', '+62', '081234567030', '1991-11-22', 'Indonesia'),
('bella.rosita@email.com', 'hashed_password_031', 'Mrs.', 'Bella', 'Rosita', '+62', '081234567031', '1993-06-13', 'Indonesia'),
('citra.dewi@email.com', 'hashed_password_032', 'Ms.', 'Citra', 'Dewi', '+62', '081234567032', '1994-01-25', 'Indonesia'),
('danny.wijaya@email.com', 'hashed_password_033', 'Mr.', 'Danny', 'Wijaya', '+62', '081234567033', '1988-08-04', 'Indonesia'),
('endang.sari@email.com', 'hashed_password_034', 'Mrs.', 'Endang', 'Sari', '+62', '081234567034', '1992-10-17', 'Indonesia'),
('febri.agustin@email.com', 'hashed_password_035', 'Mrs.', 'Febri', 'Agustin', '+62', '081234567035', '1994-04-02', 'Indonesia'),
('gerry.wijaya@email.com', 'hashed_password_036', 'Mr.', 'Gerry', 'Wijaya', '+62', '081234567036', '1990-02-19', 'Indonesia'),
('hendra.yanto@email.com', 'hashed_password_037', 'Mr.', 'Hendra', 'Yanto', '+62', '081234567037', '1989-07-26', 'Indonesia'),
('irene.santoso@email.com', 'hashed_password_038', 'Ms.', 'Irene', 'Santoso', '+62', '081234567038', '1996-09-10', 'Indonesia'),
('joko.setiawan@email.com', 'hashed_password_039', 'Mr.', 'Joko', 'Setiawan', '+62', '081234567039', '1991-12-08', 'Indonesia'),
('kartika.wijaya@email.com', 'hashed_password_040', 'Mrs.', 'Kartika', 'Wijaya', '+62', '081234567040', '1993-03-21', 'Indonesia'),
('lina.marliana@email.com', 'hashed_password_041', 'Ms.', 'Lina', 'Marliana', '+62', '081234567041', '1995-05-14', 'Indonesia'),
('meldy.santoso@email.com', 'hashed_password_042', 'Mrs.', 'Meldy', 'Santoso', '+62', '081234567042', '1990-11-30', 'Indonesia'),
('novi.kusuma@email.com', 'hashed_password_043', 'Mrs.', 'Novi', 'Kusuma', '+62', '081234567043', '1992-08-23', 'Indonesia'),
('otis.wijaya@email.com', 'hashed_password_044', 'Mr.', 'Otis', 'Wijaya', '+62', '081234567044', '1988-04-15', 'Indonesia'),
('pasha.kusuma@email.com', 'hashed_password_045', 'Mr.', 'Pasha', 'Kusuma', '+62', '081234567045', '1991-01-09', 'Indonesia'),
('qori.yusuf@email.com', 'hashed_password_046', 'Mr.', 'Qori', 'Yusuf', '+62', '081234567046', '1989-06-17', 'Indonesia'),
('ratna.wijaya@email.com', 'hashed_password_047', 'Mrs.', 'Ratna', 'Wijaya', '+62', '081234567047', '1994-09-05', 'Indonesia'),
('saiful.anwar@email.com', 'hashed_password_048', 'Mr.', 'Saiful', 'Anwar', '+62', '081234567048', '1992-02-28', 'Indonesia'),
('tania.bella@email.com', 'hashed_password_049', 'Ms.', 'Tania', 'Bella', '+62', '081234567049', '1995-10-12', 'Indonesia'),
('udang.haryo@email.com', 'hashed_password_050', 'Mr.', 'Udang', 'Haryo', '+62', '081234567050', '1990-07-03', 'Indonesia'),
('vanessa.dewi@email.com', 'hashed_password_051', 'Ms.', 'Vanessa', 'Dewi', '+62', '081234567051', '1993-12-19', 'Indonesia'),
('wahyu.sanusi@email.com', 'hashed_password_052', 'Mr.', 'Wahyu', 'Sanusi', '+62', '081234567052', '1991-05-24', 'Indonesia'),
('xena.wijaya@email.com', 'hashed_password_053', 'Mrs.', 'Xena', 'Wijaya', '+62', '081234567053', '1994-03-11', 'Indonesia'),
('yuki.suzuki@email.com', 'hashed_password_054', 'Ms.', 'Yuki', 'Suzuki', '+65', '081234567054', '1996-08-07', 'Singapore'),
('zulfikar.fahmi@email.com', 'hashed_password_055', 'Mr.', 'Zulfikar', 'Fahmi', '+62', '081234567055', '1988-10-22', 'Indonesia'),
('adriana.putri@email.com', 'hashed_password_056', 'Ms.', 'Adriana', 'Putri', '+62', '081234567056', '1995-01-14', 'Indonesia'),
('arif.kusuma@email.com', 'hashed_password_057', 'Mr.', 'Arif', 'Kusuma', '+62', '081234567057', '1989-04-06', 'Indonesia'),
('astrid.murni@email.com', 'hashed_password_058', 'Mrs.', 'Astrid', 'Murni', '+62', '081234567058', '1992-09-09', 'Indonesia'),
('aziz.irfandi@email.com', 'hashed_password_059', 'Mr.', 'Aziz', 'Irfandi', '+62', '081234567059', '1990-12-31', 'Indonesia'),
('ayu.citra@email.com', 'hashed_password_060', 'Mrs.', 'Ayu', 'Citra', '+62', '081234567060', '1993-11-27', 'Indonesia');


INSERT INTO MASKAPAI (kode_maskapai, nama_maskapai) VALUES
('GA', 'Garuda Indonesia'),
('QG', 'Citilink'),
('JT', 'Lion Air'),
('SJ', 'Sriwijaya Air'),
('ID', 'Batik Air');


INSERT INTO STAF (email, id_staf, kode_maskapai) VALUES
('ahmad.rahman@email.com', 'S0001', 'GA'),
('siti.nurhaliza@email.com', 'S0002', 'GA'),
('budi.santoso@email.com', 'S0003', 'QG'),
('dewi.lestari@email.com', 'S0004', 'QG'),
('eka.putra@email.com', 'S0005', 'JT'),
('farah.yasmin@email.com', 'S0006', 'JT'),
('gunawan.setia@email.com', 'S0007', 'SJ'),
('hana.widya@email.com', 'S0008', 'SJ'),
('indra.kusuma@email.com', 'S0009', 'ID'),
('jaka.sinopati@email.com', 'S0010', 'ID');