CREATE OR REPLACE FUNCTION prevent_duplicate_salary_history()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM salary_history
        WHERE id_contract = NEW.id_contract
          AND id_employee_aproved_by = NEW.id_employee_aproved_by
          AND base_salary = NEW.base_salary
          AND extra_hour_rate = NEW.extra_hour_rate
          AND start_date = NEW.start_date
    ) THEN
        RAISE NOTICE 'Duplicate entry detected. Insert ignored.';
        RETURN NULL; -- Ignora
    ELSE
        RAISE NOTICE 'No duplicate entry detected. Insert allowed.';
        RETURN NEW; -- Permite
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trigger_prevent_duplicate_salary_history
BEFORE INSERT ON salary_history
FOR EACH ROW
EXECUTE FUNCTION prevent_duplicate_salary_history();
