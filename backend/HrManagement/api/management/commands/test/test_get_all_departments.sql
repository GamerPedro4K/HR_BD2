SELECT *
FROM get_all_departments(
    NULL::text,                     -- global_search_param
    ARRAY['department_name']::text[], -- order_by_param
    ARRAY['ASC']::text[],             -- order_direction_param
    2,                                -- limit_param
    0                                 -- offset_param
);
