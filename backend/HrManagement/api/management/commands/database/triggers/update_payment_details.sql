-- Função trigger
CREATE OR REPLACE FUNCTION update_payment_totals()
RETURNS TRIGGER AS $$
DECLARE
    base_salary NUMERIC(10, 2) := 0;
BEGIN
    -- deductions
    UPDATE deductions
    SET id_payment = NEW.id_payment
    FROM absence_reason
    WHERE deductions.id_absence_reason = absence_reason.id_absence_reason
      AND id_employee = NEW.id_employee
      AND deduction_date = NEW.payment_date;

    -- bonuses
    UPDATE bonuses
    SET id_payment = NEW.id_payment
    WHERE id_employee = NEW.id_employee
      AND bonus_date = NEW.payment_date;

    -- deduções e bônus relacionados ao pagamento
    SELECT COALESCE(SUM(deductions.amount), 0) INTO NEW.deduction_amount
    FROM deductions
    INNER JOIN absence_reason ON deductions.id_absence_reason = absence_reason.id_absence_reason
    WHERE
        absence_reason.id_employee = NEW.id_employee
        AND deductions.deduction_date = NEW.payment_date;

    SELECT COALESCE(SUM(b.amount), 0) INTO NEW.bonus_amount
    FROM bonuses b
    WHERE
        b.id_employee = NEW.id_employee
        AND b.bonus_date = NEW.payment_date;

    -- base salary
    SELECT COALESCE(latest_salary_materialized_view.base_salary, 0) INTO base_salary FROM latest_salary_materialized_view
    INNER JOIN contract ON contract.id_contract = latest_salary_materialized_view.id_contract
    INNER JOIN employees ON employees.id_employee = contract.id_employee
    WHERE employees.id_employee = NEW.id_employee
    LIMIT 1;


    NEW.amount = base_salary
               + COALESCE(NEW.extra_amount, 0)
               + COALESCE(NEW.bonus_amount, 0)
               - COALESCE(NEW.deduction_amount, 0);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que chama a função na inserção de pagamentos
CREATE OR REPLACE TRIGGER trg_update_payment_totals
AFTER INSERT ON payments
FOR EACH ROW
EXECUTE FUNCTION update_payment_totals();