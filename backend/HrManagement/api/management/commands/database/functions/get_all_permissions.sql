CREATE OR REPLACE FUNCTION get_all_permissions(
    global_search_param VARCHAR DEFAULT NULL,
    order_by_param TEXT[] DEFAULT ARRAY['name'],
    order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
    limit_param INTEGER DEFAULT NULL,
    offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    codename VARCHAR,
    total_count BIGINT
) AS $$
DECLARE
    base_query TEXT;
    count_query TEXT;
    final_query TEXT;
    total BIGINT;
BEGIN
    base_query := '
    WITH permissions_data AS (
        SELECT
            p.id,
            p.name,
            p.codename
        FROM auth_permission p
        WHERE (
            $1 IS NULL OR
            p.id::text = $1 OR
            LOWER(p.name) LIKE LOWER(''%'' || $1 || ''%'') OR
            LOWER(p.codename) LIKE LOWER(''%'' || $1 || ''%'')
        )
        ORDER BY
            CASE WHEN $2[1] = ''name'' AND $3[1] = ''ASC'' THEN p.name END ASC NULLS LAST,
            CASE WHEN $2[1] = ''name'' AND $3[1] = ''DESC'' THEN p.name END DESC NULLS LAST,
            CASE WHEN $2[1] = ''codename'' AND $3[1] = ''ASC'' THEN p.codename END ASC NULLS LAST,
            CASE WHEN $2[1] = ''codename'' AND $3[1] = ''DESC'' THEN p.codename END DESC NULLS LAST
    ';

    IF limit_param IS NOT NULL AND offset_param IS NOT NULL THEN
        base_query := base_query || '
        LIMIT $4 OFFSET $5';
    END IF;

    base_query := base_query || '
    )
    SELECT *
    FROM permissions_data';

    count_query := '
    SELECT COUNT(*)
    FROM auth_permission p
    WHERE (
        $1 IS NULL OR
        p.id::text = $1 OR
        LOWER(p.name) LIKE LOWER(''%'' || $1 || ''%'') OR
        LOWER(p.codename) LIKE LOWER(''%'' || $1 || ''%'')
    )';

    EXECUTE count_query
    USING global_search_param
    INTO total;

    final_query := 'SELECT sub.*, ' || total || '::BIGINT as total_count FROM (' || base_query || ') sub';

    RETURN QUERY EXECUTE final_query
    USING global_search_param, order_by_param, order_direction_param, limit_param, offset_param;
END;
$$ LANGUAGE plpgsql;