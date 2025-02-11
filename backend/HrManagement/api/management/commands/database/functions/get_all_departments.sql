CREATE OR REPLACE FUNCTION get_all_departments(
   global_search_param VARCHAR DEFAULT NULL,
   order_by_param TEXT[] DEFAULT ARRAY['name'],
   order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
   limit_param INTEGER DEFAULT NULL,
   offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
   id_department UUID,
   department_name VARCHAR,
   department_description TEXT,
   id_role UUID,
   role_name VARCHAR,
   hex_color VARCHAR,
   role_description TEXT,
   id_training_type UUID,
   training_type_name VARCHAR,
   training_type_description TEXT,
   training_type_hours INT,
   total_count BIGINT
) AS $$
DECLARE
   base_query TEXT;
   count_query TEXT;
   final_query TEXT;
   total BIGINT;
BEGIN
   -- First get the limited departments
   base_query := '
   WITH limited_departments AS (
       SELECT d.id_department, d.name, d.description
       FROM departments d
       WHERE d.deleted_at IS NULL
       AND (
           $1 IS NULL OR
           d.id_department::text = $1 OR
           LOWER(d.name) LIKE LOWER(''%'' || $1 || ''%'') OR
           LOWER(d.description) LIKE LOWER(''%'' || $1 || ''%'')
       )
       ORDER BY
           CASE WHEN $2[1] = ''name'' AND $3[1] = ''ASC'' THEN d.name END ASC NULLS LAST,
           CASE WHEN $2[1] = ''name'' AND $3[1] = ''DESC'' THEN d.name END DESC NULLS LAST';

   IF limit_param IS NOT NULL AND offset_param IS NOT NULL THEN
       base_query := base_query || '
       LIMIT $4 OFFSET $5';
   END IF;

   base_query := base_query || '
   )
   SELECT
       d.id_department,
       d.name,
       d.description,
       r.id_role,
       r.role_name,
       r.hex_color,
       r.description,
       ttr.id_training_type,
       tt.name,
       tt.description,
       tt.hours
   FROM limited_departments d
   LEFT JOIN roles r ON d.id_department = r.id_department AND r.deleted_at IS NULL
   LEFT JOIN training_type_role ttr ON r.id_role = ttr.id_role AND ttr.deleted_at IS NULL
   LEFT JOIN training_types tt ON ttr.id_training_type = tt.id_training_type AND tt.deleted_at IS NULL';

   -- Get total count of departments
   count_query := '
   SELECT COUNT(DISTINCT d.id_department)
   FROM departments d
   WHERE d.deleted_at IS NULL
   AND (
       $1 IS NULL OR
       d.id_department::text = $1 OR
       LOWER(d.name) LIKE LOWER(''%'' || $1 || ''%'') OR
       LOWER(d.description) LIKE LOWER(''%'' || $1 || ''%'')
   )';

   EXECUTE count_query
   USING global_search_param
   INTO total;

   final_query := 'SELECT sub.*, ' || total || '::BIGINT as total_count FROM (' || base_query || ') sub';

   RETURN QUERY EXECUTE final_query
   USING global_search_param, order_by_param, order_direction_param, limit_param, offset_param;

END;
$$ LANGUAGE plpgsql;
