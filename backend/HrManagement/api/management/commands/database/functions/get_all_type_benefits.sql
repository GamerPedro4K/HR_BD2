CREATE OR REPLACE FUNCTION get_all_type_benefits(
    global_search_param VARCHAR DEFAULT NULL,
    order_by_param TEXT[] DEFAULT ARRAY['name'],
    order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
    limit_param INTEGER DEFAULT NULL,
    offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
    id_type_benefit UUID,
    name VARCHAR,
    description TEXT,
    total_count BIGINT
) AS $$
DECLARE
    base_query TEXT;
    count_query TEXT;
    final_query TEXT;
    total BIGINT;
BEGIN
    -- Base query to select type benefits with filters
    base_query := '
    WITH limited_type_benefits AS (
        SELECT
            id_type_benefit,
            name,
            description
        FROM type_benefit
        WHERE (
            $1 IS NULL OR
            id_type_benefit::text = $1 OR
            LOWER(name) LIKE LOWER(''%'' || $1 || ''%'') OR
            LOWER(description) LIKE LOWER(''%'' || $1 || ''%'')
        )
        ORDER BY
            CASE WHEN $2[1] = ''name'' AND $3[1] = ''ASC'' THEN name END ASC NULLS LAST,
            CASE WHEN $2[1] = ''name'' AND $3[1] = ''DESC'' THEN name END DESC NULLS LAST,
            CASE WHEN $2[1] = ''description'' AND $3[1] = ''ASC'' THEN description END ASC NULLS LAST,
            CASE WHEN $2[1] = ''description'' AND $3[1] = ''DESC'' THEN description END DESC NULLS LAST
    ';

    IF limit_param IS NOT NULL AND offset_param IS NOT NULL THEN
        base_query := base_query || '
        LIMIT $4 OFFSET $5';
    END IF;

    base_query := base_query || '
    )
    SELECT *
    FROM limited_type_benefits';

    -- Query to count total type benefits
    count_query := '
    SELECT COUNT(*)
    FROM type_benefit
    WHERE (
        $1 IS NULL OR
        id_type_benefit::text = $1 OR
        LOWER(name) LIKE LOWER(''%'' || $1 || ''%'') OR
        LOWER(description) LIKE LOWER(''%'' || $1 || ''%'')
    )';

    -- Execute count
    EXECUTE count_query
    USING global_search_param
    INTO total;

    -- Combine count with paginated results
    final_query := 'SELECT sub.*, ' || total || '::BIGINT as total_count FROM (' || base_query || ') sub';

    RETURN QUERY EXECUTE final_query
    USING global_search_param, order_by_param, order_direction_param, limit_param, offset_param;
END;
$$ LANGUAGE plpgsql;