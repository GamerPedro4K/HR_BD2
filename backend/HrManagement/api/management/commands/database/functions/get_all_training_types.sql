CREATE OR REPLACE FUNCTION get_all_training_types(
   global_search_param VARCHAR DEFAULT NULL,
   order_by_param TEXT[] DEFAULT ARRAY['name'],
   order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
   limit_param INTEGER DEFAULT NULL,
   offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
   id_training_type UUID,
   name VARCHAR,
   description TEXT,
   hours INT,
   total_count BIGINT
) AS $$
DECLARE
   base_query TEXT;
   count_query TEXT;
   final_query TEXT;
   total BIGINT;
BEGIN
   -- Base query para selecionar os training types com filtros
   base_query := '
   WITH limited_training_types AS (
       SELECT
           id_training_type,
           name,
           description,
           hours
       FROM training_types
       WHERE deleted_at IS NULL
       AND (
           $1 IS NULL OR
           id_training_type::text = $1 OR
           LOWER(name) LIKE LOWER(''%'' || $1 || ''%'') OR
           LOWER(description) LIKE LOWER(''%'' || $1 || ''%'') OR
           hours::text = $1
       )
       ORDER BY
           CASE WHEN $2[1] = ''name'' AND $3[1] = ''ASC'' THEN name END ASC NULLS LAST,
           CASE WHEN $2[1] = ''name'' AND $3[1] = ''DESC'' THEN name END DESC NULLS LAST,
           CASE WHEN $2[1] = ''description'' AND $3[1] = ''ASC'' THEN description END ASC NULLS LAST,
           CASE WHEN $2[1] = ''description'' AND $3[1] = ''DESC'' THEN description END DESC NULLS LAST,
           CASE WHEN $2[1] = ''hours'' AND $3[1] = ''ASC'' THEN hours END ASC NULLS LAST,
           CASE WHEN $2[1] = ''hours'' AND $3[1] = ''DESC'' THEN hours END DESC NULLS LAST';

   IF limit_param IS NOT NULL AND offset_param IS NOT NULL THEN
       base_query := base_query || '
       LIMIT $4 OFFSET $5';
   END IF;

   base_query := base_query || '
   )
   SELECT *
   FROM limited_training_types';

   -- Query para contar o total de training types
   count_query := '
   SELECT COUNT(*)
   FROM training_types
   WHERE deleted_at IS NULL
   AND (
       $1 IS NULL OR
       id_training_type::text = $1 OR
       LOWER(name) LIKE LOWER(''%'' || $1 || ''%'') OR
       LOWER(description) LIKE LOWER(''%'' || $1 || ''%'') OR
       hours::text = $1
   )';

   -- Executar a contagem
   EXECUTE count_query
   USING global_search_param
   INTO total;

   -- Combinar a contagem com os resultados paginados
   final_query := 'SELECT sub.*, ' || total || '::BIGINT as total_count FROM (' || base_query || ') sub';

   RETURN QUERY EXECUTE final_query
   USING global_search_param, order_by_param, order_direction_param, limit_param, offset_param;
END;
$$ LANGUAGE plpgsql;
