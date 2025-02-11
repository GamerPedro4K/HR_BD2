SELECT *
FROM get_all_payment_methods(
    NULL::text,                   -- global_search_param (sem filtro de pesquisa)
    ARRAY['name']::text[],        -- order_by_param (ordenar pelo nome do método de pagamento)
    ARRAY['ASC']::text[],         -- order_direction_param (ordem crescente)
    5,                            -- limit_param (limitar a 5 resultados)
    0                             -- offset_param (começar do primeiro resultado)
);
