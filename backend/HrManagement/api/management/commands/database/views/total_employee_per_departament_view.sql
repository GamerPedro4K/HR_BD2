CREATE OR REPLACE VIEW total_employees_per_department_view AS
SELECT 
    d.name AS department_name, 
    COUNT(c.id_employee) AS total_employees
FROM departments d
LEFT JOIN roles r ON d.id_department = r.id_department
LEFT JOIN contract c ON r.id_role = c.id_role
WHERE c.deleted_at IS NULL
GROUP BY d.name;
