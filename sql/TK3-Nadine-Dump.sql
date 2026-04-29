-- ⚠️ Jalankan group1_alia.sql dulu sebelum file ini!
-- Dependencies: PENGGUNA, TIER (dari group 1)

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
('SIN', 'Singapore Changi Airport', 'Singapore', 'Singapore'),
('KUL', 'Kuala Lumpur International Airport', 'Kuala Lumpur', 'Malaysia'),
('BKK', 'Suvarnabhumi Airport', 'Bangkok', 'Thailand'),
('NRT', 'Narita International Airport', 'Tokyo', 'Japan'),
('HKG', 'Hong Kong International Airport', 'Hong Kong', 'China'),
('ICN', 'Incheon International Airport', 'Seoul', 'South Korea'),
('SYD', 'Sydney Kingsford Smith Airport', 'Sydney', 'Australia'),
('DOH', 'Hamad International Airport', 'Doha', 'Qatar');

CREATE TABLE MEMBER (
    email VARCHAR(100) PRIMARY KEY REFERENCES PENGGUNA(email),
    nomor_member VARCHAR(20) NOT NULL UNIQUE,
    tanggal_bergabung DATE NOT NULL,
    id_tier VARCHAR(10) NOT NULL REFERENCES TIER(id_tier),
    award_miles INT DEFAULT 0,
    total_miles INT DEFAULT 0
);

CREATE TABLE IDENTITAS (
    nomor VARCHAR(50) PRIMARY KEY,
    email_member VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    tanggal_habis DATE NOT NULL,
    tanggal_terbit DATE NOT NULL,
    negara_penerbit VARCHAR(50) NOT NULL,
    jenis VARCHAR(30) NOT NULL CHECK (jenis IN ('Paspor', 'KTP', 'SIM'))
);