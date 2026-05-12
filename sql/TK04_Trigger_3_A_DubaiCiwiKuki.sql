CREATE OR REPLACE FUNCTION fn_validasi_redeem_hadiah()
RETURNS TRIGGER AS $$
DECLARE
    v_saldo         INT;
    v_miles_hadiah  INT;
    v_nama_hadiah   VARCHAR(100);
    v_start_date    DATE;
    v_end_date      DATE;
    v_tanggal_now   DATE;
BEGIN
    -- 1. Ambil data hadiah
    SELECT nama, miles, valid_start_date, program_end
      INTO v_nama_hadiah, v_miles_hadiah, v_start_date, v_end_date
      FROM HADIAH
     WHERE kode_hadiah = NEW.kode_hadiah;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'ERROR: Hadiah dengan kode "%" tidak ditemukan.',
            NEW.kode_hadiah;
    END IF;

    -- 2. Validasi periode aktif hadiah
    v_tanggal_now := DATE(NEW.timestamp);
    IF v_tanggal_now < v_start_date OR v_tanggal_now > v_end_date THEN
        RAISE EXCEPTION 'ERROR: Hadiah "%" tidak tersedia pada periode ini.',
            v_nama_hadiah;
    END IF;

    -- 3. Ambil saldo award_miles member
    SELECT award_miles
      INTO v_saldo
      FROM MEMBER
     WHERE email = NEW.email_member;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'ERROR: Member dengan email "%" tidak ditemukan.',
            NEW.email_member;
    END IF;

    -- 4. Validasi kecukupan saldo
    IF v_saldo < v_miles_hadiah THEN
        RAISE EXCEPTION
            'ERROR: Saldo award miles tidak mencukupi. Dibutuhkan % miles, saldo Anda: % miles.',
            v_miles_hadiah, v_saldo;
    END IF;

    -- 5. Kurangi award_miles (total_miles TIDAK berubah)
    UPDATE MEMBER
       SET award_miles = award_miles - v_miles_hadiah
     WHERE email = NEW.email_member;

    -- 6. Pesan sukses
    RAISE NOTICE
        'SUKSES: Redeem hadiah "%" berhasil. Award miles Anda berkurang % miles.',
        v_nama_hadiah, v_miles_hadiah;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validasi_redeem_hadiah ON REDEEM;

CREATE TRIGGER trg_validasi_redeem_hadiah
BEFORE INSERT ON REDEEM
FOR EACH ROW
EXECUTE FUNCTION fn_validasi_redeem_hadiah();

CREATE OR REPLACE FUNCTION fn_sinkron_pembelian_package()
RETURNS TRIGGER AS $$
DECLARE
    v_jumlah_award_miles INT;
BEGIN
    -- Ambil jumlah award_miles dari paket
    SELECT jumlah_award_miles
      INTO v_jumlah_award_miles
      FROM AWARD_MILES_PACKAGE
     WHERE id = NEW.id_award_miles_package;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'ERROR: Paket dengan ID "%" tidak ditemukan.',
            NEW.id_award_miles_package;
    END IF;

    UPDATE MEMBER
       SET award_miles = award_miles + v_jumlah_award_miles,
           total_miles = total_miles + v_jumlah_award_miles
     WHERE email = NEW.email_member;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'ERROR: Member dengan email "%" tidak ditemukan.',
            NEW.email_member;
    END IF;

    RAISE NOTICE
        'SUKSES: Pembelian package berhasil. Award miles dan total miles Anda bertambah % miles.',
        v_jumlah_award_miles;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_sinkron_pembelian_package
    ON MEMBER_AWARD_MILES_PACKAGE;

CREATE TRIGGER trg_sinkron_pembelian_package
AFTER INSERT ON MEMBER_AWARD_MILES_PACKAGE
FOR EACH ROW
EXECUTE FUNCTION fn_sinkron_pembelian_package();