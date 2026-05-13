DROP TABLE IF EXISTS REDEEM CASCADE;
DROP TABLE IF EXISTS HADIAH CASCADE;
DROP TABLE IF EXISTS TRANSFER CASCADE;
DROP TABLE IF EXISTS CLAIM_MISSING_MILES CASCADE;
DROP TABLE IF EXISTS MEMBER_AWARD_MILES_PACKAGE CASCADE;
DROP TABLE IF EXISTS AWARD_MILES_PACKAGE CASCADE;
DROP TABLE IF EXISTS IDENTITAS CASCADE;
DROP TABLE IF EXISTS JENIS_IDENTITAS CASCADE;
DROP TABLE IF EXISTS MITRA CASCADE;
DROP TABLE IF EXISTS STAF CASCADE;
DROP TABLE IF EXISTS MASKAPAI CASCADE;
DROP TABLE IF EXISTS PENYEDIA CASCADE;
DROP TABLE IF EXISTS MEMBER CASCADE;
DROP TABLE IF EXISTS BANDARA CASCADE;
DROP TABLE IF EXISTS TIER CASCADE;
DROP TABLE IF EXISTS PENGGUNA CASCADE;
DROP FUNCTION IF EXISTS generate_prefixed_id(regclass, text, text, text, int);
DROP SEQUENCE IF EXISTS member_nomor_member_seq;
DROP SEQUENCE IF EXISTS staf_id_staf_seq;
DROP SEQUENCE IF EXISTS award_miles_package_id_seq;
DROP SEQUENCE IF EXISTS hadiah_kode_hadiah_seq;

CREATE SEQUENCE member_nomor_member_seq START 1;
CREATE SEQUENCE staf_id_staf_seq START 1;
CREATE SEQUENCE award_miles_package_id_seq START 1;
CREATE SEQUENCE hadiah_kode_hadiah_seq START 1;

CREATE OR REPLACE FUNCTION generate_prefixed_id(
    p_sequence regclass,
    p_table_name text,
    p_column_name text,
    p_prefix text,
    p_width int
)
RETURNS text AS $$
DECLARE
    v_max_number int;
    v_sequence_number int;
    v_next_number int;
BEGIN
    PERFORM pg_advisory_xact_lock(hashtext(p_table_name || '.' || p_column_name));

    EXECUTE format(
        'SELECT COALESCE(MAX(CAST(SUBSTRING(%I FROM %s) AS INTEGER)), 0)
           FROM %I
          WHERE LEFT(%I, %s) = %L
            AND SUBSTRING(%I FROM %s) ~ ''^[0-9]+$''',
        p_column_name,
        length(p_prefix) + 1,
        p_table_name,
        p_column_name,
        length(p_prefix),
        p_prefix,
        p_column_name,
        length(p_prefix) + 1
    )
    INTO v_max_number;

    v_sequence_number := nextval(p_sequence)::int;
    v_next_number := GREATEST(v_max_number + 1, v_sequence_number);
    PERFORM setval(p_sequence, v_next_number, true);

    RETURN p_prefix || LPAD(v_next_number::text, p_width, '0');
END;
$$ LANGUAGE plpgsql;

CREATE TABLE PENGGUNA (
    email VARCHAR(100) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    salutation VARCHAR(10) NOT NULL CHECK (salutation IN ('Mr.', 'Mrs.', 'Ms.', 'Dr.')),
    first_mid_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(5) NOT NULL,
    mobile_number VARCHAR(20) NOT NULL UNIQUE,
    tanggal_lahir DATE NOT NULL,
    kewarganegaraan VARCHAR(50) NOT NULL
);

INSERT INTO PENGGUNA (email, password, salutation, first_mid_name, last_name, country_code, mobile_number, tanggal_lahir, kewarganegaraan) VALUES
('john@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'John William', 'Doe', '+62', '081234567890', '1990-05-15', 'Indonesia'),
('admin@aeromiles.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Admin', 'Aero', '+62', '081111111111', '1988-01-01', 'Indonesia'),
('ahmad.rahman@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Ahmad', 'Rahman', '+62', '081234567001', '1990-03-15', 'Indonesia'),
('siti.nurhaliza@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Siti', 'Nurhaliza', '+62', '081234567002', '1992-07-22', 'Indonesia'),
('budi.santoso@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Budi', 'Santoso', '+62', '081234567003', '1988-11-10', 'Indonesia'),
('dewi.lestari@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Dewi', 'Lestari', '+62', '081234567004', '1995-05-18', 'Indonesia'),
('eka.putra@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Eka', 'Putra', '+62', '081234567005', '1991-09-25', 'Indonesia'),
('farah.yasmin@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Farah', 'Yasmin', '+62', '081234567006', '1993-01-30', 'Indonesia'),
('gunawan.setia@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Gunawan', 'Setia', '+62', '081234567007', '1987-12-05', 'Indonesia'),
('hana.widya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Hana', 'Widya', '+62', '081234567008', '1994-06-12', 'Indonesia'),
('indra.kusuma@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Indra', 'Kusuma', '+62', '081234567009', '1989-08-20', 'Indonesia'),
('jaka.sinopati@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Jaka', 'Sinopati', '+62', '081234567010', '1992-02-14', 'Indonesia'),
-- Member (50 data)
('karina.salsabila@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Karina', 'Salsabila', '+62', '081234567011', '1996-04-08', 'Indonesia'),
('luthfi.akbar@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Luthfi', 'Akbar', '+62', '081234567012', '1990-10-17', 'Indonesia'),
('maya.handoko@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Maya', 'Handoko', '+62', '081234567013', '1994-11-23', 'Indonesia'),
('nanda.pratama@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Nanda', 'Pratama', '+62', '081234567014', '1991-03-09', 'Indonesia'),
('only.wijaya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Only', 'Wijaya', '+62', '081234567015', '1988-05-27', 'Indonesia'),
('prima.sakti@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Prima', 'Sakti', '+62', '081234567016', '1993-07-14', 'Indonesia'),
('qiana.sofia@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Qiana', 'Sofia', '+62', '081234567017', '1995-12-21', 'Indonesia'),
('ridha.maulana@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Ridha', 'Maulana', '+62', '081234567018', '1989-09-03', 'Indonesia'),
('sinta.kusuma@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Sinta', 'Kusuma', '+62', '081234567019', '1992-01-16', 'Indonesia'),
('taufik.mulya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Taufik', 'Mulya', '+62', '081234567020', '1990-06-28', 'Indonesia'),
('ulfa.rahmawati@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Ulfa', 'Rahmawati', '+62', '081234567021', '1994-08-11', 'Indonesia'),
('viki.pratama@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Viki', 'Pratama', '+62', '081234567022', '1991-04-19', 'Indonesia'),
('wulan.sari@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Wulan', 'Sari', '+62', '081234567023', '1993-10-06', 'Indonesia'),
('xandra.bella@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Xandra', 'Bella', '+62', '081234567024', '1996-02-24', 'Indonesia'),
('yanto.setiadi@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Yanto', 'Setiadi', '+62', '081234567025', '1988-12-15', 'Indonesia'),
('zara.aulia@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Zara', 'Aulia', '+62', '081234567026', '1992-05-31', 'Indonesia'),
('aldi.wijaya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Aldi', 'Wijaya', '+62', '081234567027', '1990-09-12', 'Indonesia'),
('andi.hermawan@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Andi', 'Hermawan', '+62', '081234567028', '1989-03-07', 'Indonesia'),
('anita.bulan@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Anita', 'Bulan', '+62', '081234567029', '1995-07-29', 'Indonesia'),
('bambang.irawan@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Bambang', 'Irawan', '+62', '081234567030', '1991-11-22', 'Indonesia'),
('bella.rosita@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Bella', 'Rosita', '+62', '081234567031', '1993-06-13', 'Indonesia'),
('citra.dewi@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Citra', 'Dewi', '+62', '081234567032', '1994-01-25', 'Indonesia'),
('danny.wijaya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Danny', 'Wijaya', '+62', '081234567033', '1988-08-04', 'Indonesia'),
('endang.sari@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Endang', 'Sari', '+62', '081234567034', '1992-10-17', 'Indonesia'),
('febri.agustin@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Febri', 'Agustin', '+62', '081234567035', '1994-04-02', 'Indonesia'),
('gerry.wijaya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Gerry', 'Wijaya', '+62', '081234567036', '1990-02-19', 'Indonesia'),
('hendra.yanto@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Hendra', 'Yanto', '+62', '081234567037', '1989-07-26', 'Indonesia'),
('irene.santoso@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Irene', 'Santoso', '+62', '081234567038', '1996-09-10', 'Indonesia'),
('joko.setiawan@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Joko', 'Setiawan', '+62', '081234567039', '1991-12-08', 'Indonesia'),
('kartika.wijaya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Kartika', 'Wijaya', '+62', '081234567040', '1993-03-21', 'Indonesia'),
('lina.marliana@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Lina', 'Marliana', '+62', '081234567041', '1995-05-14', 'Indonesia'),
('meldy.santoso@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Meldy', 'Santoso', '+62', '081234567042', '1990-11-30', 'Indonesia'),
('novi.kusuma@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Novi', 'Kusuma', '+62', '081234567043', '1992-08-23', 'Indonesia'),
('otis.wijaya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Otis', 'Wijaya', '+62', '081234567044', '1988-04-15', 'Indonesia'),
('pasha.kusuma@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Pasha', 'Kusuma', '+62', '081234567045', '1991-01-09', 'Indonesia'),
('qori.yusuf@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Qori', 'Yusuf', '+62', '081234567046', '1989-06-17', 'Indonesia'),
('ratna.wijaya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Ratna', 'Wijaya', '+62', '081234567047', '1994-09-05', 'Indonesia'),
('saiful.anwar@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Saiful', 'Anwar', '+62', '081234567048', '1992-02-28', 'Indonesia'),
('tania.bella@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Tania', 'Bella', '+62', '081234567049', '1995-10-12', 'Indonesia'),
('udang.haryo@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Udang', 'Haryo', '+62', '081234567050', '1990-07-03', 'Indonesia'),
('vanessa.dewi@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Vanessa', 'Dewi', '+62', '081234567051', '1993-12-19', 'Indonesia'),
('wahyu.sanusi@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Wahyu', 'Sanusi', '+62', '081234567052', '1991-05-24', 'Indonesia'),
('xena.wijaya@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Xena', 'Wijaya', '+62', '081234567053', '1994-03-11', 'Indonesia'),
('yuki.suzuki@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Yuki', 'Suzuki', '+65', '081234567054', '1996-08-07', 'Singapore'),
('zulfikar.fahmi@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Zulfikar', 'Fahmi', '+62', '081234567055', '1988-10-22', 'Indonesia'),
('adriana.putri@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ms.', 'Adriana', 'Putri', '+62', '081234567056', '1995-01-14', 'Indonesia'),
('arif.kusuma@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Arif', 'Kusuma', '+62', '081234567057', '1989-04-06', 'Indonesia'),
('astrid.murni@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Astrid', 'Murni', '+62', '081234567058', '1992-09-09', 'Indonesia'),
('aziz.irfandi@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mr.', 'Aziz', 'Irfandi', '+62', '081234567059', '1990-12-31', 'Indonesia'),
('ayu.citra@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Mrs.', 'Ayu', 'Citra', '+62', '081234567060', '1993-11-27', 'Indonesia');

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

CREATE TABLE MEMBER (
    email VARCHAR(100) PRIMARY KEY REFERENCES PENGGUNA(email) ON DELETE CASCADE,
    nomor_member VARCHAR(20) NOT NULL UNIQUE DEFAULT generate_prefixed_id('member_nomor_member_seq'::regclass, 'member', 'nomor_member', 'M', 4),
    tanggal_bergabung DATE NOT NULL,
    id_tier VARCHAR(10) NOT NULL REFERENCES TIER(id_tier),
    award_miles INT DEFAULT 0 CHECK (award_miles >= 0),
    total_miles INT DEFAULT 0 CHECK (total_miles >= 0)
);

INSERT INTO MEMBER (email, nomor_member, tanggal_bergabung, id_tier, award_miles, total_miles) VALUES
('john@example.com', 'M0001', '2024-01-15', 'T003', 32000, 55000),
('karina.salsabila@email.com', 'M0002', '2022-01-10', 'T004', 180000, 250000),
('luthfi.akbar@email.com', 'M0003', '2022-02-15', 'T003', 55000, 90000),
('maya.handoko@email.com', 'M0004', '2022-03-20', 'T003', 60000, 95000),
('nanda.pratama@email.com', 'M0005', '2022-04-05', 'T002', 18000, 35000),
('only.wijaya@email.com', 'M0006', '2022-05-12', 'T002', 22000, 40000),
('prima.sakti@email.com', 'M0007', '2022-06-18', 'T001', 3000, 5000),
('qiana.sofia@email.com', 'M0008', '2022-07-22', 'T001', 4500, 7000),
('ridha.maulana@email.com', 'M0009', '2022-08-28', 'T002', 25000, 45000),
('sinta.kusuma@email.com', 'M0010', '2022-09-14', 'T003', 70000, 110000),
('taufik.mulya@email.com', 'M0011', '2022-10-01', 'T004', 200000, 300000),
('ulfa.rahmawati@email.com', 'M0012', '2022-11-05', 'T004', 180000, 250000),
('viki.pratama@email.com', 'M0013', '2022-12-10', 'T003', 55000, 90000),
('wulan.sari@email.com', 'M0014', '2023-01-10', 'T003', 60000, 95000),
('xandra.bella@email.com', 'M0015', '2023-02-15', 'T002', 18000, 35000),
('yanto.setiadi@email.com', 'M0016', '2023-03-20', 'T002', 22000, 40000),
('zara.aulia@email.com', 'M0017', '2023-04-05', 'T001', 3000, 5000),
('aldi.wijaya@email.com', 'M0018', '2023-05-12', 'T001', 4500, 7000),
('andi.hermawan@email.com', 'M0019', '2023-06-18', 'T002', 25000, 45000),
('anita.bulan@email.com', 'M0020', '2023-07-22', 'T003', 70000, 110000),
('bambang.irawan@email.com', 'M0021', '2023-08-28', 'T004', 200000, 300000),
('bella.rosita@email.com', 'M0022', '2023-09-14', 'T004', 180000, 250000),
('citra.dewi@email.com', 'M0023', '2023-10-01', 'T003', 55000, 90000),
('danny.wijaya@email.com', 'M0024', '2023-11-05', 'T003', 60000, 95000),
('endang.sari@email.com', 'M0025', '2023-12-10', 'T002', 18000, 35000),
('febri.agustin@email.com', 'M0026', '2024-01-10', 'T002', 22000, 40000),
('gerry.wijaya@email.com', 'M0027', '2024-02-15', 'T001', 3000, 5000),
('hendra.yanto@email.com', 'M0028', '2024-03-20', 'T001', 4500, 7000),
('irene.santoso@email.com', 'M0029', '2024-04-05', 'T002', 25000, 45000),
('joko.setiawan@email.com', 'M0030', '2024-05-12', 'T003', 70000, 110000),
('kartika.wijaya@email.com', 'M0031', '2024-06-18', 'T004', 200000, 300000),
('lina.marliana@email.com', 'M0032', '2024-07-22', 'T004', 180000, 250000),
('meldy.santoso@email.com', 'M0033', '2024-08-28', 'T003', 55000, 90000),
('novi.kusuma@email.com', 'M0034', '2024-09-14', 'T003', 60000, 95000),
('otis.wijaya@email.com', 'M0035', '2024-10-01', 'T002', 18000, 35000),
('pasha.kusuma@email.com', 'M0036', '2024-11-05', 'T002', 22000, 40000),
('qori.yusuf@email.com', 'M0037', '2024-12-10', 'T001', 3000, 5000),
('ratna.wijaya@email.com', 'M0038', '2025-01-10', 'T001', 4500, 7000),
('saiful.anwar@email.com', 'M0039', '2025-02-15', 'T002', 25000, 45000),
('tania.bella@email.com', 'M0040', '2025-03-20', 'T003', 70000, 110000),
('udang.haryo@email.com', 'M0041', '2025-04-05', 'T004', 200000, 300000),
('vanessa.dewi@email.com', 'M0042', '2025-05-12', 'T004', 180000, 250000),
('wahyu.sanusi@email.com', 'M0043', '2025-06-18', 'T003', 55000, 90000),
('xena.wijaya@email.com', 'M0044', '2025-07-22', 'T003', 60000, 95000),
('yuki.suzuki@email.com', 'M0045', '2025-08-28', 'T002', 18000, 35000),
('zulfikar.fahmi@email.com', 'M0046', '2025-09-14', 'T002', 22000, 40000),
('adriana.putri@email.com', 'M0047', '2025-10-01', 'T001', 3000, 5000),
('arif.kusuma@email.com', 'M0048', '2025-11-05', 'T001', 4500, 7000),
('astrid.murni@email.com', 'M0049', '2025-12-10', 'T002', 25000, 45000),
('aziz.irfandi@email.com', 'M0050', '2026-01-10', 'T003', 70000, 110000),
('ayu.citra@email.com', 'M0051', '2026-02-15', 'T004', 200000, 300000);
SELECT setval('member_nomor_member_seq', (SELECT COALESCE(MAX(CAST(SUBSTRING(nomor_member FROM 2) AS INTEGER)), 1) FROM MEMBER), true);

CREATE TABLE PENYEDIA (
    id SERIAL PRIMARY KEY
);

INSERT INTO PENYEDIA (id) VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
SELECT setval(pg_get_serial_sequence('penyedia','id'), 10, true);

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

CREATE TABLE STAF (
    email VARCHAR(100) PRIMARY KEY REFERENCES PENGGUNA(email) ON DELETE CASCADE,
    id_staf VARCHAR(20) NOT NULL UNIQUE DEFAULT generate_prefixed_id('staf_id_staf_seq'::regclass, 'staf', 'id_staf', 'S', 4),
    kode_maskapai VARCHAR(10) NOT NULL REFERENCES MASKAPAI(kode_maskapai)
);

INSERT INTO STAF (email, id_staf, kode_maskapai) VALUES
('admin@aeromiles.com', 'S0001', 'GA'),
('ahmad.rahman@email.com', 'S0002', 'GA'),
('siti.nurhaliza@email.com', 'S0003', 'GA'),
('budi.santoso@email.com', 'S0004', 'QG'),
('dewi.lestari@email.com', 'S0005', 'QG'),
('eka.putra@email.com', 'S0006', 'JT'),
('farah.yasmin@email.com', 'S0007', 'JT'),
('gunawan.setia@email.com', 'S0008', 'SJ'),
('hana.widya@email.com', 'S0009', 'SJ'),
('indra.kusuma@email.com', 'S0010', 'ID'),
('jaka.sinopati@email.com', 'S0011', 'ID');
SELECT setval('staf_id_staf_seq', (SELECT COALESCE(MAX(CAST(SUBSTRING(id_staf FROM 2) AS INTEGER)), 1) FROM STAF), true);

CREATE TABLE MITRA (
    email_mitra VARCHAR(100) PRIMARY KEY,
    id_penyedia INT NOT NULL UNIQUE REFERENCES PENYEDIA(id) ON DELETE CASCADE,
    nama_mitra VARCHAR(100) NOT NULL,
    tanggal_kerja_sama DATE NOT NULL
);

INSERT INTO MITRA (email_mitra, id_penyedia, nama_mitra, tanggal_kerja_sama) VALUES
('hotelplus@aeromiles.id', 6, 'Hotel Plus Indonesia', '2023-01-15'),
('travelmart@aeromiles.id', 7, 'Travel Mart Asia', '2023-03-20'),
('foodies@aeromiles.id', 8, 'Foodies Reward', '2023-06-10'),
('shopindo@aeromiles.id', 9, 'ShopIndo Voucher', '2024-01-05'),
('rentcar@aeromiles.id', 10, 'RentCar Nusantara', '2024-02-12');

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

CREATE TABLE JENIS_IDENTITAS (
    nama VARCHAR(30) PRIMARY KEY,
    urutan INT NOT NULL UNIQUE
);

INSERT INTO JENIS_IDENTITAS (nama, urutan) VALUES
('Paspor', 1),
('KTP', 2),
('SIM', 3);

CREATE TABLE IDENTITAS (
    nomor VARCHAR(50) PRIMARY KEY,
    email_member VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    tanggal_habis DATE NOT NULL,
    tanggal_terbit DATE NOT NULL,
    CHECK (tanggal_terbit < tanggal_habis),
    negara_penerbit VARCHAR(50) NOT NULL,
    jenis VARCHAR(30) NOT NULL REFERENCES JENIS_IDENTITAS(nama)
);

INSERT INTO IDENTITAS (nomor, email_member, tanggal_habis, tanggal_terbit, negara_penerbit, jenis) VALUES
('P-0001-AERO', 'john@example.com', '2030-01-15', '2024-01-15', 'Indonesia', 'Paspor'),
('P-0002-AERO', 'karina.salsabila@email.com', '2030-01-20', '2024-01-20', 'Indonesia', 'Paspor'),
('KTP-0003-AERO', 'luthfi.akbar@email.com', '2030-02-20', '2024-02-20', 'Indonesia', 'KTP'),
('SIM-0004-AERO', 'maya.handoko@email.com', '2030-03-20', '2024-03-20', 'Indonesia', 'SIM'),
('P-0005-AERO', 'nanda.pratama@email.com', '2030-04-20', '2024-04-20', 'Indonesia', 'Paspor'),
('KTP-0006-AERO', 'only.wijaya@email.com', '2030-05-20', '2024-05-20', 'Indonesia', 'KTP'),
('SIM-0007-AERO', 'prima.sakti@email.com', '2030-06-20', '2024-06-20', 'Indonesia', 'SIM'),
('P-0008-AERO', 'qiana.sofia@email.com', '2030-07-20', '2024-07-20', 'Indonesia', 'Paspor'),
('KTP-0009-AERO', 'ridha.maulana@email.com', '2030-08-20', '2024-08-20', 'Indonesia', 'KTP'),
('SIM-0010-AERO', 'sinta.kusuma@email.com', '2030-09-20', '2024-09-20', 'Indonesia', 'SIM'),
('P-0011-AERO', 'taufik.mulya@email.com', '2030-10-20', '2024-10-20', 'Indonesia', 'Paspor'),
('KTP-0012-AERO', 'ulfa.rahmawati@email.com', '2030-11-20', '2024-11-20', 'Indonesia', 'KTP'),
('SIM-0013-AERO', 'viki.pratama@email.com', '2030-12-20', '2024-12-20', 'Indonesia', 'SIM'),
('P-0014-AERO', 'wulan.sari@email.com', '2030-01-20', '2024-01-20', 'Indonesia', 'Paspor'),
('KTP-0015-AERO', 'xandra.bella@email.com', '2030-02-20', '2024-02-20', 'Indonesia', 'KTP'),
('SIM-0016-AERO', 'yanto.setiadi@email.com', '2030-03-20', '2024-03-20', 'Indonesia', 'SIM'),
('P-0017-AERO', 'zara.aulia@email.com', '2030-04-20', '2024-04-20', 'Indonesia', 'Paspor'),
('KTP-0018-AERO', 'aldi.wijaya@email.com', '2030-05-20', '2024-05-20', 'Indonesia', 'KTP'),
('SIM-0019-AERO', 'andi.hermawan@email.com', '2030-06-20', '2024-06-20', 'Indonesia', 'SIM'),
('P-0020-AERO', 'anita.bulan@email.com', '2030-07-20', '2024-07-20', 'Indonesia', 'Paspor'),
('KTP-0021-AERO', 'bambang.irawan@email.com', '2030-08-20', '2024-08-20', 'Indonesia', 'KTP'),
('SIM-0022-AERO', 'bella.rosita@email.com', '2030-09-20', '2024-09-20', 'Indonesia', 'SIM'),
('P-0023-AERO', 'citra.dewi@email.com', '2030-10-20', '2024-10-20', 'Indonesia', 'Paspor'),
('KTP-0024-AERO', 'danny.wijaya@email.com', '2030-11-20', '2024-11-20', 'Indonesia', 'KTP'),
('SIM-0025-AERO', 'endang.sari@email.com', '2030-12-20', '2024-12-20', 'Indonesia', 'SIM'),
('P-0026-AERO', 'febri.agustin@email.com', '2030-01-20', '2024-01-20', 'Indonesia', 'Paspor'),
('KTP-0027-AERO', 'gerry.wijaya@email.com', '2030-02-20', '2024-02-20', 'Indonesia', 'KTP'),
('SIM-0028-AERO', 'hendra.yanto@email.com', '2030-03-20', '2024-03-20', 'Indonesia', 'SIM'),
('P-0029-AERO', 'irene.santoso@email.com', '2030-04-20', '2024-04-20', 'Indonesia', 'Paspor'),
('KTP-0030-AERO', 'joko.setiawan@email.com', '2030-05-20', '2024-05-20', 'Indonesia', 'KTP');

CREATE TABLE AWARD_MILES_PACKAGE (
    id VARCHAR(20) PRIMARY KEY DEFAULT generate_prefixed_id('award_miles_package_id_seq'::regclass, 'award_miles_package', 'id', 'AMP-', 3),
    harga_paket DECIMAL(15,2) NOT NULL,
    jumlah_award_miles INT NOT NULL
);

INSERT INTO AWARD_MILES_PACKAGE (id, harga_paket, jumlah_award_miles) VALUES
('AMP-001', 150000.00, 1000),
('AMP-002', 650000.00, 5000),
('AMP-003', 1200000.00, 10000),
('AMP-004', 2750000.00, 25000),
('AMP-005', 5000000.00, 50000);
SELECT setval('award_miles_package_id_seq', (SELECT COALESCE(MAX(CAST(SUBSTRING(id FROM 5) AS INTEGER)), 1) FROM AWARD_MILES_PACKAGE), true);

CREATE TABLE MEMBER_AWARD_MILES_PACKAGE (
    id_award_miles_package VARCHAR(20) NOT NULL REFERENCES AWARD_MILES_PACKAGE(id),
    email_member VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (id_award_miles_package, email_member, timestamp)
);

INSERT INTO MEMBER_AWARD_MILES_PACKAGE (id_award_miles_package, email_member, timestamp) VALUES
('AMP-001', 'john@example.com', '2024-01-01 08:00:00'),
('AMP-001', 'karina.salsabila@email.com', '2024-01-02 08:00:00'),
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
('AMP-004', 'anita.bulan@email.com', '2024-04-13 16:00:00');

CREATE TABLE CLAIM_MISSING_MILES (
    id SERIAL PRIMARY KEY,
    email_member VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    email_staf VARCHAR(100) NULL REFERENCES STAF(email),
    maskapai VARCHAR(10) NOT NULL REFERENCES MASKAPAI(kode_maskapai),
    bandara_asal CHAR(3) NOT NULL REFERENCES BANDARA(iata_code),
    bandara_tujuan CHAR(3) NOT NULL REFERENCES BANDARA(iata_code),
    tanggal_penerbangan DATE NOT NULL CHECK (tanggal_penerbangan <= CURRENT_DATE),
    flight_number VARCHAR(10) NOT NULL,
    nomor_tiket VARCHAR(20) NOT NULL,
    kelas_kabin VARCHAR(20) NOT NULL CHECK (kelas_kabin IN ('Economy', 'Business', 'First')),
    pnr VARCHAR(10) NOT NULL,
    status_penerimaan VARCHAR(20) NOT NULL DEFAULT 'Menunggu' CHECK (status_penerimaan IN ('Menunggu', 'Disetujui', 'Ditolak')),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_claim_no_duplicate UNIQUE (email_member, flight_number, tanggal_penerbangan, nomor_tiket)
);

-- Data awal klaim dirancang konsisten dengan tier member.
-- approved_claims mengikuti minimal_frekuensi_terbang tier awal:
-- Bronze 0, Silver 5, Gold 15, Diamond 30.
-- Beberapa klaim Menunggu/Ditolak tetap disediakan untuk skenario staf.
-- Trigger TK04 dipasang setelah dump TK03, sehingga data historis ini
-- tidak mengubah award_miles/total_miles yang sudah ditentukan.
WITH claim_seed_plan(email_member, approved_claims, member_idx) AS (
    VALUES
    ('john@example.com', 15, 1),
    ('karina.salsabila@email.com', 30, 2),
    ('luthfi.akbar@email.com', 15, 3),
    ('maya.handoko@email.com', 15, 4),
    ('nanda.pratama@email.com', 5, 5),
    ('only.wijaya@email.com', 5, 6),
    ('prima.sakti@email.com', 1, 7),
    ('qiana.sofia@email.com', 1, 8),
    ('ridha.maulana@email.com', 5, 9),
    ('sinta.kusuma@email.com', 15, 10),
    ('taufik.mulya@email.com', 30, 11),
    ('ulfa.rahmawati@email.com', 30, 12),
    ('viki.pratama@email.com', 15, 13),
    ('wulan.sari@email.com', 15, 14),
    ('xandra.bella@email.com', 5, 15),
    ('yanto.setiadi@email.com', 5, 16),
    ('zara.aulia@email.com', 0, 17),
    ('aldi.wijaya@email.com', 0, 18),
    ('andi.hermawan@email.com', 5, 19),
    ('anita.bulan@email.com', 15, 20),
    ('bambang.irawan@email.com', 30, 21),
    ('bella.rosita@email.com', 30, 22),
    ('citra.dewi@email.com', 15, 23),
    ('danny.wijaya@email.com', 15, 24),
    ('endang.sari@email.com', 5, 25),
    ('febri.agustin@email.com', 5, 26),
    ('gerry.wijaya@email.com', 0, 27),
    ('hendra.yanto@email.com', 0, 28),
    ('irene.santoso@email.com', 5, 29),
    ('joko.setiawan@email.com', 15, 30),
    ('kartika.wijaya@email.com', 30, 31),
    ('lina.marliana@email.com', 30, 32),
    ('meldy.santoso@email.com', 15, 33),
    ('novi.kusuma@email.com', 15, 34),
    ('otis.wijaya@email.com', 5, 35),
    ('pasha.kusuma@email.com', 5, 36),
    ('qori.yusuf@email.com', 0, 37),
    ('ratna.wijaya@email.com', 0, 38),
    ('saiful.anwar@email.com', 5, 39),
    ('tania.bella@email.com', 15, 40),
    ('udang.haryo@email.com', 30, 41),
    ('vanessa.dewi@email.com', 30, 42),
    ('wahyu.sanusi@email.com', 15, 43),
    ('xena.wijaya@email.com', 15, 44),
    ('yuki.suzuki@email.com', 5, 45),
    ('zulfikar.fahmi@email.com', 5, 46),
    ('adriana.putri@email.com', 0, 47),
    ('arif.kusuma@email.com', 0, 48),
    ('astrid.murni@email.com', 5, 49),
    ('aziz.irfandi@email.com', 15, 50),
    ('ayu.citra@email.com', 30, 51)
),
approved_claims AS (
    SELECT
        plan.email_member, plan.member_idx, gs.n, 'Disetujui'::VARCHAR(20) AS status_penerimaan,
        'admin@aeromiles.com'::VARCHAR(100) AS email_staf,
        (DATE '2025-01-01' + ((plan.member_idx * 31 + gs.n) % 300)) AS flight_date,
        'AP'::TEXT AS claim_prefix
    FROM claim_seed_plan plan
    CROSS JOIN LATERAL generate_series(1, plan.approved_claims) AS gs(n)
),
pending_claims(email_member, member_idx, n) AS (
    VALUES
    ('john@example.com', 1, 1),
    ('wulan.sari@email.com', 14, 1),
    ('xandra.bella@email.com', 15, 1),
    ('yanto.setiadi@email.com', 16, 1),
    ('zara.aulia@email.com', 17, 1),
    ('aldi.wijaya@email.com', 18, 1),
    ('andi.hermawan@email.com', 19, 1)
),
rejected_claims(email_member, member_idx, n) AS (
    VALUES
    ('ridha.maulana@email.com', 9, 1),
    ('sinta.kusuma@email.com', 10, 1),
    ('taufik.mulya@email.com', 11, 1),
    ('ulfa.rahmawati@email.com', 12, 1),
    ('viki.pratama@email.com', 13, 1)
),
all_claims AS (
    SELECT * FROM approved_claims
    UNION ALL
    SELECT
        email_member, member_idx, n, 'Menunggu'::VARCHAR(20), NULL::VARCHAR(100),
        (DATE '2025-11-01' + member_idx) AS flight_date, 'PN'::TEXT AS claim_prefix
    FROM pending_claims
    UNION ALL
    SELECT
        email_member, member_idx, n, 'Ditolak'::VARCHAR(20), 'admin@aeromiles.com'::VARCHAR(100),
        (DATE '2025-12-01' + member_idx) AS flight_date, 'RJ'::TEXT AS claim_prefix
    FROM rejected_claims
)
INSERT INTO CLAIM_MISSING_MILES (
    email_member, email_staf, maskapai, bandara_asal, bandara_tujuan,
    tanggal_penerbangan, flight_number, nomor_tiket, kelas_kabin, pnr,
    status_penerimaan, timestamp
)
SELECT
    email_member,
    email_staf,
    CASE member_idx % 3 WHEN 0 THEN 'GA' WHEN 1 THEN 'QG' ELSE 'JT' END,
    CASE member_idx % 4 WHEN 0 THEN 'CGK' WHEN 1 THEN 'DPS' WHEN 2 THEN 'SUB' ELSE 'JOG' END,
    CASE member_idx % 4 WHEN 0 THEN 'DPS' WHEN 1 THEN 'CGK' WHEN 2 THEN 'JOG' ELSE 'SUB' END,
    flight_date,
    claim_prefix || LPAD(member_idx::text, 3, '0') || LPAD(n::text, 2, '0'),
    'TK4-' || claim_prefix || '-' || LPAD(member_idx::text, 3, '0') || '-' || LPAD(n::text, 2, '0'),
    CASE n % 3 WHEN 0 THEN 'Business' WHEN 1 THEN 'Economy' ELSE 'First' END,
    claim_prefix || LPAD(member_idx::text, 3, '0') || LPAD(n::text, 2, '0'),
    status_penerimaan,
    flight_date::timestamp + TIME '10:00:00'
FROM all_claims;

CREATE TABLE TRANSFER (
    email_member_1 VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    email_member_2 VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    jumlah INT NOT NULL CHECK (jumlah > 0),
    catatan VARCHAR(255),
    PRIMARY KEY (email_member_1, email_member_2, timestamp),
    CHECK (email_member_1 <> email_member_2)
);

INSERT INTO TRANSFER (email_member_1, email_member_2, timestamp, jumlah, catatan) VALUES
('john@example.com', 'karina.salsabila@email.com', '2025-01-15 10:30:00', 5000, 'Transfer miles #1'),
('karina.salsabila@email.com', 'luthfi.akbar@email.com', '2024-06-01 09:30:00', 500, 'Transfer miles #2'),
('luthfi.akbar@email.com', 'maya.handoko@email.com', '2024-06-02 10:30:00', 650, 'Transfer miles #3'),
('maya.handoko@email.com', 'nanda.pratama@email.com', '2024-06-03 11:30:00', 800, 'Transfer miles #4'),
('nanda.pratama@email.com', 'only.wijaya@email.com', '2024-06-04 12:30:00', 950, 'Transfer miles #5'),
('only.wijaya@email.com', 'prima.sakti@email.com', '2024-06-05 13:30:00', 1100, 'Transfer miles #6'),
('prima.sakti@email.com', 'qiana.sofia@email.com', '2024-06-06 14:30:00', 1250, 'Transfer miles #7'),
('qiana.sofia@email.com', 'ridha.maulana@email.com', '2024-06-07 15:30:00', 1400, 'Transfer miles #8'),
('ridha.maulana@email.com', 'sinta.kusuma@email.com', '2024-06-08 16:30:00', 1550, 'Transfer miles #9'),
('sinta.kusuma@email.com', 'taufik.mulya@email.com', '2024-06-09 17:30:00', 1700, 'Transfer miles #10'),
('taufik.mulya@email.com', 'ulfa.rahmawati@email.com', '2024-06-10 18:30:00', 1850, 'Transfer miles #11'),
('ulfa.rahmawati@email.com', 'viki.pratama@email.com', '2024-06-11 09:30:00', 2000, 'Transfer miles #12'),
('viki.pratama@email.com', 'wulan.sari@email.com', '2024-06-12 10:30:00', 2150, 'Transfer miles #13'),
('wulan.sari@email.com', 'xandra.bella@email.com', '2024-06-13 11:30:00', 2300, 'Transfer miles #14'),
('xandra.bella@email.com', 'yanto.setiadi@email.com', '2024-06-14 12:30:00', 2450, 'Transfer miles #15');

CREATE TABLE HADIAH (
    kode_hadiah VARCHAR(20) PRIMARY KEY DEFAULT generate_prefixed_id('hadiah_kode_hadiah_seq'::regclass, 'hadiah', 'kode_hadiah', 'RWD-', 3),
    nama VARCHAR(100) NOT NULL,
    miles INT NOT NULL,
    deskripsi TEXT,
    valid_start_date DATE NOT NULL,
    program_end DATE NOT NULL,
    CHECK (program_end > valid_start_date),
    id_penyedia INT NOT NULL REFERENCES PENYEDIA(id) ON DELETE CASCADE
);

INSERT INTO HADIAH (kode_hadiah, nama, miles, deskripsi, valid_start_date, program_end, id_penyedia) VALUES
('RWD-001', 'Upgrade Business Class', 15000, 'Upgrade kursi ke Business Class.', '2024-01-01', '2026-12-31', 1),
('RWD-002', 'Extra Baggage 20kg', 8000, 'Tambahan bagasi sebesar 20kg.', '2024-01-01', '2026-12-31', 1),
('RWD-003', 'Airport Lounge Access', 12000, 'Akses lounge bandara internasional.', '2024-01-01', '2026-12-31', 2),
('RWD-004', 'Hotel Voucher Rp500.000', 10000, 'Voucher menginap di Hotel Plus.', '2024-01-01', '2026-12-31', 6),
('RWD-005', 'Travel Voucher Rp300.000', 7000, 'Voucher pembelian tiket di Travel Mart.', '2024-01-01', '2026-12-31', 7),
('RWD-006', 'Dining Voucher Rp250.000', 6000, 'Voucher makan di merchant Foodies.', '2024-01-01', '2026-12-31', 8),
('RWD-007', 'Shopping Voucher Rp400.000', 9000, 'Voucher belanja di ShopIndo.', '2024-01-01', '2026-12-31', 9),
('RWD-008', 'Car Rental Discount', 11000, 'Diskon sewa mobil dari RentCar Nusantara.', '2024-01-01', '2026-12-31', 10),
('RWD-009', 'Priority Boarding', 5000, 'Fasilitas naik pesawat lebih awal.', '2024-01-01', '2026-12-31', 3),
('RWD-010', 'Free Seat Selection', 4000, 'Bebas memilih kursi penerbangan.', '2024-01-01', '2026-12-31', 2);
SELECT setval('hadiah_kode_hadiah_seq', (SELECT COALESCE(MAX(CAST(SUBSTRING(kode_hadiah FROM 5) AS INTEGER)), 1) FROM HADIAH), true);

CREATE TABLE REDEEM (
    email_member VARCHAR(100) NOT NULL REFERENCES MEMBER(email) ON DELETE CASCADE,
    kode_hadiah VARCHAR(20) NOT NULL REFERENCES HADIAH(kode_hadiah),
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (email_member, kode_hadiah, timestamp)
);

INSERT INTO REDEEM (email_member, kode_hadiah, timestamp) VALUES
('john@example.com', 'RWD-003', '2025-01-20 16:00:00'),
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
('anita.bulan@email.com', 'RWD-009', '2024-08-19 18:00:00');
