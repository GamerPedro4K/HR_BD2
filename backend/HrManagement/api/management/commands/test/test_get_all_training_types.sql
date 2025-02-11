SELECT *
FROM get_all_training_types(
    NULL::varchar,              -- global_search_param (sem filtro)
    ARRAY['name']::text[],      -- order_by_param (ordenar por nome)
    ARRAY['ASC']::text[],       -- order_direction_param (ordem ascendente)
    5,                          -- limit_param (limitar a 5 resultados)
    0                           -- offset_param (sem deslocamento)
);
