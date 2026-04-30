
CREATE TABLE PENYEDIA (
    id SERIAL PRIMARY KEY
);

INSERT INTO PENYEDIA DEFAULT VALUES;
INSERT INTO PENYEDIA DEFAULT VALUES;
INSERT INTO PENYEDIA DEFAULT VALUES;
INSERT INTO PENYEDIA DEFAULT VALUES;
INSERT INTO PENYEDIA DEFAULT VALUES;
INSERT INTO PENYEDIA DEFAULT VALUES;
INSERT INTO PENYEDIA DEFAULT VALUES;
INSERT INTO PENYEDIA DEFAULT VALUES;


-- =========================================================
-- MITRA
-- Minimal: 5 data
-- =========================================================

CREATE TABLE MITRA (
    email_mitra VARCHAR(100) PRIMARY KEY,
    id_penyedia INT NOT NULL UNIQUE,
    nama_mitra VARCHAR(100) NOT NULL,
    tanggal_kerja_sama DATE NOT NULL,
    FOREIGN KEY (id_penyedia) REFERENCES PENYEDIA(id) ON DELETE CASCADE
);

INSERT INTO MITRA 
(email_mitra, id_penyedia, nama_mitra, tanggal_kerja_sama)
VALUES
('hotelplus@aeromiles.id', 4, 'Hotel Plus Indonesia', '2023-01-15'),
('travelmart@aeromiles.id', 5, 'Travel Mart Asia', '2023-03-20'),
('foodies@aeromiles.id', 6, 'Foodies Reward', '2023-06-10'),
('shopindo@aeromiles.id', 7, 'ShopIndo Voucher', '2024-01-05'),
('rentcar@aeromiles.id', 8, 'RentCar Nusantara', '2024-02-12');


-- =========================================================
-- AWARD_MILES_PACKAGE
-- Minimal: 5 data
-- =========================================================

CREATE TABLE AWARD_MILES_PACKAGE (
    id VARCHAR(20) PRIMARY KEY,
    harga_paket DECIMAL(15,2) NOT NULL,
    jumlah_award_miles INT NOT NULL
);

INSERT INTO AWARD_MILES_PACKAGE 
(id, harga_paket, jumlah_award_miles)
VALUES
('AMP-001', 150000.00, 1000),
('AMP-002', 650000.00, 5000),
('AMP-003', 1200000.00, 10000),
('AMP-004', 2750000.00, 25000),
('AMP-005', 5000000.00, 50000);


-- =========================================================
-- HADIAH
-- Minimal: 10 data
-- =========================================================

CREATE TABLE HADIAH (
    kode_hadiah VARCHAR(20) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    miles INT NOT NULL,
    deskripsi TEXT,
    valid_start_date DATE NOT NULL,
    program_end DATE NOT NULL,
    id_penyedia INT NOT NULL,
    FOREIGN KEY (id_penyedia) REFERENCES PENYEDIA(id) ON DELETE CASCADE
);

INSERT INTO HADIAH
(kode_hadiah, nama, miles, deskripsi, valid_start_date, program_end, id_penyedia)
VALUES
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


-- =========================================================
-- MEMBER_AWARD_MILES_PACKAGE
-- Pembelian miles package
-- Minimal: 20 data
-- =========================================================

CREATE TABLE MEMBER_AWARD_MILES_PACKAGE (
    id_award_miles_package VARCHAR(20) NOT NULL,
    email_member VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (id_award_miles_package, email_member, timestamp),
    FOREIGN KEY (id_award_miles_package) REFERENCES AWARD_MILES_PACKAGE(id),
    FOREIGN KEY (email_member) REFERENCES MEMBER(email) ON DELETE CASCADE
);

INSERT INTO MEMBER_AWARD_MILES_PACKAGE
(id_award_miles_package, email_member, timestamp)
VALUES
('AMP-001', 'member01@aeromiles.id', '2024-01-10 10:00:00'),
('AMP-002', 'member02@aeromiles.id', '2024-01-15 11:30:00'),
('AMP-003', 'member03@aeromiles.id', '2024-01-20 09:45:00'),
('AMP-004', 'member04@aeromiles.id', '2024-02-01 14:20:00'),
('AMP-005', 'member05@aeromiles.id', '2024-02-05 16:10:00'),
('AMP-001', 'member06@aeromiles.id', '2024-02-10 08:30:00'),
('AMP-002', 'member07@aeromiles.id', '2024-02-14 12:00:00'),
('AMP-003', 'member08@aeromiles.id', '2024-03-01 13:15:00'),
('AMP-004', 'member09@aeromiles.id', '2024-03-05 17:40:00'),
('AMP-005', 'member10@aeromiles.id', '2024-03-10 19:25:00'),
('AMP-001', 'member01@aeromiles.id', '2024-04-01 10:05:00'),
('AMP-002', 'member02@aeromiles.id', '2024-04-03 11:10:00'),
('AMP-003', 'member03@aeromiles.id', '2024-04-07 15:30:00'),
('AMP-004', 'member04@aeromiles.id', '2024-04-12 09:00:00'),
('AMP-005', 'member05@aeromiles.id', '2024-04-18 20:15:00'),
('AMP-001', 'member06@aeromiles.id', '2024-05-01 07:55:00'),
('AMP-002', 'member07@aeromiles.id', '2024-05-06 13:25:00'),
('AMP-003', 'member08@aeromiles.id', '2024-05-10 18:45:00'),
('AMP-004', 'member09@aeromiles.id', '2024-05-15 21:00:00'),
('AMP-005', 'member10@aeromiles.id', '2024-05-20 22:10:00');


-- =========================================================
-- TRANSFER
-- Minimal: 15 data
-- =========================================================

CREATE TABLE TRANSFER (
    email_member_1 VARCHAR(100) NOT NULL,
    email_member_2 VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    jumlah INT NOT NULL,
    catatan VARCHAR(255),
    PRIMARY KEY (email_member_1, email_member_2, timestamp),
    FOREIGN KEY (email_member_1) REFERENCES MEMBER(email) ON DELETE CASCADE,
    FOREIGN KEY (email_member_2) REFERENCES MEMBER(email) ON DELETE CASCADE,
    CHECK (email_member_1 <> email_member_2)
);

INSERT INTO TRANSFER
(email_member_1, email_member_2, timestamp, jumlah, catatan)
VALUES
('member01@aeromiles.id', 'member02@aeromiles.id', '2024-06-01 10:00:00', 1000, 'Transfer keluarga'),
('member02@aeromiles.id', 'member03@aeromiles.id', '2024-06-03 11:15:00', 1500, 'Bantuan redeem'),
('member03@aeromiles.id', 'member04@aeromiles.id', '2024-06-05 12:30:00', 2000, 'Hadiah miles'),
('member04@aeromiles.id', 'member05@aeromiles.id', '2024-06-07 13:45:00', 1200, 'Transfer teman'),
('member05@aeromiles.id', 'member06@aeromiles.id', '2024-06-09 15:00:00', 1800, 'Untuk perjalanan'),
('member06@aeromiles.id', 'member07@aeromiles.id', '2024-06-11 16:20:00', 2500, 'Sharing miles'),
('member07@aeromiles.id', 'member08@aeromiles.id', '2024-06-13 09:10:00', 900, 'Transfer kecil'),
('member08@aeromiles.id', 'member09@aeromiles.id', '2024-06-15 18:25:00', 3000, 'Redeem bantuan'),
('member09@aeromiles.id', 'member10@aeromiles.id', '2024-06-17 19:40:00', 1100, 'Miles tambahan'),
('member10@aeromiles.id', 'member01@aeromiles.id', '2024-06-19 20:55:00', 1600, 'Balasan transfer'),
('member01@aeromiles.id', 'member03@aeromiles.id', '2024-07-01 10:30:00', 1400, 'Transfer promo'),
('member02@aeromiles.id', 'member04@aeromiles.id', '2024-07-03 11:45:00', 2200, 'Untuk tiket'),
('member03@aeromiles.id', 'member05@aeromiles.id', '2024-07-05 14:10:00', 1750, 'Bantuan miles'),
('member04@aeromiles.id', 'member06@aeromiles.id', '2024-07-07 17:35:00', 1300, 'Transfer reguler'),
('member05@aeromiles.id', 'member07@aeromiles.id', '2024-07-09 21:05:00', 2800, 'Redeem hadiah');


-- =========================================================
-- REDEEM
-- Minimal: 20 data
-- =========================================================

CREATE TABLE REDEEM (
    email_member VARCHAR(100) NOT NULL,
    kode_hadiah VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (email_member, kode_hadiah, timestamp),
    FOREIGN KEY (email_member) REFERENCES MEMBER(email) ON DELETE CASCADE,
    FOREIGN KEY (kode_hadiah) REFERENCES HADIAH(kode_hadiah)
);

INSERT INTO REDEEM
(email_member, kode_hadiah, timestamp)
VALUES
('member01@aeromiles.id', 'RWD-001', '2024-08-01 10:00:00'),
('member02@aeromiles.id', 'RWD-002', '2024-08-02 11:15:00'),
('member03@aeromiles.id', 'RWD-003', '2024-08-03 12:30:00'),
('member04@aeromiles.id', 'RWD-004', '2024-08-04 13:45:00'),
('member05@aeromiles.id', 'RWD-005', '2024-08-05 15:00:00'),
('member06@aeromiles.id', 'RWD-006', '2024-08-06 16:20:00'),
('member07@aeromiles.id', 'RWD-007', '2024-08-07 09:10:00'),
('member08@aeromiles.id', 'RWD-008', '2024-08-08 18:25:00'),
('member09@aeromiles.id', 'RWD-009', '2024-08-09 19:40:00'),
('member10@aeromiles.id', 'RWD-010', '2024-08-10 20:55:00'),
('member01@aeromiles.id', 'RWD-002', '2024-09-01 10:30:00'),
('member02@aeromiles.id', 'RWD-003', '2024-09-02 11:45:00'),
('member03@aeromiles.id', 'RWD-004', '2024-09-03 14:10:00'),
('member04@aeromiles.id', 'RWD-005', '2024-09-04 17:35:00'),
('member05@aeromiles.id', 'RWD-006', '2024-09-05 21:05:00'),
('member06@aeromiles.id', 'RWD-007', '2024-09-06 08:50:00'),
('member07@aeromiles.id', 'RWD-008', '2024-09-07 12:05:00'),
('member08@aeromiles.id', 'RWD-009', '2024-09-08 13:25:00'),
('member09@aeromiles.id', 'RWD-010', '2024-09-09 14:45:00'),
('member10@aeromiles.id', 'RWD-001', '2024-09-10 16:00:00');