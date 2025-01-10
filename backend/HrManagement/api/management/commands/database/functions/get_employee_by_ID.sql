DROP FUNCTION IF EXISTS get_employees_by_id(param_employee_id UUID);
CREATE OR REPLACE FUNCTION get_employees_by_id(param_employee_id UUID)
RETURNS TABLE(
    id_employee character varying,
    employee_name character varying,
    phone character varying,
    photo character varying,
    email character varying,
    birth_date date,
    date_joined timestamp with time zone,
    id_role UUID,
    role_name character varying,
    role_hex_color character varying,
    role_description character varying,
    department_name character varying,
    state character varying,
    icon character varying,
    state_hex_color character varying,
    base_salary numeric,
    city character varying,
    country character varying,
    district character varying,
    address character varying,
    zip_code character varying

) AS $$
BEGIN
    RETURN QUERY
    SELECT
        CAST(employees.id_employee AS character varying) AS id_employee,
        CAST(auth_user.first_name || ' ' || auth_user.last_name AS character varying) AS employee_name,
        employees.phone,
        employees.src AS photo,
        auth_user.email,
        employees.birth_date,
        auth_user.date_joined,
        roles.id_role,
        roles.role_name,
        roles.hex_color AS role_hex_color,
        CAST(roles.description AS character varying) AS role_description,
        departments.name AS department_name,
        contract_state.state,
        contract_state.icon,
        contract_state.hex_color AS state_hex_color,
        latest_salary_materialized_view.base_salary,
        employee_location.city,
        employee_location.country,
        employee_location.district,
        employee_location.address,
        employee_location.zip_code
    FROM employees
    INNER JOIN auth_user ON employees.id_auth_user = auth_user.id
    LEFT JOIN contract ON employees.id_employee = contract.id_employee
    LEFT JOIN latest_salary_materialized_view ON contract.id_contract = latest_salary_materialized_view.id_contract
    LEFT JOIN latest_contract_materialized_view ON contract.id_contract = latest_contract_materialized_view.id_contract
    LEFT JOIN roles ON contract.id_role = roles.id_role
    LEFT JOIN departments ON roles.id_department = departments.id_department
    LEFT JOIN latest_contract_state_materialized_view ON contract.id_contract = latest_contract_state_materialized_view.id_contract
    LEFT JOIN contract_state ON latest_contract_state_materialized_view.id_contract_state = contract_state.id_contract_state
    LEFT JOIN employee_location ON employees.id_employee = employee_location.id_employee
    WHERE
        employees.id_employee = param_employee_id AND
        employees.deleted_at IS NULL AND
        (latest_contract_materialized_view.id_contract = contract.id_contract OR latest_contract_materialized_view.id_contract IS NULL);
END;
$$ LANGUAGE plpgsql;
