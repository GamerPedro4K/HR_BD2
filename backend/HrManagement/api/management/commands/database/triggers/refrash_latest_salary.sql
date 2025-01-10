CREATE OR REPLACE FUNCTION refresh_latest_salary()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY latest_salary_materialized_view;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_refresh_latest_salary
AFTER INSERT ON salary_history
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_latest_salary();

