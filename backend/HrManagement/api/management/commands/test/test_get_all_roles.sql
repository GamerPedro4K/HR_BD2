SELECT *
FROM get_all_roles(
    NULL::varchar,              -- global_search_param
    ARRAY['role_name']::text[], -- order_by_param
    ARRAY['ASC']::text[],      -- order_direction_param
    5,                         -- limit_param
    0                          -- offset_param
);