DROP TABLE IF EXISTS bonuses cascade;
DROP TABLE IF EXISTS deductions cascade;
DROP TABLE IF EXISTS payments cascade;
DROP TABLE IF EXISTS payment_methods cascade;
DROP TABLE IF EXISTS absence_reason cascade;
DROP TABLE IF EXISTS trainings cascade;
DROP TABLE IF EXISTS employee_hierarchy cascade;
DROP TABLE IF EXISTS certifications cascade;
DROP TABLE IF EXISTS certificate_types cascade;
DROP TABLE IF EXISTS vacations cascade;
DROP TABLE IF EXISTS contract_leave_type cascade;
DROP TABLE IF EXISTS contract_state_contract cascade;
DROP TABLE IF EXISTS contract_state cascade;
DROP TABLE IF EXISTS salary_history cascade;
DROP TABLE IF EXISTS contract_benefits cascade;
DROP TABLE IF EXISTS type_benefit cascade;
DROP TABLE IF EXISTS contract cascade;
DROP TABLE IF EXISTS contract_type cascade;
DROP TABLE IF EXISTS employee_location cascade;
DROP TABLE IF EXISTS employees cascade;
DROP TABLE IF EXISTS training_type_role cascade;
DROP TABLE IF EXISTS training_types cascade;
DROP TABLE IF EXISTS roles cascade;
DROP TABLE IF EXISTS departments cascade;


-- Drop funções e triggers
DROP FUNCTION IF EXISTS update_payment_totals() CASCADE;
DROP TRIGGER IF EXISTS trg_update_payment_totals ON payments;

DROP FUNCTION IF EXISTS refresh_latest_salary() CASCADE;
DROP TRIGGER IF EXISTS trigger_refresh_latest_salary ON contract;

DROP FUNCTION IF EXISTS refresh_latest_contract() CASCADE;
DROP TRIGGER IF EXISTS trigger_refresh_latest_contract ON contract;

DROP FUNCTION IF EXISTS refresh_latest_contract_state() CASCADE;
DROP TRIGGER IF EXISTS trigger_refresh_latest_contract_state ON contract_state_contract;

-- Drop views materializadas
DROP MATERIALIZED VIEW IF EXISTS latest_salary_materialized_view CASCADE;
DROP MATERIALIZED VIEW IF EXISTS latest_contract_materialized_view CASCADE;
DROP MATERIALIZED VIEW IF EXISTS latest_contract_state_materialized_view CASCADE;