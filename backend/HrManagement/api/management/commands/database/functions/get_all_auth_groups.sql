CREATE OR REPLACE FUNCTION get_all_auth_groups(
    global_search_param VARCHAR DEFAULT NULL,
    order_by_param TEXT[] DEFAULT ARRAY['name'],
    order_direction_param TEXT[] DEFAULT ARRAY['ASC'],
    limit_param INTEGER DEFAULT NULL,
    offset_param INTEGER DEFAULT NULL
)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    permissions JSONB,
    total_count BIGINT
) AS $$
DECLARE
    base_query TEXT;
    count_query TEXT;
    final_query TEXT;
    total BIGINT;
BEGIN
    -- Base query with group permissions as JSONB array
    base_query := '
    WITH group_permissions AS (
        SELECT
            ag.id,
            ag.name,
            COALESCE(
                jsonb_agg(
                    jsonb_build_object(
                        ''id'', ap.id,
                        ''name'', ap.name,
                        ''codename'', ap.codename
                    )
                ) FILTER (WHERE ap.id IS NOT NULL),
                ''[]''::jsonb
            ) as permissions
        FROM auth_group ag
        LEFT JOIN auth_group_permissions agp ON ag.id = agp.group_id
        LEFT JOIN auth_permission ap ON agp.permission_id = ap.id
        WHERE (
            $1 IS NULL OR
            ag.id::text = $1 OR
            LOWER(ag.name) LIKE LOWER(''%'' || $1 || ''%'') OR
            LOWER(ap.name) LIKE LOWER (''%'' || $1 || ''%'') OR
            LOWER(ap.codename) LIKE LOWER (''%'' || $1 || ''%'')
        )
        GROUP BY ag.id, ag.name
        ORDER BY
            CASE WHEN $2[1] = ''name'' AND $3[1] = ''ASC'' THEN ag.name END ASC NULLS LAST,
            CASE WHEN $2[1] = ''name'' AND $3[1] = ''DESC'' THEN ag.name END DESC NULLS LAST,
            CASE WHEN $2[1] = ''id'' AND $3[1] = ''ASC'' THEN ag.id END ASC NULLS LAST,
            CASE WHEN $2[1] = ''id'' AND $3[1] = ''DESC'' THEN ag.id END DESC NULLS LAST
    ';

    IF limit_param IS NOT NULL AND offset_param IS NOT NULL THEN
        base_query := base_query || '
        LIMIT $4 OFFSET $5';
    END IF;

    base_query := base_query || '
    )
    SELECT *
    FROM group_permissions';

    -- Count query
    count_query := '
    SELECT COUNT(*)
    FROM auth_group ag
    WHERE (
        $1 IS NULL OR
        ag.id::text = $1 OR
        LOWER(ag.name) LIKE LOWER(''%'' || $1 || ''%'')
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