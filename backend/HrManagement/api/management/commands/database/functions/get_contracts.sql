
DROP FUNCTION IF EXISTS get_contracts(
    employee_id_param UUID,
    global_search_param VARCHAR,
    id_contract_param UUID,
    role_name_param VARCHAR,
    department_name_param VARCHAR,
    contract_type_name_param VARCHAR,
    contract_state_name_param VARCHAR,
    order_by_param TEXT[],
    order_direction_param TEXT[]
);

CREATE OR REPLACE FUNCTION get_contracts(
    employee_id_param UUID,
    global_search_param VARCHAR DEFAULT NULL,
    id_contract_param UUID DEFAULT NULL,
    role_name_param VARCHAR DEFAULT NULL,
    department_name_param VARCHAR DEFAULT NULL,
    contract_type_name_param VARCHAR DEFAULT NULL,
    contract_state_name_param VARCHAR DEFAULT NULL,
    order_by_param TEXT[] DEFAULT NULL,
    order_direction_param TEXT[] DEFAULT NULL
)
RETURNS TABLE(
    id_contract UUID,
    base_salary NUMERIC,
    extra_hour_rate NUMERIC,
    role_name VARCHAR,
    department_name VARCHAR,
    created_at TIMESTAMP,
    contract_type_name VARCHAR,
    description TEXT,
    benefits_eligible BOOLEAN,
    overtime_eligible BOOLEAN,
    termination_notice_period NUMERIC,
    contract_state_name VARCHAR,
    contract_state_icon VARCHAR,
    contract_state_color VARCHAR
) AS $$
DECLARE
    order_by_clause TEXT;
    sql_query TEXT;
BEGIN
    -- Construir a cláusula ORDER BY dinamicamente
    order_by_clause := '';
    FOR i IN 1..array_length(order_by_param, 1)
    LOOP
        IF order_by_clause <> '' THEN
            order_by_clause := order_by_clause || ', ';
        END IF;

        order_by_clause := concat(order_by_clause,
            CASE
                WHEN order_by_param[i] = 'id_contract' THEN 'contract.id_contract'
                WHEN order_by_param[i] = 'base_salary' THEN 'salary_history.base_salary'
                WHEN order_by_param[i] = 'extra_hour_rate' THEN 'salary_history.extra_hour_rate'
                WHEN order_by_param[i] = 'role_name' THEN 'roles.role_name'
                WHEN order_by_param[i] = 'department_name' THEN 'departments.name'
                WHEN order_by_param[i] = 'created_at' THEN 'contract.created_at'
                WHEN order_by_param[i] = 'contract_type_name' THEN 'contract_type.contract_type_name'
                WHEN order_by_param[i] = 'description' THEN 'contract_type.description'
                WHEN order_by_param[i] = 'benefits_eligible' THEN 'contract_type.benefits_eligible'
                WHEN order_by_param[i] = 'overtime_eligible' THEN 'contract_type.overtime_eligible'
                WHEN order_by_param[i] = 'termination_notice_period' THEN 'contract_type.termination_notice_period'
                WHEN order_by_param[i] = 'contract_state_name' THEN 'contract_state.state'
                ELSE 'contract.created_at' -- Padrão
            END
        );

        order_by_clause := concat(order_by_clause,
            CASE
                WHEN order_direction_param[i] = 'ASC' THEN ' ASC'
                WHEN order_direction_param[i] = 'DESC' THEN ' DESC'
                ELSE ' DESC' -- DESC DEFAULT
            END
        );
    END LOOP;

    IF order_by_clause = '' THEN
        order_by_clause := 'contract.created_at DESC'; -- Padrão se nada for fornecido
    END IF;

    -- Construir a consulta SQL
    sql_query := '
    SELECT
        contract.id_contract,
        salary_history.base_salary,
        salary_history.extra_hour_rate,
        roles.role_name,
        departments.name AS department_name,
        contract.created_at,
        contract_type.contract_type_name,
        contract_type.description,
        contract_type.benefits_eligible,
        contract_type.overtime_eligible,
        contract_type.termination_notice_period,
        contract_state.state AS contract_state_name,
        contract_state.icon AS contract_state_icon,
        contract_state.hex_color AS contract_state_color
    FROM contract
    INNER JOIN contract_type ON contract.id_contract_type = contract_type.id_contract_type
    INNER JOIN roles ON contract.id_role = roles.id_role
    INNER JOIN departments ON roles.id_department = departments.id_department
    LEFT JOIN latest_contract_state_materialized_view ON contract.id_contract = latest_contract_state_materialized_view.id_contract
    INNER JOIN contract_state ON latest_contract_state_materialized_view.id_contract_state = contract_state.id_contract_state
    LEFT JOIN salary_history ON contract.id_contract = salary_history.id_contract
    WHERE $1 IS NULL OR contract.id_employee = $1
        AND ($2 IS NULL OR (
            contract.id_contract::text ILIKE ''%'' || $2 || ''%'' OR
            contract_type.contract_type_name ILIKE ''%'' || $2 || ''%'' OR
            roles.role_name ILIKE ''%'' || $2 || ''%'' OR
            departments.name ILIKE ''%'' || $2 || ''%'' OR
            contract_state.state ILIKE ''%'' || $2 || ''%''
        ))
        AND ($3 IS NULL OR contract.id_contract = $3)
        AND ($4 IS NULL OR roles.role_name ILIKE ''%'' || $4 || ''%'' )
        AND ($5 IS NULL OR departments.name ILIKE ''%'' || $5 || ''%'' )
        AND ($6 IS NULL OR contract_type.contract_type_name ILIKE ''%'' || $6 || ''%'' )
        AND ($7 IS NULL OR contract_state.state ILIKE ''%'' || $7 || ''%'' )
    ORDER BY ' || order_by_clause;

    RETURN QUERY EXECUTE sql_query USING employee_id_param, global_search_param, id_contract_param, role_name_param, department_name_param, contract_type_name_param, contract_state_name_param;
END;
$$ LANGUAGE plpgsql;





/* SELECT * FROM get_contracts(
    NULL, -- employee_id_param
    NULL,                                  -- global_search_param
    NULL,-- id_contract_param
    NULL,                                  -- role_name_param
    NULL,                                  -- department_name_param
    NULL,                                  -- contract_type_name_param
    NULL,                                  -- contract_state_name_param
    ARRAY['base_salary'],                  -- order_by_param
    ARRAY['ASC']                           -- order_direction_param
); */