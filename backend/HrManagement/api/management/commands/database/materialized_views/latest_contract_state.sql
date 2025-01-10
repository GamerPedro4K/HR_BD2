DROP MATERIALIZED VIEW IF EXISTS latest_contract_state_materialized_view;
CREATE MATERIALIZED VIEW latest_contract_state_materialized_view AS (
    SELECT *
    FROM contract_state_contract
    WHERE (contract_state_contract.id_contract, contract_state_contract.created_at) IN (
        SELECT contract_state_contract.id_contract, MAX(created_at)
        FROM contract_state_contract
        WHERE contract_state_contract.deleted_at IS NULL
        GROUP BY contract_state_contract.id_contract
    )
);

CREATE UNIQUE INDEX ON latest_contract_state_materialized_view (id_contract_state_contract);