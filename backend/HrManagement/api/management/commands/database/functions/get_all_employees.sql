DROP FUNCTION IF EXISTS get_all_employees(
    name_param varchar,
    id_param UUID,
    department_id_param UUID,
    role_param UUID,
    status_param UUID,
    order_by_param text[],
    order_direction_param text[],
    global_search_param varchar
);

CREATE OR REPLACE FUNCTION get_all_employees(
    name_param varchar DEFAULT NULL,
    id_param UUID DEFAULT NULL,
    department_id_param UUID DEFAULT NULL,
    role_param UUID DEFAULT NULL,
    status_param UUID DEFAULT NULL,
    order_by_param text[] DEFAULT NULL,           -- array para ordenação
    order_direction_param text[] DEFAULT NULL,   -- (ASC ou DESC)
    global_search_param varchar DEFAULT NULL
)
RETURNS TABLE(
    employee_name character varying,
    id character varying,
    role_name character varying,
    role_hex_color character varying,
    department_name character varying,
    status_name character varying,
    icon character varying,
    state_hex_color character varying
) AS $$
DECLARE
    order_by_clause text;
    sql_query text;
BEGIN
    order_by_clause := '';

    FOR i IN 1..array_length(order_by_param, 1)
    LOOP
        IF order_by_clause <> '' THEN
            order_by_clause := order_by_clause || ', ';
        END IF;

        order_by_clause := concat(order_by_clause,
            CASE
                WHEN order_by_param[i] = 'employee_name' THEN 'employee_name'
                WHEN order_by_param[i] = 'id' THEN 'employees.id_employee'
                WHEN order_by_param[i] = 'role_name' THEN 'roles.role_name'
                WHEN order_by_param[i] = 'department_name' THEN 'departments.name'
                WHEN order_by_param[i] = 'state_name' THEN 'contract_state.state'
                ELSE 'auth_user.first_name'
            END
        );

        order_by_clause := concat(order_by_clause,
            CASE
                WHEN order_direction_param[i] = 'ASC' THEN ' ASC'
                WHEN order_direction_param[i] = 'DESC' THEN ' DESC'
                ELSE ' ASC' -- ASC DEFAULT
            END
        );
    END LOOP;

    IF order_by_clause = '' THEN
        order_by_clause := 'auth_user.first_name ASC';
    END IF;

    sql_query := '
        SELECT
            CAST(employees.id_employee AS character varying) AS id_employee,
            CAST(auth_user.first_name || '' '' || auth_user.last_name AS character varying) AS employee_name,
            roles.role_name,
            roles.hex_color AS role_hex_color,
            departments.name AS department_name,
            contract_state.state,
            contract_state.icon,
            contract_state.hex_color AS state_hex_color
        FROM employees
        INNER JOIN auth_user ON employees.id_auth_user = auth_user.id
        LEFT JOIN latest_contract_materialized_view ON employees.id_employee = latest_contract_materialized_view.id_employee
        LEFT JOIN roles ON latest_contract_materialized_view.id_role = roles.id_role
        LEFT JOIN departments ON roles.id_department = departments.id_department
        LEFT JOIN latest_contract_state_materialized_view ON latest_contract_materialized_view.id_contract = latest_contract_state_materialized_view.id_contract
        LEFT JOIN contract_state ON latest_contract_state_materialized_view.id_contract_state = contract_state.id_contract_state
        WHERE
            ($1 IS NULL OR (auth_user.first_name || '' '' || auth_user.last_name) ILIKE $1)
            AND ($2 IS NULL OR employees.id_employee = $2)
            AND ($3 IS NULL OR departments.id_department = $3)
            AND ($4 IS NULL OR roles.id_role = $4)
            AND ($5 IS NULL OR contract_state.id_contract_state = $5)
            AND ($6 IS NULL OR (
                (auth_user.first_name || '' '' || auth_user.last_name) ILIKE ''%'' || $6 || ''%'' OR
                employees.id_employee::text ILIKE ''%'' || $6 || ''%'' OR
                roles.role_name ILIKE ''%'' || $6 || ''%'' OR
                departments.name ILIKE ''%'' || $6 || ''%'' OR
                contract_state.state ILIKE ''%'' || $6 || ''%''
            ))
        GROUP BY
            auth_user.first_name,
            auth_user.last_name,
            employees.id_employee,
            roles.role_name,
            roles.hex_color,
            departments.name,
            contract_state.state,
            contract_state.icon,
            contract_state.hex_color
        ORDER BY ' || order_by_clause || ';';

    RETURN QUERY EXECUTE sql_query USING name_param, id_param, department_id_param, role_param, status_param, global_search_param;
END;
$$ LANGUAGE plpgsql;


/* -- TESTE
SELECT *
FROM get_all_employees(
        NULL::varchar,    -- name_param
        NULL::UUID,    -- id_param
        NULL::uuid,       -- department_id_param
        NULL::uuid,       -- role_param
        NULL::uuid,       -- status_param
        ARRAY['first_name']::text[],   -- order_by_param
        ARRAY['ASC']::text[],  -- order_direction_param
        NULL::varchar
     );
 */