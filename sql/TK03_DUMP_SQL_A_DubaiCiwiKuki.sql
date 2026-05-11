DROP TABLE IF EXISTS REDEEM CASCADE;
DROP TABLE IF EXISTS HADIAH CASCADE;
DROP TABLE IF EXISTS TRANSFER CASCADE;
DROP TABLE IF EXISTS CLAIM_MISSING_MILES CASCADE;
DROP TABLE IF EXISTS MEMBER_AWARD_MILES_PACKAGE CASCADE;
DROP TABLE IF EXISTS AWARD_MILES_PACKAGE CASCADE;
DROP TABLE IF EXISTS IDENTITAS CASCADE;
DROP TABLE IF EXISTS MITRA CASCADE;
DROP TABLE IF EXISTS STAF CASCADE;
DROP TABLE IF EXISTS MASKAPAI CASCADE;
DROP TABLE IF EXISTS PENYEDIA CASCADE;
DROP TABLE IF EXISTS MEMBER CASCADE;
DROP TABLE IF EXISTS TIER CASCADE;
DROP TABLE IF EXISTS PENGGUNA CASCADE;

-- 1. PENGGUNA
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

-- 2. TIER
CREATE TABLE TIER (
    id_tier VARCHAR(10) PRIMARY KEY,
    nama VARCHAR(50) NOT NULL,
    minimal_frekuensi_terbang INT NOT NULL,
    minimal_tier_miles INT NOT NULL
);

INSERT INTO TIER (id_tier, nama, minimal_frekuensi_terbang, minimal_tier_miles) VALUES
('T001', 'Bronze', 0, 0),
('T002', 'Silver', 5, 10000),
('T003', 'Gold', 15, 50000),
('T004', 'Diamond', 30, 150000);

-- 3. MEMBER
CREATE TABLE MEMBER (
    email VARCHAR(100) PRIMARY KEY REFERENCES PENGGUNA(email) ON DELETE CASCADE,
    nomor_member VARCHAR(20) NOT NULL UNIQUE,
    tanggal_bergabung DATE NOT NULL,
    id_tier VARCHAR(10) NOT NULL REFERENCES TIER(id_tier),
    award_miles INT DEFAULT 0,
    total_miles INT DEFAULT 0
);

INSERT INTO MEMBER (email, nomor_member, tanggal_bergabung, id_tier, award_miles, total_miles) VALUES
('karina.salsabila@email.com', 'M0001', '2022-01-10', 'T004', 180000, 250000),
('luthfi.akbar@email.com', 'M0002', '2022-02-15', 'T003', 55000, 90000),
('maya.handoko@email.com', 'M0003', '2022-03-20', 'T003', 60000, 95000),
('nanda.pratama@email.com', 'M0004', '2022-04-05', 'T002', 18000, 35000),
('only.wijaya@email.com', 'M0005', '2022-05-12', 'T002', 22000, 40000),
('prima.sakti@email.com', 'M0006', '2022-06-18', 'T001', 3000, 5000),
('qiana.sofia@email.com', 'M0007', '2022-07-22', 'T001', 4500, 7000),
('ridha.maulana@email.com', 'M0008', '2022-08-28', 'T002', 25000, 45000),
('sinta.kusuma@email.com', 'M0009', '2022-09-14', 'T003', 70000, 110000),
('taufik.mulya@email.com', 'M0010', '2022-10-01', 'T004', 200000, 300000),
('ulfa.rahmawati@email.com', 'M0011', '2022-11-05', 'T004', 180000, 250000),
('viki.pratama@email.com', 'M0012', '2022-12-10', 'T003', 55000, 90000),
('wulan.sari@email.com', 'M0013', '2023-01-10', 'T003', 60000, 95000),
('xandra.bella@email.com', 'M0014', '2023-02-15', 'T002', 18000, 35000),
('yanto.setiadi@email.com', 'M0015', '2023-03-20', 'T002', 22000, 40000),
('zara.aulia@email.com', 'M0016', '2023-04-05', 'T001', 3000, 5000),
('aldi.wijaya@email.com', 'M0017', '2023-05-12', 'T001', 4500, 7000),
('andi.hermawan@email.com', 'M0018', '2023-06-18', 'T002', 25000, 45000),
('anita.bulan@email.com', 'M0019', '2023-07-22', 'T003', 70000, 110000),
('bambang.irawan@email.com', 'M0020', '2023-08-28', 'T004', 200000, 300000),
('bella.rosita@email.com', 'M0021', '2023-09-14', 'T004', 180000, 250000),
('citra.dewi@email.com', 'M0022', '2023-10-01', 'T003', 55000, 90000),
('danny.wijaya@email.com', 'M0023', '2023-11-05', 'T003', 60000, 95000),
('endang.sari@email.com', 'M0024', '2023-12-10', 'T002', 18000, 35000),
('febri.agustin@email.com', 'M0025', '2024-01-10', 'T002', 22000, 40000),
('gerry.wijaya@email.com', 'M0026', '2024-02-15', 'T001', 3000, 5000),
('hendra.yanto@email.com', 'M0027', '2024-03-20', 'T001', 4500, 7000),
('irene.santoso@email.com', 'M0028', '2024-04-05', 'T002', 25000, 45000),
('joko.setiawan@email.com', 'M0029', '2024-05-12', 'T003', 70000, 110000),
('kartika.wijaya@email.com', 'M0030', '2024-06-18', 'T004', 200000, 300000),
('lina.marliana@email.com', 'M0031', '2024-07-22', 'T004', 180000, 250000),
('meldy.santoso@email.com', 'M0032', '2024-08-28', 'T003', 55000, 90000),
('novi.kusuma@email.com', 'M0033', '2024-09-14', 'T003', 60000, 95000),
('otis.wijaya@email.com', 'M0034', '2024-10-01', 'T002', 18000, 35000),
('pasha.kusuma@email.com', 'M0035', '2024-11-05', 'T002', 22000, 40000),
('qori.yusuf@email.com', 'M0036', '2024-12-10', 'T001', 3000, 5000),
('ratna.wijaya@email.com', 'M0037', '2025-01-10', 'T001', 4500, 7000),
('saiful.anwar@email.com', 'M0038', '2025-02-15', 'T002', 25000, 45000),
('tania.bella@email.com', 'M0039', '2025-03-20', 'T003', 70000, 110000),
('udang.haryo@email.com', 'M0040', '2025-04-05', 'T004', 200000, 300000),
('vanessa.dewi@email.com', 'M0041', '2025-05-12', 'T004', 180000, 250000),
('wahyu.sanusi@email.com', 'M0042', '2025-06-18', 'T003', 55000, 90000),
('xena.wijaya@email.com', 'M0043', '2025-07-22', 'T003', 60000, 95000),
('yuki.suzuki@email.com', 'M0044', '2025-08-28', 'T002', 18000, 35000),
('zulfikar.fahmi@email.com', 'M0045', '2025-09-14', 'T002', 22000, 40000),
('adriana.putri@email.com', 'M0046', '2025-10-01', 'T001', 3000, 5000),
('arif.kusuma@email.com', 'M0047', '2025-11-05', 'T001', 4500, 7000),
('astrid.murni@email.com', 'M0048', '2025-12-10', 'T002', 25000, 45000),
('aziz.irfandi@email.com', 'M0049', '2026-01-10', 'T003', 70000, 110000),
('ayu.citra@email.com', 'M0050', '2026-02-15', 'T004', 200000, 300000);

-- 4. PENYEDIA
CREATE TABLE PENYEDIA (
    id SERIAL PRIMARY KEY
);

INSERT INTO PENYEDIA (id) VALUES
(1), (2), (3), (4), (5), (6), (7), (8);
SELECT setval(pg_get_serial_sequence('penyedia', 'id'), 8, true);

-- 5. MASKAPAI
CREATE TABLE MASKAPAI (
    kode_maskapai VARCHAR(10) PRIMARY KEY,
    nama_maskapai VARCHAR(100) NOT NULL,
    id_penyedia INT NOT NULL REFERENCES PENYEDIA(id)
);

INSERT INTO MASKAPAI (kode_maskapai, nama_maskapai, id_penyedia) VALUES
('GA', 'Garuda Indonesia', 1),
('QG', 'Citilink', 2),
('JT', 'Lion Air', 3),
('SJ', 'Sriwijaya Air', 4),
('ID', 'Batik Air', 5);

-- 6. STAF
CREATE TABLE STAF (
    email VARCHAR(100) PRIMARY KEY REFERENCES PENGGUNA(email) ON DELETE CASCADE,
    id_staf VARCHAR(20) NOT NULL UNIQUE,
    kode_maskapai VARCHAR(10) NOT NULL REFERENCES MASKAPAI(kode_maskapai)
);

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

-- 7. MITRA
CREATE TABLE MITRA (
    email_mitra VARCHAR(100) PRIMARY KEY,
    id_penyedia INT NOT NULL UNIQUE REFERENCES PENYEDIA(id) ON DELETE CASCADE,
    nama_mitra VARCHAR(100) NOT NULL,
    tanggal_kerja_sama DATE NOT NULL
);

INSERT INTO MITRA (email_mitra, id_penyedia, nama_mitra, tanggal_kerja_sama) VALUES
('hotelplus@aeromiles.id', 4, 'Hotel Plus Indonesia', '2023-01-15'),
('travelmart@aeromiles.id', 5, 'Travel Mart Asia', '2023-03-20'),
('foodies@aeromiles.id', 6, 'Foodies Reward', '2023-06-10'),
('shopindo@aeromiles.id', 7, 'ShopIndo Voucher', '2024-01-05'),
('rentcar@aeromiles.id', 8, 'RentCar Nusantara', '2024-02-12');

-- 8. IDENTITAS
CREATE TABLE IDENTITAS (
    nomor VARCHAR(50) PRIMARY KEY,
    email_member VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    tanggal_habis DATE NOT NULL,
    tanggal_terbit DATE NOT NULL,
    negara_penerbit VARCHAR(50) NOT NULL,
    jenis VARCHAR(30) NOT NULL CHECK (jenis IN ('Paspor', 'KTP', 'SIM'))
);

INSERT INTO IDENTITAS (nomor, email_member, tanggal_habis, tanggal_terbit, negara_penerbit, jenis) VALUES
('P-0001-AERO', 'karina.salsabila@email.com', '2030-01-20', '2024-01-20', 'Indonesia', 'Paspor'),
('KTP-0002-AERO', 'luthfi.akbar@email.com', '2030-02-20', '2024-02-20', 'Indonesia', 'KTP'),
('SIM-0003-AERO', 'maya.handoko@email.com', '2030-03-20', '2024-03-20', 'Indonesia', 'SIM'),
('P-0004-AERO', 'nanda.pratama@email.com', '2030-04-20', '2024-04-20', 'Indonesia', 'Paspor'),
('KTP-0005-AERO', 'only.wijaya@email.com', '2030-05-20', '2024-05-20', 'Indonesia', 'KTP'),
('SIM-0006-AERO', 'prima.sakti@email.com', '2030-06-20', '2024-06-20', 'Indonesia', 'SIM'),
('P-0007-AERO', 'qiana.sofia@email.com', '2030-07-20', '2024-07-20', 'Indonesia', 'Paspor'),
('KTP-0008-AERO', 'ridha.maulana@email.com', '2030-08-20', '2024-08-20', 'Indonesia', 'KTP'),
('SIM-0009-AERO', 'sinta.kusuma@email.com', '2030-09-20', '2024-09-20', 'Indonesia', 'SIM'),
('P-0010-AERO', 'taufik.mulya@email.com', '2030-10-20', '2024-10-20', 'Indonesia', 'Paspor'),
('KTP-0011-AERO', 'ulfa.rahmawati@email.com', '2030-11-20', '2024-11-20', 'Indonesia', 'KTP'),
('SIM-0012-AERO', 'viki.pratama@email.com', '2030-12-20', '2024-12-20', 'Indonesia', 'SIM'),
('P-0013-AERO', 'wulan.sari@email.com', '2030-01-20', '2024-01-20', 'Indonesia', 'Paspor'),
('KTP-0014-AERO', 'xandra.bella@email.com', '2030-02-20', '2024-02-20', 'Indonesia', 'KTP'),
('SIM-0015-AERO', 'yanto.setiadi@email.com', '2030-03-20', '2024-03-20', 'Indonesia', 'SIM'),
('P-0016-AERO', 'zara.aulia@email.com', '2030-04-20', '2024-04-20', 'Indonesia', 'Paspor'),
('KTP-0017-AERO', 'aldi.wijaya@email.com', '2030-05-20', '2024-05-20', 'Indonesia', 'KTP'),
('SIM-0018-AERO', 'andi.hermawan@email.com', '2030-06-20', '2024-06-20', 'Indonesia', 'SIM'),
('P-0019-AERO', 'anita.bulan@email.com', '2030-07-20', '2024-07-20', 'Indonesia', 'Paspor'),
('KTP-0020-AERO', 'bambang.irawan@email.com', '2030-08-20', '2024-08-20', 'Indonesia', 'KTP'),
('SIM-0021-AERO', 'bella.rosita@email.com', '2030-09-20', '2024-09-20', 'Indonesia', 'SIM'),
('P-0022-AERO', 'citra.dewi@email.com', '2030-10-20', '2024-10-20', 'Indonesia', 'Paspor'),
('KTP-0023-AERO', 'danny.wijaya@email.com', '2030-11-20', '2024-11-20', 'Indonesia', 'KTP'),
('SIM-0024-AERO', 'endang.sari@email.com', '2030-12-20', '2024-12-20', 'Indonesia', 'SIM'),
('P-0025-AERO', 'febri.agustin@email.com', '2030-01-20', '2024-01-20', 'Indonesia', 'Paspor'),
('KTP-0026-AERO', 'gerry.wijaya@email.com', '2030-02-20', '2024-02-20', 'Indonesia', 'KTP'),
('SIM-0027-AERO', 'hendra.yanto@email.com', '2030-03-20', '2024-03-20', 'Indonesia', 'SIM'),
('P-0028-AERO', 'irene.santoso@email.com', '2030-04-20', '2024-04-20', 'Indonesia', 'Paspor'),
('KTP-0029-AERO', 'joko.setiawan@email.com', '2030-05-20', '2024-05-20', 'Indonesia', 'KTP'),
('SIM-0030-AERO', 'kartika.wijaya@email.com', '2030-06-20', '2024-06-20', 'Indonesia', 'SIM');

-- 9. AWARD_MILES_PACKAGE
CREATE TABLE AWARD_MILES_PACKAGE (
    id VARCHAR(20) PRIMARY KEY,
    harga_paket DECIMAL(15,2) NOT NULL,
    jumlah_award_miles INT NOT NULL
);

INSERT INTO AWARD_MILES_PACKAGE (id, harga_paket, jumlah_award_miles) VALUES
('AMP-001', 150000.00, 1000),
('AMP-002', 650000.00, 5000),
('AMP-003', 1200000.00, 10000),
('AMP-004', 2750000.00, 25000),
('AMP-005', 5000000.00, 50000);

-- 10. MEMBER_AWARD_MILES_PACKAGE
CREATE TABLE MEMBER_AWARD_MILES_PACKAGE (
    id_award_miles_package VARCHAR(20) NOT NULL REFERENCES AWARD_MILES_PACKAGE(id),
    email_member VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (id_award_miles_package, email_member, timestamp)
);

INSERT INTO MEMBER_AWARD_MILES_PACKAGE (id_award_miles_package, email_member, timestamp) VALUES
('AMP-001', 'karina.salsabila@email.com', '2024-01-01 08:00:00'),
('AMP-002', 'luthfi.akbar@email.com', '2024-01-05 09:00:00'),
('AMP-003', 'maya.handoko@email.com', '2024-01-09 10:00:00'),
('AMP-004', 'nanda.pratama@email.com', '2024-01-13 11:00:00'),
('AMP-005', 'only.wijaya@email.com', '2024-01-17 12:00:00'),
('AMP-001', 'prima.sakti@email.com', '2024-02-01 13:00:00'),
('AMP-002', 'qiana.sofia@email.com', '2024-02-05 14:00:00'),
('AMP-003', 'ridha.maulana@email.com', '2024-02-09 15:00:00'),
('AMP-004', 'sinta.kusuma@email.com', '2024-02-13 16:00:00'),
('AMP-005', 'taufik.mulya@email.com', '2024-02-17 17:00:00'),
('AMP-001', 'ulfa.rahmawati@email.com', '2024-03-01 08:00:00'),
('AMP-002', 'viki.pratama@email.com', '2024-03-05 09:00:00'),
('AMP-003', 'wulan.sari@email.com', '2024-03-09 10:00:00'),
('AMP-004', 'xandra.bella@email.com', '2024-03-13 11:00:00'),
('AMP-005', 'yanto.setiadi@email.com', '2024-03-17 12:00:00'),
('AMP-001', 'zara.aulia@email.com', '2024-04-01 13:00:00'),
('AMP-002', 'aldi.wijaya@email.com', '2024-04-05 14:00:00'),
('AMP-003', 'andi.hermawan@email.com', '2024-04-09 15:00:00'),
('AMP-004', 'anita.bulan@email.com', '2024-04-13 16:00:00'),
('AMP-005', 'bambang.irawan@email.com', '2024-04-17 17:00:00');

-- 11. BANDARA
CREATE TABLE BANDARA (
    iata_code CHAR(3) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    kota VARCHAR(100) NOT NULL,
    negara VARCHAR(100) NOT NULL
);

INSERT INTO BANDARA (iata_code, nama, kota, negara) VALUES
('CGK', 'Soekarno-Hatta International Airport', 'Tangerang', 'Indonesia'),
('DPS', 'Ngurah Rai International Airport', 'Denpasar', 'Indonesia'),
('SUB', 'Juanda International Airport', 'Surabaya', 'Indonesia'),
('JOG', 'Adisutjipto International Airport', 'Yogyakarta', 'Indonesia'),
('MDC', 'Sam Ratulangi International Airport', 'Manado', 'Indonesia'),
('BPN', 'Sultan Aji Muhammad Sulaiman Airport', 'Balikpapan', 'Indonesia'),
('PLM', 'Sultan Mahmud Badaruddin II Airport', 'Palembang', 'Indonesia'),
('SIN', 'Singapore Changi Airport', 'Singapore', 'Singapore'),
('KUL', 'Kuala Lumpur International Airport', 'Kuala Lumpur', 'Malaysia'),
('BKK', 'Suvarnabhumi Airport', 'Bangkok', 'Thailand'),
('NRT', 'Narita International Airport', 'Tokyo', 'Japan'),
('HKG', 'Hong Kong International Airport', 'Hong Kong', 'China'),
('ICN', 'Incheon International Airport', 'Seoul', 'South Korea'),
('SYD', 'Sydney Kingsford Smith Airport', 'Sydney', 'Australia'),
('DOH', 'Hamad International Airport', 'Doha', 'Qatar');

-- 12. CLAIM_MISSING_MILES
CREATE TABLE CLAIM_MISSING_MILES (
    id SERIAL PRIMARY KEY,
    email_member VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    email_staf VARCHAR(100) NULL REFERENCES STAF(email),
    maskapai VARCHAR(10) NOT NULL REFERENCES MASKAPAI(kode_maskapai),
    bandara_asal CHAR(3) NOT NULL REFERENCES BANDARA(iata_code),
    bandara_tujuan CHAR(3) NOT NULL REFERENCES BANDARA(iata_code),
    tanggal_penerbangan DATE NOT NULL,
    flight_number VARCHAR(10) NOT NULL,
    nomor_tiket VARCHAR(20) NOT NULL,
    kelas_kabin VARCHAR(20) NOT NULL CHECK (kelas_kabin IN ('Economy', 'Business', 'First')),
    pnr VARCHAR(10) NOT NULL,
    status_penerimaan VARCHAR(20) NOT NULL DEFAULT 'Menunggu' CHECK (status_penerimaan IN ('Menunggu', 'Disetujui', 'Ditolak')),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_claim_no_duplicate UNIQUE (email_member, flight_number, tanggal_penerbangan, nomor_tiket)
);

INSERT INTO CLAIM_MISSING_MILES (email_member, email_staf, maskapai, bandara_asal, bandara_tujuan, tanggal_penerbangan, flight_number, nomor_tiket, kelas_kabin, pnr, status_penerimaan, timestamp) VALUES
('karina.salsabila@email.com', 'ahmad.rahman@email.com', 'GA', 'CGK', 'DPS', '2024-01-01', 'GA401', '001-1234567001', 'Economy', 'PNR0001', 'Disetujui', '2024-01-02 10:00:00'),
('luthfi.akbar@email.com', 'siti.nurhaliza@email.com', 'GA', 'DPS', 'CGK', '2024-02-02', 'GA402', '001-1234567002', 'Business', 'PNR0002', 'Disetujui', '2024-02-03 10:00:00'),
('maya.handoko@email.com', 'budi.santoso@email.com', 'QG', 'CGK', 'SUB', '2024-03-03', 'QG403', '001-1234567003', 'First', 'PNR0003', 'Disetujui', '2024-03-04 10:00:00'),
('nanda.pratama@email.com', 'dewi.lestari@email.com', 'QG', 'SUB', 'CGK', '2024-04-04', 'QG404', '001-1234567004', 'Economy', 'PNR0004', 'Disetujui', '2024-04-05 10:00:00'),
('only.wijaya@email.com', 'eka.putra@email.com', 'JT', 'CGK', 'JOG', '2024-05-05', 'JT405', '001-1234567005', 'Business', 'PNR0005', 'Disetujui', '2024-05-06 10:00:00'),
('prima.sakti@email.com', 'farah.yasmin@email.com', 'GA', 'SIN', 'NRT', '2024-06-06', 'GA406', '001-1234567006', 'First', 'PNR0006', 'Disetujui', '2024-06-07 10:00:00'),
('qiana.sofia@email.com', 'gunawan.setia@email.com', 'GA', 'KUL', 'BKK', '2024-07-07', 'GA407', '001-1234567007', 'Economy', 'PNR0007', 'Disetujui', '2024-07-08 10:00:00'),
('ridha.maulana@email.com', 'hana.widya@email.com', 'QG', 'HKG', 'ICN', '2024-08-08', 'QG408', '001-1234567008', 'Business', 'PNR0008', 'Ditolak', '2024-08-09 10:00:00'),
('sinta.kusuma@email.com', 'indra.kusuma@email.com', 'QG', 'SYD', 'DOH', '2024-09-09', 'QG409', '001-1234567009', 'First', 'PNR0009', 'Ditolak', '2024-09-10 10:00:00'),
('taufik.mulya@email.com', 'jaka.sinopati@email.com', 'JT', 'BPN', 'PLM', '2024-10-10', 'JT410', '001-1234567010', 'Economy', 'PNR0010', 'Ditolak', '2024-10-11 10:00:00'),
('ulfa.rahmawati@email.com', 'ahmad.rahman@email.com', 'GA', 'CGK', 'DPS', '2024-11-11', 'GA411', '001-1234567011', 'Business', 'PNR0011', 'Ditolak', '2024-11-12 10:00:00'),
('viki.pratama@email.com', 'siti.nurhaliza@email.com', 'GA', 'DPS', 'CGK', '2024-12-12', 'GA412', '001-1234567012', 'First', 'PNR0012', 'Ditolak', '2024-12-13 10:00:00'),
('wulan.sari@email.com', NULL, 'QG', 'CGK', 'SUB', '2024-01-13', 'QG413', '001-1234567013', 'Economy', 'PNR0013', 'Menunggu', '2024-01-14 10:00:00'),
('xandra.bella@email.com', NULL, 'QG', 'SUB', 'CGK', '2024-02-14', 'QG414', '001-1234567014', 'Business', 'PNR0014', 'Menunggu', '2024-02-15 10:00:00'),
('yanto.setiadi@email.com', NULL, 'JT', 'CGK', 'JOG', '2024-03-15', 'JT415', '001-1234567015', 'First', 'PNR0015', 'Menunggu', '2024-03-16 10:00:00'),
('zara.aulia@email.com', NULL, 'GA', 'SIN', 'NRT', '2024-04-16', 'GA416', '001-1234567016', 'Economy', 'PNR0016', 'Menunggu', '2024-04-17 10:00:00'),
('aldi.wijaya@email.com', NULL, 'GA', 'KUL', 'BKK', '2024-05-17', 'GA417', '001-1234567017', 'Business', 'PNR0017', 'Menunggu', '2024-05-18 10:00:00'),
('andi.hermawan@email.com', NULL, 'QG', 'HKG', 'ICN', '2024-06-18', 'QG418', '001-1234567018', 'First', 'PNR0018', 'Menunggu', '2024-06-19 10:00:00'),
('anita.bulan@email.com', NULL, 'QG', 'SYD', 'DOH', '2024-07-19', 'QG419', '001-1234567019', 'Economy', 'PNR0019', 'Menunggu', '2024-07-20 10:00:00'),
('bambang.irawan@email.com', NULL, 'JT', 'BPN', 'PLM', '2024-08-20', 'JT420', '001-1234567020', 'Business', 'PNR0020', 'Menunggu', '2024-08-21 10:00:00');

-- 13. TRANSFER
CREATE TABLE TRANSFER (
    email_member_1 VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    email_member_2 VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    jumlah INT NOT NULL,
    catatan VARCHAR(255),
    PRIMARY KEY (email_member_1, email_member_2, timestamp),
    CHECK (email_member_1 <> email_member_2)
);

INSERT INTO TRANSFER (email_member_1, email_member_2, timestamp, jumlah, catatan) VALUES
('karina.salsabila@email.com', 'luthfi.akbar@email.com', '2024-06-01 09:30:00', 500, 'Transfer miles #1'),
('luthfi.akbar@email.com', 'maya.handoko@email.com', '2024-06-02 10:30:00', 650, 'Transfer miles #2'),
('maya.handoko@email.com', 'nanda.pratama@email.com', '2024-06-03 11:30:00', 800, 'Transfer miles #3'),
('nanda.pratama@email.com', 'only.wijaya@email.com', '2024-06-04 12:30:00', 950, 'Transfer miles #4'),
('only.wijaya@email.com', 'prima.sakti@email.com', '2024-06-05 13:30:00', 1100, 'Transfer miles #5'),
('prima.sakti@email.com', 'qiana.sofia@email.com', '2024-06-06 14:30:00', 1250, 'Transfer miles #6'),
('qiana.sofia@email.com', 'ridha.maulana@email.com', '2024-06-07 15:30:00', 1400, 'Transfer miles #7'),
('ridha.maulana@email.com', 'sinta.kusuma@email.com', '2024-06-08 16:30:00', 1550, 'Transfer miles #8'),
('sinta.kusuma@email.com', 'taufik.mulya@email.com', '2024-06-09 17:30:00', 1700, 'Transfer miles #9'),
('taufik.mulya@email.com', 'ulfa.rahmawati@email.com', '2024-06-10 18:30:00', 1850, 'Transfer miles #10'),
('ulfa.rahmawati@email.com', 'viki.pratama@email.com', '2024-06-11 09:30:00', 2000, 'Transfer miles #11'),
('viki.pratama@email.com', 'wulan.sari@email.com', '2024-06-12 10:30:00', 2150, 'Transfer miles #12'),
('wulan.sari@email.com', 'xandra.bella@email.com', '2024-06-13 11:30:00', 2300, 'Transfer miles #13'),
('xandra.bella@email.com', 'yanto.setiadi@email.com', '2024-06-14 12:30:00', 2450, 'Transfer miles #14'),
('yanto.setiadi@email.com', 'zara.aulia@email.com', '2024-06-15 13:30:00', 2600, 'Transfer miles #15');

-- 14. HADIAH
CREATE TABLE HADIAH (
    kode_hadiah VARCHAR(20) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    miles INT NOT NULL,
    deskripsi TEXT,
    valid_start_date DATE NOT NULL,
    program_end DATE NOT NULL,
    id_penyedia INT NOT NULL REFERENCES PENYEDIA(id) ON DELETE CASCADE
);

INSERT INTO HADIAH (kode_hadiah, nama, miles, deskripsi, valid_start_date, program_end, id_penyedia) VALUES
('RWD-001', 'Upgrade Business Class', 15000, 'Upgrade kursi ke Business Class.', '2024-01-01', '2026-12-31', 1),
('RWD-002', 'Extra Baggage 20kg', 8000, 'Tambahan bagasi sebesar 20kg.', '2024-01-01', '2026-12-31', 1),
('RWD-003', 'Airport Lounge Access', 12000, 'Akses lounge bandara internasional.', '2024-01-01', '2026-12-31', 2),
('RWD-004', 'Hotel Voucher Rp500.000', 10000, 'Voucher menginap di Hotel Plus.', '2024-01-01', '2026-12-31', 4),
('RWD-005', 'Travel Voucher Rp300.000', 7000, 'Voucher pembelian tiket di Travel Mart.', '2024-01-01', '2026-12-31', 5),
('RWD-006', 'Dining Voucher Rp250.000', 6000, 'Voucher makan di merchant Foodies.', '2024-01-01', '2026-12-31', 6),
('RWD-007', 'Shopping Voucher Rp400.000', 9000, 'Voucher belanja di ShopIndo.', '2024-01-01', '2026-12-31', 7),
('RWD-008', 'Car Rental Discount', 11000, 'Diskon sewa mobil dari RentCar Nusantara.', '2024-01-01', '2026-12-31', 8),
('RWD-009', 'Priority Boarding', 5000, 'Fasilitas naik pesawat lebih awal.', '2024-01-01', '2026-12-31', 3),
('RWD-010', 'Free Seat Selection', 4000, 'Bebas memilih kursi penerbangan.', '2024-01-01', '2026-12-31', 2);

-- 15. REDEEM
CREATE TABLE REDEEM (
    email_member VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    kode_hadiah VARCHAR(20) NOT NULL REFERENCES HADIAH(kode_hadiah),
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (email_member, kode_hadiah, timestamp)
);

INSERT INTO REDEEM (email_member, kode_hadiah, timestamp) VALUES
('karina.salsabila@email.com', 'RWD-001', '2024-08-01 10:00:00'),
('luthfi.akbar@email.com', 'RWD-002', '2024-08-02 11:00:00'),
('maya.handoko@email.com', 'RWD-003', '2024-08-03 12:00:00'),
('nanda.pratama@email.com', 'RWD-004', '2024-08-04 13:00:00'),
('only.wijaya@email.com', 'RWD-005', '2024-08-05 14:00:00'),
('prima.sakti@email.com', 'RWD-006', '2024-08-06 15:00:00'),
('qiana.sofia@email.com', 'RWD-007', '2024-08-07 16:00:00'),
('ridha.maulana@email.com', 'RWD-008', '2024-08-08 17:00:00'),
('sinta.kusuma@email.com', 'RWD-009', '2024-08-09 18:00:00'),
('taufik.mulya@email.com', 'RWD-010', '2024-08-10 09:00:00'),
('ulfa.rahmawati@email.com', 'RWD-001', '2024-08-11 10:00:00'),
('viki.pratama@email.com', 'RWD-002', '2024-08-12 11:00:00'),
('wulan.sari@email.com', 'RWD-003', '2024-08-13 12:00:00'),
('xandra.bella@email.com', 'RWD-004', '2024-08-14 13:00:00'),
('yanto.setiadi@email.com', 'RWD-005', '2024-08-15 14:00:00'),
('zara.aulia@email.com', 'RWD-006', '2024-08-16 15:00:00'),
('aldi.wijaya@email.com', 'RWD-007', '2024-08-17 16:00:00'),
('andi.hermawan@email.com', 'RWD-008', '2024-08-18 17:00:00'),
('anita.bulan@email.com', 'RWD-009', '2024-08-19 18:00:00'),
('bambang.irawan@email.com', 'RWD-010', '2024-08-20 09:00:00');
