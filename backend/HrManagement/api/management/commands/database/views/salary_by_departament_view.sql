CREATE OR REPLACE VIEW salary_by_departament_view AS
SELECT 
    d.name as department_name,
    COUNT(DISTINCT e.id_employee) as employee_count,
    ROUND(AVG(sh.base_salary), 2) as avg_salary,
    MIN(sh.base_salary) as min_salary,
    MAX(sh.base_salary) as max_salary
FROM departments d
JOIN roles r ON r.id_department = d.id_department
JOIN contract c ON c.id_role = r.id_role
JOIN employees e ON e.id_employee = c.id_employee
JOIN salary_history sh ON sh.id_contract = c.id_contract
WHERE d.deleted_at IS NULL 
  AND r.deleted_at IS NULL 
  AND c.deleted_at IS NULL 
  AND e.deleted_at IS NULL
  AND sh.deleted_at IS NULL
GROUP BY d.name;