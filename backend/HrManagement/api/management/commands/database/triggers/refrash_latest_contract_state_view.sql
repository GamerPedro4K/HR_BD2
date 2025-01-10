CREATE OR REPLACE FUNCTION refresh_latest_contract_state() 
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY latest_contract_state_materialized_view;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trigger_refresh_latest_contract_state
AFTER INSERT ON contract_state_contract
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_latest_contract_state();
