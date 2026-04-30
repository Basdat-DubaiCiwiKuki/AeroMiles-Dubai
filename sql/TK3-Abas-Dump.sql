-- =================================================================
--  TK03 | Dump SQL — Group 3: Claim Missing Miles
--  Kelompok A-10
--  Nama File  : TK03_DUMP_SQL_A_10_group3.sql
--
--  Urutan eksekusi (jalankan berurutan):
--    1. TK3-Alia-Dump.sql   → PENGGUNA, TIER, MASKAPAI, STAF
--    2. TK3-Nadine-Dump.sql → BANDARA, MEMBER, IDENTITAS
--    3. TK3-Abas-Dump.sql   → CLAIM_MISSING_MILES          ← file ini
--    4. TK3-Shafa-Dump.sql  → PENYEDIA, MITRA, HADIAH,
--                              AWARD_MILES_PACKAGE,
--                              MEMBER_AWARD_MILES_PACKAGE,
--                              TRANSFER, REDEEM
--
--  Dependencies tabel:
--    MEMBER  (email_member)  → dari Nadine
--    STAF    (email_staf)    → dari Alia
--    MASKAPAI(maskapai)      → dari Alia
--    BANDARA (bandara_asal,
--             bandara_tujuan)→ dari Nadine
-- =================================================================

-- -----------------------------------------------------------------
-- TABLE: CLAIM_MISSING_MILES
-- -----------------------------------------------------------------
CREATE TABLE claim_missing_miles (
    id                   SERIAL        PRIMARY KEY,

    -- Member yang mengajukan klaim
    email_member         VARCHAR(100)  NOT NULL
                             REFERENCES member(email)
                             ON DELETE CASCADE,

    -- Staf yang memproses klaim; NULL jika belum ditangani
    email_staf           VARCHAR(100)  NULL
                             REFERENCES staf(email),

    -- Detail penerbangan
    maskapai             VARCHAR(10)   NOT NULL
                             REFERENCES maskapai(kode_maskapai),
    bandara_asal         CHAR(3)       NOT NULL
                             REFERENCES bandara(iata_code),
    bandara_tujuan       CHAR(3)       NOT NULL
                             REFERENCES bandara(iata_code),
    tanggal_penerbangan  DATE          NOT NULL,
    flight_number        VARCHAR(10)   NOT NULL,
    nomor_tiket          VARCHAR(20)   NOT NULL,

    -- FIX: tambah 'Premium Economy' agar konsisten dengan data Khayra
    kelas_kabin          VARCHAR(20)   NOT NULL
                             CHECK (kelas_kabin IN
                                    ('Economy', 'Premium Economy',
                                     'Business', 'First')),
    pnr                  VARCHAR(10)   NOT NULL,

    -- Status & waktu pengajuan
    status_penerimaan    VARCHAR(20)   NOT NULL DEFAULT 'Menunggu'
                             CHECK (status_penerimaan IN
                                    ('Menunggu', 'Disetujui', 'Ditolak')),
    timestamp            TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Mencegah pengajuan klaim duplikat untuk penerbangan yang sama
    -- (kombinasi member + nomor penerbangan + tanggal + nomor tiket harus unik)
    CONSTRAINT uq_claim_no_duplicate
        UNIQUE (email_member, flight_number, tanggal_penerbangan, nomor_tiket)
);

-- -----------------------------------------------------------------
-- DATA DUMMY  (20 baris minimum sesuai spesifikasi TK03)
--
-- Email member mengacu pada data yang diinsert oleh Nadine (group 2).
-- Email staf   mengacu pada data yang diinsert oleh Alia  (group 1).
--
-- Distribusi status:
--   Disetujui  : 7 baris
--   Ditolak    : 5 baris
--   Menunggu   : 8 baris
-- -----------------------------------------------------------------

INSERT INTO claim_missing_miles
    (email_member, email_staf, maskapai,
     bandara_asal, bandara_tujuan, tanggal_penerbangan,
     flight_number, nomor_tiket, kelas_kabin, pnr,
     status_penerimaan, timestamp)
VALUES

-- ── Disetujui (7 baris) ─────────────────────────────────────────
('member01@aeromiles.id', 'staf01@aeromiles.id', 'GA',
 'CGK', 'DPS', '2024-06-10',
 'GA404',  '001-1234567001', 'Business',        'ABX101',
 'Disetujui', '2024-06-15 09:12:00'),

('member02@aeromiles.id', 'staf01@aeromiles.id', 'SQ',
 'SIN', 'NRT', '2024-07-03',
 'SQ026',  '001-1234567002', 'Economy',         'CDX202',
 'Disetujui', '2024-07-08 14:30:00'),

('member03@aeromiles.id', 'staf02@aeromiles.id', 'MH',
 'KUL', 'BKK', '2024-07-20',
 'MH780',  '001-1234567003', 'Premium Economy', 'EFX303',
 'Disetujui', '2024-07-25 10:45:00'),

('member04@aeromiles.id', 'staf02@aeromiles.id', 'GA',
 'CGK', 'SUB', '2024-08-05',
 'GA200',  '001-1234567004', 'Economy',         'GHX404',
 'Disetujui', '2024-08-10 08:20:00'),

('member05@aeromiles.id', 'staf01@aeromiles.id', 'SQ',
 'SIN', 'HKG', '2024-08-18',
 'SQ882',  '001-1234567005', 'First',           'IJX505',
 'Disetujui', '2024-08-23 16:00:00'),

('member06@aeromiles.id', 'staf03@aeromiles.id', 'GA',
 'DPS', 'CGK', '2024-09-01',
 'GA401',  '001-1234567006', 'Economy',         'KLX606',
 'Disetujui', '2024-09-06 11:30:00'),

('member07@aeromiles.id', 'staf03@aeromiles.id', 'MH',
 'KUL', 'NRT', '2024-09-14',
 'MH070',  '001-1234567007', 'Business',        'MNX707',
 'Disetujui', '2024-09-19 13:15:00'),

-- ── Ditolak (5 baris) ───────────────────────────────────────────
('member01@aeromiles.id', 'staf01@aeromiles.id', 'GA',
 'CGK', 'JOG', '2024-10-05',
 'GA152',  '001-1234567008', 'Economy',         'OPX808',
 'Ditolak', '2024-10-10 09:00:00'),

('member02@aeromiles.id', 'staf02@aeromiles.id', 'SQ',
 'SIN', 'ICN', '2024-10-20',
 'SQ600',  '001-1234567009', 'Premium Economy', 'QRX909',
 'Ditolak', '2024-10-25 15:40:00'),

('member08@aeromiles.id', 'staf01@aeromiles.id', 'GA',
 'DPS', 'SUB', '2024-11-02',
 'GA087',  '001-1234567010', 'Economy',         'STX010',
 'Ditolak', '2024-11-07 07:55:00'),

('member09@aeromiles.id', 'staf03@aeromiles.id', 'MH',
 'KUL', 'DOH', '2024-11-10',
 'MH003',  '001-1234567011', 'Business',        'UVX011',
 'Ditolak', '2024-11-15 12:00:00'),

('member10@aeromiles.id', 'staf02@aeromiles.id', 'SQ',
 'SIN', 'SYD', '2024-11-25',
 'SQ211',  '001-1234567012', 'Economy',         'WXX012',
 'Ditolak', '2024-11-30 10:20:00'),

-- ── Menunggu (8 baris) ──────────────────────────────────────────
('member03@aeromiles.id', NULL, 'SQ',
 'SIN', 'NRT', '2024-12-01',
 'SQ012',  '001-1234567013', 'Economy',         'YZX013',
 'Menunggu', '2024-12-06 18:45:00'),

('member04@aeromiles.id', NULL, 'MH',
 'KUL', 'BKK', '2025-01-10',
 'MH782',  '001-1234567014', 'Premium Economy', 'AAX014',
 'Menunggu', '2025-01-15 09:30:00'),

('member05@aeromiles.id', NULL, 'GA',
 'CGK', 'DPS', '2025-01-22',
 'GA406',  '001-1234567015', 'First',           'BBX015',
 'Menunggu', '2025-01-27 14:00:00'),

('member06@aeromiles.id', NULL, 'GA',
 'SUB', 'CGK', '2025-02-03',
 'GA150',  '001-1234567016', 'Economy',         'CCX016',
 'Menunggu', '2025-02-08 08:10:00'),

('member07@aeromiles.id', NULL, 'SQ',
 'SIN', 'HKG', '2025-02-17',
 'SQ890',  '001-1234567017', 'Business',        'DDX017',
 'Menunggu', '2025-02-22 11:50:00'),

('member08@aeromiles.id', NULL, 'MH',
 'KUL', 'ICN', '2025-03-05',
 'MH066',  '001-1234567018', 'Economy',         'EEX018',
 'Menunggu', '2025-03-10 16:35:00'),

('member09@aeromiles.id', NULL, 'GA',
 'CGK', 'BPN', '2025-03-18',
 'GA570',  '001-1234567019', 'Economy',         'FFX019',
 'Menunggu', '2025-03-23 07:20:00'),

('member10@aeromiles.id', NULL, 'SQ',
 'SIN', 'SYD', '2025-04-01',
 'SQ231',  '001-1234567020', 'First',           'GGX020',
 'Menunggu', '2025-04-06 13:00:00');