-- ⚠️ Jalankan TK3-Alia-Dump.sql dulu sebelum file ini!
-- Dependencies: PENGGUNA, TIER (dari Alia)

-- =================================================================
-- TABLE: BANDARA (15 data)
-- =================================================================
CREATE TABLE BANDARA (
    iata_code CHAR(3) PRIMARY KEY,
    nama      VARCHAR(100) NOT NULL,
    kota      VARCHAR(100) NOT NULL,
    negara    VARCHAR(100) NOT NULL
);

INSERT INTO BANDARA (iata_code, nama, kota, negara) VALUES
('CGK', 'Soekarno-Hatta International Airport',         'Tangerang',    'Indonesia'),
('DPS', 'Ngurah Rai International Airport',              'Denpasar',     'Indonesia'),
('SUB', 'Juanda International Airport',                  'Surabaya',     'Indonesia'),
('JOG', 'Adisutjipto International Airport',             'Yogyakarta',   'Indonesia'),
('MDC', 'Sam Ratulangi International Airport',           'Manado',       'Indonesia'),
('BPN', 'Sultan Aji Muhammad Sulaiman Airport',          'Balikpapan',   'Indonesia'),
('PLM', 'Sultan Mahmud Badaruddin II Airport',           'Palembang',    'Indonesia'),
('SIN', 'Singapore Changi Airport',                      'Singapore',    'Singapore'),
('KUL', 'Kuala Lumpur International Airport',            'Kuala Lumpur', 'Malaysia'),
('BKK', 'Suvarnabhumi Airport',                          'Bangkok',      'Thailand'),
('NRT', 'Narita International Airport',                  'Tokyo',        'Japan'),
('HKG', 'Hong Kong International Airport',               'Hong Kong',    'China'),
('ICN', 'Incheon International Airport',                 'Seoul',        'South Korea'),
('SYD', 'Sydney Kingsford Smith Airport',                'Sydney',       'Australia'),
('DOH', 'Hamad International Airport',                   'Doha',         'Qatar');

-- =================================================================
-- TABLE: MEMBER (50 data, email mengacu ke PENGGUNA dari Alia)
-- =================================================================
CREATE TABLE MEMBER (
    email             VARCHAR(100) PRIMARY KEY REFERENCES PENGGUNA(email),
    nomor_member      VARCHAR(20)  NOT NULL UNIQUE,
    tanggal_bergabung DATE         NOT NULL,
    id_tier           VARCHAR(10)  NOT NULL REFERENCES TIER(id_tier),
    award_miles       INT          DEFAULT 0,
    total_miles       INT          DEFAULT 0
);

INSERT INTO MEMBER (email, nomor_member, tanggal_bergabung, id_tier, award_miles, total_miles) VALUES
('karina.salsabila@email.com',  'M0001', '2022-01-10', 'T004', 180000, 250000),
('luthfi.akbar@email.com',      'M0002', '2022-02-15', 'T003',  55000,  90000),
('maya.handoko@email.com',      'M0003', '2022-03-20', 'T003',  60000,  95000),
('nanda.pratama@email.com',     'M0004', '2022-04-05', 'T002',  18000,  35000),
('only.wijaya@email.com',       'M0005', '2022-05-12', 'T002',  22000,  40000),
('prima.sakti@email.com',       'M0006', '2022-06-18', 'T001',   3000,   5000),
('qiana.sofia@email.com',       'M0007', '2022-07-22', 'T001',   4500,   7000),
('ridha.maulana@email.com',     'M0008', '2022-08-30', 'T002',  25000,  45000),
('sinta.kusuma@email.com',      'M0009', '2022-09-14', 'T003',  70000, 110000),
('taufik.mulya@email.com',      'M0010', '2022-10-01', 'T004', 200000, 300000),
('ulfa.rahmawati@email.com',    'M0011', '2022-11-05', 'T001',   2000,   3000),
('viki.pratama@email.com',      'M0012', '2022-12-10', 'T002',  12000,  20000),
('wulan.sari@email.com',        'M0013', '2023-01-08', 'T001',   5000,   8000),
('xandra.bella@email.com',      'M0014', '2023-02-14', 'T002',  15000,  28000),
('yanto.setiadi@email.com',     'M0015', '2023-03-20', 'T003',  52000,  80000),
('zara.aulia@email.com',        'M0016', '2023-04-25', 'T001',   1500,   2500),
('aldi.wijaya@email.com',       'M0017', '2023-05-30', 'T002',  20000,  38000),
('andi.hermawan@email.com',     'M0018', '2023-06-15', 'T001',   8000,  12000),
('anita.bulan@email.com',       'M0019', '2023-07-20', 'T002',  17000,  30000),
('bambang.irawan@email.com',    'M0020', '2023-08-10', 'T003',  65000, 100000),
('bella.rosita@email.com',      'M0021', '2023-09-05', 'T001',   3500,   5500),
('citra.dewi@email.com',        'M0022', '2023-10-12', 'T002',  14000,  25000),
('danny.wijaya@email.com',      'M0023', '2023-11-18', 'T004', 160000, 220000),
('endang.sari@email.com',       'M0024', '2023-12-01', 'T001',   6000,   9000),
('febri.agustin@email.com',     'M0025', '2024-01-07', 'T002',  11000,  18000),
('gerry.wijaya@email.com',      'M0026', '2024-02-14', 'T003',  58000,  88000),
('hendra.yanto@email.com',      'M0027', '2024-03-20', 'T001',   2500,   4000),
('irene.santoso@email.com',     'M0028', '2024-04-05', 'T002',  16000,  29000),
('joko.setiawan@email.com',     'M0029', '2024-05-11', 'T001',   4000,   6500),
('kartika.wijaya@email.com',    'M0030', '2024-06-18', 'T003',  75000, 120000),
('lina.marliana@email.com',     'M0031', '2024-07-22', 'T001',   7000,  11000),
('meldy.santoso@email.com',     'M0032', '2024-08-28', 'T002',  19000,  34000),
('novi.kusuma@email.com',       'M0033', '2024-09-04', 'T001',   5500,   8500),
('otis.wijaya@email.com',       'M0034', '2024-10-10', 'T004', 170000, 240000),
('pasha.kusuma@email.com',      'M0035', '2024-11-15', 'T002',  13000,  22000),
('qori.yusuf@email.com',        'M0036', '2024-12-01', 'T001',   3000,   4500),
('ratna.wijaya@email.com',      'M0037', '2025-01-08', 'T003',  62000,  95000),
('saiful.anwar@email.com',      'M0038', '2025-02-14', 'T001',   9000,  14000),
('tania.bella@email.com',       'M0039', '2025-03-20', 'T002',  21000,  37000),
('udang.haryo@email.com',       'M0040', '2025-04-05', 'T001',   1000,   1500),
('vanessa.dewi@email.com',      'M0041', '2025-05-10', 'T002',  10000,  17000),
('wahyu.sanusi@email.com',      'M0042', '2025-06-15', 'T003',  53000,  82000),
('xena.wijaya@email.com',       'M0043', '2025-07-20', 'T001',   4500,   7000),
('yuki.suzuki@email.com',       'M0044', '2025-08-25', 'T002',  18000,  32000),
('zulfikar.fahmi@email.com',    'M0045', '2025-09-01', 'T001',   2000,   3200),
('adriana.putri@email.com',     'M0046', '2025-10-08', 'T002',  16000,  28000),
('arif.kusuma@email.com',       'M0047', '2025-11-12', 'T001',   6500,  10000),
('astrid.murni@email.com',      'M0048', '2025-12-01', 'T003',  57000,  87000),
('aziz.irfandi@email.com',      'M0049', '2026-01-10', 'T001',   3500,   5500),
('ayu.citra@email.com',         'M0050', '2026-02-14', 'T002',  11000,  19000);

-- =================================================================
-- TABLE: IDENTITAS (30 data)
-- =================================================================
CREATE TABLE IDENTITAS (
    nomor           VARCHAR(50) PRIMARY KEY,
    email_member    VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    tanggal_habis   DATE         NOT NULL,
    tanggal_terbit  DATE         NOT NULL,
    negara_penerbit VARCHAR(50)  NOT NULL,
    jenis           VARCHAR(30)  NOT NULL CHECK (jenis IN ('Paspor', 'KTP', 'SIM'))
);

INSERT INTO IDENTITAS (nomor, email_member, tanggal_habis, tanggal_terbit, negara_penerbit, jenis) VALUES
('A12345678',    'karina.salsabila@email.com', '2029-01-10', '2019-01-10', 'Indonesia', 'Paspor'),
('3201010190001','karina.salsabila@email.com', '2026-01-10', '2021-01-10', 'Indonesia', 'KTP'),
('B23456789',    'luthfi.akbar@email.com',     '2028-02-15', '2018-02-15', 'Indonesia', 'Paspor'),
('C34567890',    'maya.handoko@email.com',     '2030-03-20', '2020-03-20', 'Indonesia', 'Paspor'),
('3201020390002','maya.handoko@email.com',     '2025-03-20', '2020-03-20', 'Indonesia', 'KTP'),
('D45678901',    'nanda.pratama@email.com',    '2027-04-05', '2017-04-05', 'Indonesia', 'Paspor'),
('E56789012',    'only.wijaya@email.com',      '2029-05-12', '2019-05-12', 'Indonesia', 'Paspor'),
('SIM-001-2021', 'prima.sakti@email.com',      '2026-06-18', '2021-06-18', 'Indonesia', 'SIM'),
('F67890123',    'ridha.maulana@email.com',    '2028-08-30', '2018-08-30', 'Indonesia', 'Paspor'),
('G78901234',    'sinta.kusuma@email.com',     '2030-09-14', '2020-09-14', 'Indonesia', 'Paspor'),
('3201090490003','sinta.kusuma@email.com',     '2027-09-14', '2022-09-14', 'Indonesia', 'KTP'),
('H89012345',    'taufik.mulya@email.com',     '2029-10-01', '2019-10-01', 'Indonesia', 'Paspor'),
('I90123456',    'ulfa.rahmawati@email.com',   '2027-11-05', '2022-11-05', 'Indonesia', 'Paspor'),
('J01234567',    'viki.pratama@email.com',     '2028-12-10', '2023-12-10', 'Indonesia', 'Paspor'),
('SIM-002-2022', 'wulan.sari@email.com',       '2027-01-08', '2022-01-08', 'Indonesia', 'SIM'),
('K12345670',    'xandra.bella@email.com',     '2029-02-14', '2024-02-14', 'Indonesia', 'Paspor'),
('L23456781',    'yanto.setiadi@email.com',    '2028-03-20', '2023-03-20', 'Indonesia', 'Paspor'),
('3201150490004','zara.aulia@email.com',       '2026-04-25', '2021-04-25', 'Indonesia', 'KTP'),
('M34567892',    'aldi.wijaya@email.com',      '2030-05-30', '2025-05-30', 'Indonesia', 'Paspor'),
('N45678903',    'andi.hermawan@email.com',    '2027-06-15', '2022-06-15', 'Indonesia', 'Paspor'),
('SIM-003-2023', 'anita.bulan@email.com',      '2028-07-20', '2023-07-20', 'Indonesia', 'SIM'),
('O56789014',    'bambang.irawan@email.com',   '2029-08-10', '2019-08-10', 'Indonesia', 'Paspor'),
('3201200890005','bambang.irawan@email.com',   '2026-08-10', '2021-08-10', 'Indonesia', 'KTP'),
('P67890125',    'bella.rosita@email.com',     '2028-09-05', '2023-09-05', 'Indonesia', 'Paspor'),
('Q78901236',    'citra.dewi@email.com',       '2030-10-12', '2025-10-12', 'Indonesia', 'Paspor'),
('R89012347',    'danny.wijaya@email.com',     '2027-11-18', '2022-11-18', 'Indonesia', 'Paspor'),
('SIM-004-2021', 'endang.sari@email.com',      '2026-12-01', '2021-12-01', 'Indonesia', 'SIM'),
('S90123458',    'febri.agustin@email.com',    '2029-01-07', '2024-01-07', 'Indonesia', 'Paspor'),
('T01234569',    'gerry.wijaya@email.com',     '2028-02-14', '2023-02-14', 'Indonesia', 'Paspor'),
('3201260290006','hendra.yanto@email.com',     '2027-03-20', '2022-03-20', 'Indonesia', 'KTP');