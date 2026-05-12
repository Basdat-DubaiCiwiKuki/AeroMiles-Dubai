CREATE OR REPLACE FUNCTION check_duplicate_email()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM PENGGUNA
        WHERE LOWER(email) = LOWER(NEW.email)
    ) THEN

        RAISE EXCEPTION
        'ERROR: Email "%" sudah terdaftar, silakan gunakan email lain.',
        NEW.email;

    END IF;

    NEW.email := LOWER(NEW.email);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_check_duplicate_email ON PENGGUNA;
CREATE TRIGGER trg_check_duplicate_email
BEFORE INSERT ON PENGGUNA
FOR EACH ROW
EXECUTE FUNCTION check_duplicate_email();


-- -----------------------------------------------------------
-- STORED FUNCTION 1.2: Verifikasi kredensial login
-- Diimplementasikan sebagai FUNCTION (bukan trigger karena
-- login adalah SELECT, bukan INSERT/UPDATE/DELETE)
-- Dipanggil dari backend Django di views.py
-- -----------------------------------------------------------
CREATE OR REPLACE FUNCTION verify_login(
    p_email VARCHAR(100),
    p_password_hash VARCHAR(255)
)
RETURNS TABLE (
    email VARCHAR(100),
    salutation VARCHAR(10),
    first_mid_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(10),
    success BOOLEAN,
    message TEXT
) AS $$
DECLARE
    v_stored_password VARCHAR(255);
    v_is_staf BOOLEAN := FALSE;
    v_is_member BOOLEAN := FALSE;
BEGIN
    -- Cek apakah email ada (case-insensitive)
    SELECT p.password INTO v_stored_password
    FROM PENGGUNA p
    WHERE LOWER(p.email) = LOWER(p_email);

    IF NOT FOUND THEN
        RETURN QUERY SELECT
            NULL::VARCHAR(100),
            NULL::VARCHAR(10),
            NULL::VARCHAR(100),
            NULL::VARCHAR(100),
            NULL::VARCHAR(10),
            FALSE,
            'Email atau password salah, silakan coba lagi.'::TEXT;
        RETURN;
    END IF;

    -- Cek password
    IF v_stored_password <> p_password_hash THEN
        RETURN QUERY SELECT
            NULL::VARCHAR(100),
            NULL::VARCHAR(10),
            NULL::VARCHAR(100),
            NULL::VARCHAR(100),
            NULL::VARCHAR(10),
            FALSE,
            'Email atau password salah, silakan coba lagi.'::TEXT;
        RETURN;
    END IF;

    -- Tentukan role
    SELECT EXISTS(
        SELECT 1
        FROM STAF s
        WHERE LOWER(s.email) = LOWER(p_email)
    ) INTO v_is_staf;

    SELECT EXISTS(
        SELECT 1
        FROM MEMBER m
        WHERE LOWER(m.email) = LOWER(p_email)
    ) INTO v_is_member;

    -- VALIDASI role
    IF NOT v_is_staf AND NOT v_is_member THEN
        RETURN QUERY SELECT
            NULL::VARCHAR(100),
            NULL::VARCHAR(10),
            NULL::VARCHAR(100),
            NULL::VARCHAR(100),
            NULL::VARCHAR(10),
            FALSE,
            'Akun tidak memiliki role valid.'::TEXT;
        RETURN;
    END IF;

    -- Return data user
    RETURN QUERY
    SELECT
        p.email,
        p.salutation,
        p.first_mid_name,
        p.last_name,
        CASE
            WHEN v_is_staf THEN 'staf'::VARCHAR(10)
            WHEN v_is_member THEN 'member'::VARCHAR(10)
        END,
        TRUE,
        'Login berhasil.'::TEXT
    FROM PENGGUNA p
    WHERE LOWER(p.email) = LOWER(p_email);
END;
$$ LANGUAGE plpgsql;
