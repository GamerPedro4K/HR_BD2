CREATE OR REPLACE FUNCTION get_all_roles(
   global_search_param VARCHAR DEFAULT NULL,
   order_by_param TEXT[] DEFAULT ARRAY['role_name'],
   order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
   limit_param INTEGER DEFAULT NULL,
   offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
   id_role UUID,
   id_department UUID,
   id_auth_group INTEGER,
   role_name VARCHAR,
   hex_color VARCHAR,
   role_description TEXT,
   department_name VARCHAR,
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
   -- First, get the limited roles
   base_query := '
   WITH limited_roles AS (
       SELECT
           r.id_role,
           r.id_department,
           r.id_auth_group,
           r.role_name,
           r.hex_color,
           r.description,
           d.name as department_name
       FROM roles r
       LEFT JOIN departments d ON r.id_department = d.id_department AND d.deleted_at IS NULL
       LEFT JOIN training_type_role ttr ON r.id_role = ttr.id_role AND ttr.deleted_at IS NULL
       LEFT JOIN training_types tt ON ttr.id_training_type = tt.id_training_type AND tt.deleted_at IS NULL
       WHERE r.deleted_at IS NULL
       AND (
           $1 IS NULL OR
           r.id_role::text = $1 OR
           d.id_department::text = $1 OR
           LOWER(r.role_name) LIKE LOWER(''%'' || $1 || ''%'') OR
           LOWER(d.name) LIKE LOWER(''%'' || $1 || ''%'') OR
           LOWER(r.description) LIKE LOWER(''%'' || $1 || ''%'') OR
           LOWER(tt.name) LIKE LOWER(''%'' || $1 || ''%'')
       )
       GROUP BY r.id_role, r.id_department, r.id_auth_group, r.role_name, r.hex_color, r.description, d.name
       ORDER BY
           CASE WHEN $2[1] = ''role_name'' AND $3[1] = ''ASC'' THEN r.role_name END ASC NULLS LAST,
           CASE WHEN $2[1] = ''role_name'' AND $3[1] = ''DESC'' THEN r.role_name END DESC NULLS LAST,
           CASE WHEN $2[1] = ''department_name'' AND $3[1] = ''ASC'' THEN d.name END ASC NULLS LAST,
           CASE WHEN $2[1] = ''department_name'' AND $3[1] = ''DESC'' THEN d.name END DESC NULLS LAST,
           CASE WHEN $2[1] = ''description'' AND $3[1] = ''ASC'' THEN r.description END ASC NULLS LAST,
           CASE WHEN $2[1] = ''description'' AND $3[1] = ''DESC'' THEN r.description END DESC NULLS LAST';

   IF limit_param IS NOT NULL AND offset_param IS NOT NULL THEN
       base_query := base_query || '
       LIMIT $4 OFFSET $5';
   END IF;

   base_query := base_query || '
   )
   SELECT
       r.id_role,
       r.id_department,
       r.id_auth_group,
       r.role_name,
       r.hex_color,
       r.description as role_description,
       r.department_name,
       ttr.id_training_type,
       tt.name as training_type_name,
       tt.description as training_type_description,
       tt.hours as training_type_hours
   FROM limited_roles r
   LEFT JOIN training_type_role ttr ON r.id_role = ttr.id_role AND ttr.deleted_at IS NULL
   LEFT JOIN training_types tt ON ttr.id_training_type = tt.id_training_type AND tt.deleted_at IS NULL
   ORDER BY
           CASE WHEN $2[1] = ''role_name'' AND $3[1] = ''ASC'' THEN r.role_name END ASC NULLS LAST,
           CASE WHEN $2[1] = ''role_name'' AND $3[1] = ''DESC'' THEN r.role_name END DESC NULLS LAST,
           CASE WHEN $2[1] = ''department_name'' AND $3[1] = ''ASC'' THEN r.department_name END ASC NULLS LAST,
           CASE WHEN $2[1] = ''department_name'' AND $3[1] = ''DESC'' THEN r.department_name END DESC NULLS LAST,
           CASE WHEN $2[1] = ''description'' AND $3[1] = ''ASC'' THEN r.description END ASC NULLS LAST,
           CASE WHEN $2[1] = ''description'' AND $3[1] = ''DESC'' THEN r.description END DESC NULLS LAST';

   -- Get total count of roles
   count_query := '
   SELECT COUNT(DISTINCT r.id_role)
   FROM roles r
       LEFT JOIN departments d ON r.id_department = d.id_department AND d.deleted_at IS NULL
       LEFT JOIN training_type_role ttr ON r.id_role = ttr.id_role AND ttr.deleted_at IS NULL
       LEFT JOIN training_types tt ON ttr.id_training_type = tt.id_training_type AND tt.deleted_at IS NULL
   WHERE r.deleted_at IS NULL
   AND (
           $1 IS NULL OR
           r.id_role::text = $1 OR
           d.id_department::text = $1 OR
           LOWER(r.role_name) LIKE LOWER(''%'' || $1 || ''%'') OR
           LOWER(d.name) LIKE LOWER(''%'' || $1 || ''%'') OR
           LOWER(r.description) LIKE LOWER(''%'' || $1 || ''%'') OR
           LOWER(tt.name) LIKE LOWER(''%'' || $1 || ''%'')
   )';

   EXECUTE count_query
   USING global_search_param
   INTO total;

   final_query := 'SELECT sub.*, ' || total || '::BIGINT as total_count FROM (' || base_query || ') sub';

   RETURN QUERY EXECUTE final_query
   USING global_search_param, order_by_param, order_direction_param, limit_param, offset_param;

END;
$$ LANGUAGE plpgsql;