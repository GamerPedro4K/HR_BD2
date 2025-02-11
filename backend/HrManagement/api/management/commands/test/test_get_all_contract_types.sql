SELECT *
FROM get_all_contract_types(
    NULL::text,                         -- global_search_param
    ARRAY['contract_type_name']::text[], -- order_by_param
    ARRAY['ASC']::text[],                -- order_direction_param
    2,                                   -- limit_param
    0                                    -- offset_param
);
