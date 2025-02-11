CREATE OR REPLACE FUNCTION get_all_contract_leave_types(
    global_search_param VARCHAR DEFAULT NULL,
    order_by_param TEXT[] DEFAULT ARRAY['leave_type'],
    order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
    limit_param INTEGER DEFAULT NULL,
    offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
    id_leave_type UUID,
    leave_type VARCHAR,
    description TEXT,
    is_paid BOOLEAN,
    total_count BIGINT
) AS $$
DECLARE
    base_query TEXT;
    count_query TEXT;
    final_query TEXT;
    total BIGINT;
BEGIN
    -- Base query to select leave types with filters
    base_query := '
    WITH limited_contract_leave_types AS (
        SELECT
            id_leave_type,
            leave_type,
            description,
            is_paid
        FROM contract_leave_type
        WHERE deleted_at IS NULL
        AND (
            $1 IS NULL OR
            id_leave_type::text = $1 OR
            LOWER(leave_type) LIKE LOWER(''%'' || $1 || ''%'') OR
            LOWER(description) LIKE LOWER(''%'' || $1 || ''%'')
        )
        ORDER BY
            CASE WHEN $2[1] = ''leave_type'' AND $3[1] = ''ASC'' THEN leave_type END ASC NULLS LAST,
            CASE WHEN $2[1] = ''leave_type'' AND $3[1] = ''DESC'' THEN leave_type END DESC NULLS LAST,
            CASE WHEN $2[1] = ''description'' AND $3[1] = ''ASC'' THEN description END ASC NULLS LAST,
            CASE WHEN $2[1] = ''description'' AND $3[1] = ''DESC'' THEN description END DESC NULLS LAST,
            CASE WHEN $2[1] = ''is_paid'' AND $3[1] = ''ASC'' THEN is_paid END ASC NULLS LAST,
            CASE WHEN $2[1] = ''is_paid'' AND $3[1] = ''DESC'' THEN is_paid END DESC NULLS LAST
    ';

    IF limit_param IS NOT NULL AND offset_param IS NOT NULL THEN
        base_query := base_query || '
        LIMIT $4 OFFSET $5';
    END IF;

    base_query := base_query || '
    )
    SELECT *
    FROM limited_contract_leave_types';

    -- Query to count total leave types
    count_query := '
    SELECT COUNT(*)
    FROM contract_leave_type
    WHERE deleted_at IS NULL
    AND (
        $1 IS NULL OR
        id_leave_type::text = $1 OR
        LOWER(leave_type) LIKE LOWER(''%'' || $1 || ''%'') OR
        LOWER(description) LIKE LOWER(''%'' || $1 || ''%'')
    )';

    -- Execute the count
    EXECUTE count_query
    USING global_search_param
    INTO total;

    -- Combine count with paginated results
    final_query := 'SELECT sub.*, ' || total || '::BIGINT as total_count FROM (' || base_query || ') sub';

    RETURN QUERY EXECUTE final_query
    USING global_search_param, order_by_param, order_direction_param, limit_param, offset_param;
END;
$$ LANGUAGE plpgsql;