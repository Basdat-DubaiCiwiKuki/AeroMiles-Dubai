-- ============================================================
-- TK04 TRIGGER 2 - TRANSFER MILES
-- 1. Pencegahan Transfer Miles Melebihi Saldo
-- 2. Pencatatan Log Riwayat Transfer Miles
-- ============================================================
--
-- Asumsi skema mengikuti TK03 kelompok Dubai:
--   - MEMBER(email, award_miles, total_miles, ...)
--   - TRANSFER(email_member_1, email_member_2, timestamp, jumlah, catatan)
--
-- Alur fitur:
--   1. Member membuat baris baru pada tabel TRANSFER.
--   2. Trigger memvalidasi pengirim dan penerima berbeda.
--   3. Trigger memvalidasi saldo award_miles pengirim cukup.
--   4. Jika valid, baris TRANSFER menjadi log riwayat transaksi.
--   5. award_miles pengirim berkurang.
--   6. award_miles dan total_miles penerima bertambah.
--   7. Trigger menampilkan pesan sukses/error.
-- ============================================================

CREATE OR REPLACE FUNCTION fn_transfer_miles()
RETURNS TRIGGER AS $$
DECLARE
    v_saldo_pengirim INT;
BEGIN
    -- Jika aplikasi tidak mengirim timestamp, isi otomatis.
    IF NEW.timestamp IS NULL THEN
        NEW.timestamp := CURRENT_TIMESTAMP;
    END IF;

    -- Validasi jumlah transfer.
    IF NEW.jumlah IS NULL OR NEW.jumlah <= 0 THEN
        RAISE EXCEPTION
            'ERROR: Jumlah transfer harus lebih dari 0 miles.';
    END IF;

    -- Validasi sender tidak sama dengan receiver.
    IF LOWER(NEW.email_member_1) = LOWER(NEW.email_member_2) THEN
        RAISE EXCEPTION
            'ERROR: Tidak dapat transfer miles ke diri sendiri.';
    END IF;

    -- Ambil dan kunci saldo pengirim agar transaksi paralel tidak membuat saldo minus.
    SELECT award_miles
      INTO v_saldo_pengirim
      FROM MEMBER
     WHERE email = NEW.email_member_1
     FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION
            'ERROR: Member pengirim dengan email "%" tidak ditemukan.',
            NEW.email_member_1;
    END IF;

    -- Pastikan penerima adalah member yang valid dan kunci row penerima.
    PERFORM 1
      FROM MEMBER
     WHERE email = NEW.email_member_2
     FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION
            'ERROR: Member penerima dengan email "%" tidak ditemukan.',
            NEW.email_member_2;
    END IF;

    -- Validasi saldo award_miles cukup sesuai ketentuan TK04.
    IF v_saldo_pengirim < NEW.jumlah THEN
        RAISE EXCEPTION
            'ERROR: Saldo award miles tidak mencukupi. Saldo Anda saat ini: % miles, jumlah transfer: % miles.',
            v_saldo_pengirim,
            NEW.jumlah;
    END IF;

    -- Kurangi award_miles pengirim.
    UPDATE MEMBER
       SET award_miles = award_miles - NEW.jumlah
     WHERE email = NEW.email_member_1;

    -- Tambah award_miles dan total_miles penerima.
    UPDATE MEMBER
       SET award_miles = award_miles + NEW.jumlah,
           total_miles = total_miles + NEW.jumlah
     WHERE email = NEW.email_member_2;

    -- Baris TRANSFER yang sedang di-insert menjadi log riwayat transfer.
    RAISE NOTICE
        'SUKSES: Transfer % miles dari "%" ke "%" berhasil dicatat.',
        NEW.jumlah,
        NEW.email_member_1,
        NEW.email_member_2;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_transfer_miles ON TRANSFER;

CREATE TRIGGER trg_transfer_miles
BEFORE INSERT ON TRANSFER
FOR EACH ROW
EXECUTE FUNCTION fn_transfer_miles();
