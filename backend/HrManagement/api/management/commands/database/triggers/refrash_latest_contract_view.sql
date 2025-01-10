CREATE OR REPLACE FUNCTION refresh_latest_contract()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY latest_contract_materialized_view;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_refresh_latest_contract
AFTER INSERT ON contract
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_latest_contract();

