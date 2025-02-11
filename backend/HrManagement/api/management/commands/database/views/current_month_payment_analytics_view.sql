CREATE OR REPLACE VIEW current_month_payment_analytics_view AS
WITH current_month_payments AS (
    SELECT
        p.*,
        TO_CHAR(p.payment_date, 'Month') as month_name,
        e.id_auth_user,
        COALESCE(b.amount, 0) as total_bonus,
        COALESCE(d.amount, 0) as total_deduction
    FROM payments p
    LEFT JOIN employees e ON e.id_employee = p.id_employee
    LEFT JOIN (
        SELECT id_payment, SUM(amount) as amount
        FROM bonuses
        WHERE deleted_at IS NULL
        GROUP BY id_payment
    ) b ON b.id_payment = p.id_payment
    LEFT JOIN (
        SELECT id_payment, SUM(amount) as amount
        FROM deductions
        WHERE deleted_at IS NULL
        GROUP BY id_payment
    ) d ON d.id_payment = p.id_payment
    WHERE p.deleted_at IS NULL
    AND DATE_TRUNC('month', p.payment_date) = DATE_TRUNC('month', CURRENT_DATE)
)
SELECT
    month_name,
    COUNT(DISTINCT id_employee) as total_employees_paid,
    SUM(amount) as total_base_salary,
    SUM(total_bonus) as total_bonus_amount,
    SUM(total_deduction) as total_deduction_amount,
    SUM(amount + total_bonus - total_deduction) as net_payment_amount,
    ROUND(AVG(amount + total_bonus - total_deduction), 2) as average_payment,
    MIN(amount + total_bonus - total_deduction) as min_payment,
    MAX(amount + total_bonus - total_deduction) as max_payment,
    COUNT(CASE WHEN total_bonus > 0 THEN 1 END) as employees_with_bonus,
    COUNT(CASE WHEN total_deduction > 0 THEN 1 END) as employees_with_deduction
FROM current_month_payments
GROUP BY month_name;