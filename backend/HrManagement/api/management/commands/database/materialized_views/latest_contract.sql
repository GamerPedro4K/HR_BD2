DROP MATERIALIZED VIEW IF EXISTS latest_contract_materialized_view;
CREATE MATERIALIZED VIEW latest_contract_materialized_view AS (
    SELECT *
    FROM contract
    WHERE (contract.id_employee, contract.created_at) IN (
        SELECT id_employee, MAX(created_at)
        FROM contract
        WHERE contract.deleted_at IS NULL
        GROUP BY contract.id_employee
    )
);

CREATE UNIQUE INDEX ON latest_contract_materialized_view (id_contract);