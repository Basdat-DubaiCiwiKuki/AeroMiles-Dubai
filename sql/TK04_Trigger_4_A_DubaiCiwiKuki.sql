-- ============================================================
-- TK04 - TRIGGER NOMOR 4
-- ============================================================
-- 4.1 Pemeriksaan Status Klaim Missing Miles yang Duplikat
-- 4.2 Pembaruan Tier Member secara Otomatis berdasarkan Total Miles
-- ============================================================


-- ============================================================
-- TRIGGER 4.1: Pencegahan Duplikasi Klaim Missing Miles
-- ============================================================
-- Mengecek apakah sudah ada klaim dengan kombinasi yang sama:
--   email_member + flight_number + tanggal_penerbangan + nomor_tiket
-- Status apapun (Menunggu/Disetujui/Ditolak) dianggap duplikat.

CREATE OR REPLACE FUNCTION fn_cek_duplikasi_klaim()
RETURNS TRIGGER AS $$
DECLARE
    v_existing_count INT;
BEGIN
    IF TG_OP = 'UPDATE' THEN
        SELECT COUNT(*) INTO v_existing_count
        FROM claim_missing_miles
        WHERE email_member        = NEW.email_member
          AND flight_number       = NEW.flight_number
          AND tanggal_penerbangan = NEW.tanggal_penerbangan
          AND nomor_tiket         = NEW.nomor_tiket
          AND id                 != NEW.id;
    ELSE
        SELECT COUNT(*) INTO v_existing_count
        FROM claim_missing_miles
        WHERE email_member        = NEW.email_member
          AND flight_number       = NEW.flight_number
          AND tanggal_penerbangan = NEW.tanggal_penerbangan
          AND nomor_tiket         = NEW.nomor_tiket;
    END IF;

    IF v_existing_count > 0 THEN
        RAISE EXCEPTION
            'ERROR: Klaim untuk penerbangan "%" pada tanggal "%" dengan nomor tiket "%" sudah pernah diajukan sebelumnya.',
            NEW.flight_number,
            TO_CHAR(NEW.tanggal_penerbangan, 'YYYY-MM-DD'),
            NEW.nomor_tiket;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_cek_duplikasi_klaim_insert ON claim_missing_miles;
DROP TRIGGER IF EXISTS trg_cek_duplikasi_klaim_update ON claim_missing_miles;

CREATE TRIGGER trg_cek_duplikasi_klaim_insert
    BEFORE INSERT ON claim_missing_miles
    FOR EACH ROW
    EXECUTE FUNCTION fn_cek_duplikasi_klaim();

CREATE TRIGGER trg_cek_duplikasi_klaim_update
    BEFORE UPDATE OF flight_number, tanggal_penerbangan, nomor_tiket
    ON claim_missing_miles
    FOR EACH ROW
    EXECUTE FUNCTION fn_cek_duplikasi_klaim();


-- ============================================================
-- TRIGGER 4.2: Pembaruan Tier Member Otomatis berdasarkan Total Miles
-- ============================================================
-- Dijalankan setiap kali total_miles member berubah (AFTER UPDATE).
-- Perubahan total_miles dapat terjadi akibat:
--   - Klaim missing miles disetujui
--   - Pembelian Award Miles Package
--   - Penerimaan transfer miles dari member lain
--
-- Logika penentuan tier:
--   Tier terbaik = tier dengan minimal_tier_miles <= total_miles
--                  DAN minimal_frekuensi_terbang <= jumlah klaim disetujui,
--                  diambil yang nilai minimal_tier_miles-nya paling tinggi.

CREATE OR REPLACE FUNCTION fn_update_tier_member()
RETURNS TRIGGER AS $$
DECLARE
    v_tier_baru_id      VARCHAR(10);
    v_tier_baru_nama    VARCHAR(50);
    v_tier_lama_nama    VARCHAR(50);
    v_frekuensi_terbang INT;
BEGIN
    -- Hanya proses jika total_miles benar-benar berubah
    IF NEW.total_miles = OLD.total_miles THEN
        RETURN NEW;
    END IF;

    -- Hitung frekuensi terbang: jumlah klaim yang sudah Disetujui
    SELECT COUNT(*) INTO v_frekuensi_terbang
    FROM claim_missing_miles
    WHERE email_member    = NEW.email
      AND status_penerimaan = 'Disetujui';

    -- Ambil tier terbaik yang memenuhi kedua syarat:
    --   1. total_miles >= minimal_tier_miles
    --   2. frekuensi_terbang >= minimal_frekuensi_terbang
    SELECT id_tier, nama
      INTO v_tier_baru_id, v_tier_baru_nama
      FROM tier
     WHERE minimal_tier_miles        <= NEW.total_miles
       AND minimal_frekuensi_terbang <= v_frekuensi_terbang
     ORDER BY minimal_tier_miles DESC
     LIMIT 1;

    -- Jika tidak ada tier yang cocok, fallback ke tier terendah (Bronze)
    IF NOT FOUND THEN
        SELECT id_tier, nama
          INTO v_tier_baru_id, v_tier_baru_nama
          FROM tier
         ORDER BY minimal_tier_miles ASC
         LIMIT 1;
    END IF;

    -- Ambil nama tier lama untuk pesan sukses
    SELECT t.nama INTO v_tier_lama_nama
      FROM tier t
     WHERE t.id_tier = OLD.id_tier;

    -- Hanya update dan tampilkan pesan jika tier benar-benar berubah
    IF v_tier_baru_id IS DISTINCT FROM OLD.id_tier THEN
        UPDATE member
           SET id_tier = v_tier_baru_id
         WHERE email = NEW.email;

        RAISE NOTICE
            'SUKSES: Tier Member "%" telah diperbarui dari "%" menjadi "%" berdasarkan total miles yang dimiliki.',
            NEW.email,
            v_tier_lama_nama,
            v_tier_baru_nama;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_tier_member ON member;

CREATE TRIGGER trg_update_tier_member
    AFTER UPDATE OF total_miles ON member
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_tier_member();