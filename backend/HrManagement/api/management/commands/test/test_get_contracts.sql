SELECT * FROM get_contracts(
    NULL, -- employee_id_param
    NULL,                                  -- global_search_param
    NULL,-- id_contract_param
    NULL,                                  -- role_name_param
    NULL,                                  -- department_name_param
    NULL,                                  -- contract_type_name_param
    NULL,                                  -- contract_state_name_param
    ARRAY['base_salary', 'extra_hour_rate', 'role_name', 'department_name', 'contract_type_name', 'description', 'benefits_eligible', 'overtime_eligible', 'termination_notice_period', 'contract_state_name'],                  -- order_by_param
    ARRAY['ASC']                           -- order_direction_param
)
LIMIT 1;