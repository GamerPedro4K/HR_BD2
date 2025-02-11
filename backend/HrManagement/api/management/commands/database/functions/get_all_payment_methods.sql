CREATE OR REPLACE FUNCTION get_all_payment_methods(
    global_search_param VARCHAR DEFAULT NULL,
    order_by_param TEXT[] DEFAULT ARRAY['name'],
    order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
    limit_param INTEGER DEFAULT NULL,
    offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
    id_payment_method UUID,
    name VARCHAR,
    description TEXT,
    icon VARCHAR,
    hex_color VARCHAR,
    total_count BIGINT
) AS $$
DECLARE
    base_query TEXT;
    count_query TEXT;
    final_query TEXT;
    total BIGINT;
BEGIN
    -- Base query to select payment methods with filters
    base_query := '
    WITH limited_payment_methods AS (
        SELECT
            id_payment_method,
            name,
            description,
            icon,
            hex_color
        FROM payment_methods
        WHERE (
            $1 IS NULL OR
            id_payment_method::text = $1 OR
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
    FROM limited_payment_methods';

    -- Query to count total payment methods
    count_query := '
    SELECT COUNT(*)
    FROM payment_methods
    WHERE (
        $1 IS NULL OR
        id_payment_method::text = $1 OR
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