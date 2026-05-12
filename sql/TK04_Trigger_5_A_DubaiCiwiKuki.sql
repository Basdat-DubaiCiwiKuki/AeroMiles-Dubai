-- ============================================================
-- TK04 - TRIGGER NOMOR 5
-- ============================================================
-- 5.1 Sinkronisasi Total Miles Member setelah Klaim Missing
--     Miles Disetujui
-- 5.2 Pemeringkatan Top 5 Member berdasarkan Total Miles
-- ============================================================
--
-- Asumsi skema mengikuti TK03 kelompok Dubai:
--   - MEMBER(email, award_miles, total_miles, ...)
--   - PENGGUNA(email, first_mid_name, last_name, ...)
--   - CLAIM_MISSING_MILES(email_member, flight_number,
--     status_penerimaan, ...)
--
-- INFORMASI:
--   - total_miles adalah total akumulasi miles dan ikut bertambah
--     ketika klaim missing miles disetujui.
--   - award_miles adalah saldo aktif dan juga ikut bertambah ketika
--     klaim missing miles disetujui.
-- ============================================================


-- ============================================================
-- TRIGGER 5.1: Sinkronisasi Miles setelah Klaim Disetujui
-- ============================================================
-- Dijalankan setelah staf mengubah status klaim menjadi 'Disetujui'.
-- Setiap klaim yang baru berubah menjadi Disetujui menambahkan
-- 1000 miles ke award_miles dan total_miles member terkait.

CREATE OR REPLACE FUNCTION fn_sinkron_miles_klaim_disetujui()
RETURNS TRIGGER AS $$
DECLARE
    v_miles_klaim CONSTANT INT := 1000;
BEGIN
    IF NEW.status_penerimaan = 'Disetujui'
       AND OLD.status_penerimaan IS DISTINCT FROM 'Disetujui' THEN

        UPDATE MEMBER
           SET award_miles = award_miles + v_miles_klaim,
               total_miles = total_miles + v_miles_klaim
         WHERE email = NEW.email_member;

        IF NOT FOUND THEN
            RAISE EXCEPTION
                'ERROR: Member dengan email "%" tidak ditemukan.',
                NEW.email_member;
        END IF;

        RAISE NOTICE
            'SUKSES: Total miles Member "%" telah diperbarui. Miles ditambahkan: % miles dari klaim penerbangan "%".',
            NEW.email_member,
            v_miles_klaim,
            NEW.flight_number;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_sinkron_miles_klaim_disetujui
    ON CLAIM_MISSING_MILES;

CREATE TRIGGER trg_sinkron_miles_klaim_disetujui
AFTER UPDATE OF status_penerimaan ON CLAIM_MISSING_MILES
FOR EACH ROW
EXECUTE FUNCTION fn_sinkron_miles_klaim_disetujui();


-- ============================================================
-- STORED FUNCTION 5.2: Top 5 Member berdasarkan Total Miles
-- ============================================================
-- Dipanggil oleh halaman laporan transaksi staf:
--   SELECT * FROM get_top5_member_by_miles();
--
-- Kolom pertama sampai ketiga dipertahankan sesuai views.py:
--   email, nama, total_miles
-- Kolom pesan ditambahkan agar pesan sukses berasal dari database.

DROP FUNCTION IF EXISTS get_top5_member_by_miles();

CREATE OR REPLACE FUNCTION get_top5_member_by_miles()
RETURNS TABLE (
    email VARCHAR(100),
    nama TEXT,
    total_miles INT,
    pesan TEXT
) AS $$
DECLARE
    v_email_pertama VARCHAR(100);
    v_total_pertama INT;
    v_pesan TEXT;
BEGIN
    SELECT m.email, m.total_miles
      INTO v_email_pertama, v_total_pertama
      FROM MEMBER m
     ORDER BY m.total_miles DESC, m.email ASC
     LIMIT 1;

    IF v_email_pertama IS NULL THEN
        v_pesan := 'SUKSES: Daftar Top 5 Member berdasarkan total miles berhasil diperbarui, namun belum ada member terdaftar.';
    ELSE
        v_pesan := FORMAT(
            'SUKSES: Daftar Top 5 Member berdasarkan total miles berhasil diperbarui, dengan peringkat pertama "%s" memiliki %s miles.',
            v_email_pertama,
            v_total_pertama
        );
    END IF;

    RAISE NOTICE '%', v_pesan;

    RETURN QUERY
    SELECT m.email,
           TRIM(CONCAT_WS(' ', p.first_mid_name, p.last_name)) AS nama,
           m.total_miles,
           v_pesan AS pesan
      FROM MEMBER m
      JOIN PENGGUNA p ON p.email = m.email
     ORDER BY m.total_miles DESC, m.email ASC
     LIMIT 5;
END;
$$ LANGUAGE plpgsql;
