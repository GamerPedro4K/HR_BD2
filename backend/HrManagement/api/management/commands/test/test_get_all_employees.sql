SELECT *
FROM get_all_employees(
    NULL::text,    -- name_param
    NULL::UUID,    -- id_param
    NULL::uuid,    -- department_id_param
    NULL::uuid,    -- role_param
    NULL::uuid,    -- status_param
    ARRAY['employee_name']::text[],   -- order_by_param
    ARRAY['ASC']::text[],  -- order_direction_param
    NULL::text    -- global_search_param
)
LIMIT 2;

