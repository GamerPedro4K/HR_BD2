SELECT *
FROM get_all_contract_states(
    NULL::text,                  -- global_search_param
    ARRAY['state']::text[],      -- order_by_param
    ARRAY['ASC']::text[],        -- order_direction_param
    3,                           -- limit_param
    0                            -- offset_param
);
