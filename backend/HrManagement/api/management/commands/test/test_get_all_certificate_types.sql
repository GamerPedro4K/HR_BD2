SELECT *
FROM get_all_certificate_types(
    NULL::text,                   -- global_search_param (sem filtro de pesquisa)
    ARRAY['name']::text[],        -- order_by_param (ordenar pelo nome do certificado)
    ARRAY['ASC']::text[],         -- order_direction_param (ordem crescente)
    5,                            -- limit_param (limitar a 5 resultados)
    0                             -- offset_param (começar do primeiro resultado)
);
