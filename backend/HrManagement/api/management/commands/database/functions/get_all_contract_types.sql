CREATE OR REPLACE FUNCTION get_all_contract_types(
   global_search_param VARCHAR DEFAULT NULL,
   order_by_param TEXT[] DEFAULT ARRAY['contract_type_name'],
   order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
   limit_param INTEGER DEFAULT NULL,
   offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
   id_contract_type UUID,
   contract_type_name VARCHAR,
   description TEXT,
   termination_notice_period NUMERIC(10,2),
   overtime_eligible BOOLEAN,
   benefits_eligible BOOLEAN,
   total_count BIGINT
) AS $$
DECLARE
   base_query TEXT;
   count_query TEXT;
   final_query TEXT;
   total BIGINT;
BEGIN
   -- Base query para selecionar os contract types com filtros
   base_query := '
   WITH limited_contract_types AS (
       SELECT
           id_contract_type,
           contract_type_name,
           description,
           termination_notice_period,
           overtime_eligible,
           benefits_eligible
       FROM contract_type
       WHERE deleted_at IS NULL
       AND (
           $1 IS NULL OR
           id_contract_type::text = $1 OR
           LOWER(contract_type_name) LIKE LOWER(''%'' || $1 || ''%'') OR
           LOWER(description) LIKE LOWER(''%'' || $1 || ''%'')
       )
       ORDER BY
           CASE WHEN $2[1] = ''contract_type_name'' AND $3[1] = ''ASC'' THEN contract_type_name END ASC NULLS LAST,
           CASE WHEN $2[1] = ''contract_type_name'' AND $3[1] = ''DESC'' THEN contract_type_name END DESC NULLS LAST,
           CASE WHEN $2[1] = ''description'' AND $3[1] = ''ASC'' THEN description END ASC NULLS LAST,
           CASE WHEN $2[1] = ''description'' AND $3[1] = ''DESC'' THEN description END DESC NULLS LAST,
           CASE WHEN $2[1] = ''termination_notice_period'' AND $3[1] = ''ASC'' THEN termination_notice_period END ASC NULLS LAST,
           CASE WHEN $2[1] = ''termination_notice_period'' AND $3[1] = ''DESC'' THEN termination_notice_period END DESC NULLS LAST,
           CASE WHEN $2[1] = ''overtime_eligible'' AND $3[1] = ''ASC'' THEN overtime_eligible END ASC NULLS LAST,
           CASE WHEN $2[1] = ''overtime_eligible'' AND $3[1] = ''DESC'' THEN overtime_eligible END DESC NULLS LAST,
           CASE WHEN $2[1] = ''benefits_eligible'' AND $3[1] = ''ASC'' THEN benefits_eligible END ASC NULLS LAST,
           CASE WHEN $2[1] = ''benefits_eligible'' AND $3[1] = ''DESC'' THEN benefits_eligible END DESC NULLS LAST
   ';

   IF limit_param IS NOT NULL AND offset_param IS NOT NULL THEN
       base_query := base_query || '
       LIMIT $4 OFFSET $5';
   END IF;

   base_query := base_query || '
   )
   SELECT *
   FROM limited_contract_types';

   -- Query para contar o total de contract types
   count_query := '
   SELECT COUNT(*)
   FROM contract_type
   WHERE deleted_at IS NULL
   AND (
       $1 IS NULL OR
       id_contract_type::text = $1 OR
       LOWER(contract_type_name) LIKE LOWER(''%'' || $1 || ''%'') OR
       LOWER(description) LIKE LOWER(''%'' || $1 || ''%'')
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
