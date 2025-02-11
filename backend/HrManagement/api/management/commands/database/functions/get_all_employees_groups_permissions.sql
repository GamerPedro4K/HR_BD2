CREATE OR REPLACE FUNCTION get_all_employees_groups_permissions(
    global_search_param VARCHAR DEFAULT NULL,
    order_by_param TEXT[] DEFAULT ARRAY['name'],
    order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
    limit_param INTEGER DEFAULT NULL,
    offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
    id_employee UUID,
    src VARCHAR,
    full_name TEXT,
    groups TEXT,
    total_count BIGINT
) AS $$
DECLARE
    base_query TEXT;
    count_query TEXT;
    final_query TEXT;
    total BIGINT;
BEGIN
    base_query := '
    WITH employee_data AS (
        SELECT
            e.id_employee,
            e.src,
            concat(au.first_name, '' '', au.last_name) as full_name,
            (
                SELECT json_agg(
                    json_build_object(
                        ''group_id'', ag.id,
                        ''group_name'', ag.name,
                        ''permissions'', (
                            SELECT json_agg(
                                json_build_object(
                                    ''id'', ap.id,
                                    ''name'', ap.name,
                                    ''codename'', ap.codename
                                )
                            )
                            FROM auth_group_permissions agp
                            JOIN auth_permission ap ON ap.id = agp.permission_id
                            WHERE agp.group_id = ag.id
                        )
                    )
                )
                FROM auth_user_groups aug2
                JOIN auth_group ag ON aug2.group_id = ag.id
                WHERE aug2.user_id = au.id
            )::text as groups
        FROM employees e
        JOIN auth_user au ON e.id_auth_user = au.id
        LEFT JOIN auth_user_groups aug ON au.id = aug.user_id
        LEFT JOIN auth_group ag ON aug.group_id = ag.id
        LEFT JOIN trainings t ON t.id_employee = e.id_employee
        LEFT JOIN training_types tt ON t.id_training_type = tt.id_training_type
        WHERE (
            $1 IS NULL OR
            e.id_employee::text = $1 OR
            LOWER(au.first_name) LIKE LOWER(''%'' || $1 || ''%'') OR
            LOWER(au.last_name) LIKE LOWER(''%'' || $1 || ''%'') OR
            LOWER(ag.name) LIKE LOWER(''%'' || $1 || ''%'') OR
            t.id_training::text = $1 OR
            LOWER(tt.name) LIKE LOWER(''%'' || $1 || ''%'')
        )
        GROUP BY e.id_employee, e.src, au.first_name, au.last_name, au.id, ag.name
        ORDER BY
            CASE WHEN $2[1] = ''name'' AND $3[1] = ''ASC''
                THEN concat(au.first_name, '' '', au.last_name) END ASC NULLS LAST,
            CASE WHEN $2[1] = ''name'' AND $3[1] = ''DESC''
                THEN concat(au.first_name, '' '', au.last_name) END DESC NULLS LAST,
            CASE WHEN $2[1] = ''groups'' AND $3[1] = ''ASC''
                THEN ag.name END ASC NULLS LAST,
            CASE WHEN $2[1] = ''groups'' AND $3[1] = ''DESC''
                THEN ag.name END DESC NULLS LAST
    ';

    IF limit_param IS NOT NULL AND offset_param IS NOT NULL THEN
        base_query := base_query || '
        LIMIT $4 OFFSET $5';
    END IF;

    base_query := base_query || '
    )
    SELECT *
    FROM employee_data';

    count_query := '
    SELECT COUNT(DISTINCT e.id_employee)
    FROM employees e
    JOIN auth_user au ON e.id_auth_user = au.id
    LEFT JOIN auth_user_groups aug ON au.id = aug.user_id
    LEFT JOIN auth_group ag ON aug.group_id = ag.id
    LEFT JOIN trainings t ON t.id_employee = e.id_employee
    LEFT JOIN training_types tt ON t.id_training_type = tt.id_training_type
    WHERE (
        $1 IS NULL OR
        e.id_employee::text = $1 OR
        LOWER(au.first_name) LIKE LOWER(''%'' || $1 || ''%'') OR
        LOWER(au.last_name) LIKE LOWER(''%'' || $1 || ''%'') OR
        LOWER(ag.name) LIKE LOWER(''%'' || $1 || ''%'') OR
        t.id_training::text = $1 OR
        LOWER(tt.name) LIKE LOWER(''%'' || $1 || ''%'')
    )';

    EXECUTE count_query
    USING global_search_param
    INTO total;

    final_query := 'SELECT sub.*, ' || total || '::BIGINT as total_count FROM (' || base_query || ') sub';

    RETURN QUERY EXECUTE final_query
    USING global_search_param, order_by_param, order_direction_param, limit_param, offset_param;
END;
$$ LANGUAGE plpgsql;