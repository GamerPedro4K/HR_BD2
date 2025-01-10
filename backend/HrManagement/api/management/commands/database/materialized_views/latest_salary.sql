DROP MATERIALIZED VIEW IF EXISTS latest_salary_materialized_view;
CREATE MATERIALIZED VIEW latest_salary_materialized_view AS (
    SELECT *
    FROM salary_history
    WHERE (salary_history.id_contract, salary_history.created_at) IN (
        SELECT salary_history.id_contract, MAX(created_at)
        FROM salary_history
        WHERE salary_history.deleted_at IS NULL
        GROUP BY salary_history.id_contract
    )
);

CREATE UNIQUE INDEX ON latest_salary_materialized_view (id_salary_history);