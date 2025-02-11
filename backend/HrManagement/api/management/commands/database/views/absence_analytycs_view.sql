CREATE OR REPLACE VIEW absence_analytics_view AS
SELECT
    au.first_name || ' ' || au.last_name as employee_name,
    COUNT(ar.id_absence_reason) as total_absences,
    SUM(DATE_PART('day', ar.end_date::timestamp - ar.start_date::timestamp)) as total_days_absent
FROM employees e
INNER JOIN auth_user au ON e.id_auth_user = au.id
INNER JOIN absence_reason ar ON ar.id_employee = e.id_employee
WHERE e.deleted_at IS NULL
  AND ar.deleted_at IS NULL
GROUP BY employee_name
ORDER BY total_days_absent DESC
LIMIT 5;