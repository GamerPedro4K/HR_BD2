CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS departments (
    id_department UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS roles (
    id_role UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_department UUID NOT NULL,
    id_auth_group INTEGER NOT NULL,
    role_name VARCHAR(100),
    hex_color VARCHAR(7),
    description TEXT,
    FOREIGN KEY (id_department) REFERENCES departments(id_department),
    FOREIGN KEY (id_auth_group) REFERENCES auth_group(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS training_types (
    id_training_type UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    hours INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS training_type_role (
    id_training_type UUID NOT NULL,
    id_role UUID NOT NULL,
    PRIMARY KEY (id_training_type, id_role),
    FOREIGN KEY (id_training_type) REFERENCES training_types(id_training_type),
    FOREIGN KEY (id_role) REFERENCES roles(id_role),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    id_auth_user INTEGER NOT NULL UNIQUE,
    id_employee UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(50) NOT NULL,
    src VARCHAR(200) NOT NULL,
    birth_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS employee_location (
    id_location UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL UNIQUE,
    address VARCHAR(200),
    city VARCHAR(100),
    district VARCHAR(20),
    country VARCHAR(2),
    zip_code VARCHAR(8),
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);


CREATE TABLE IF NOT EXISTS contract_type (
    id_contract_type UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_type_name VARCHAR(100),
    description TEXT,
    termination_notice_period NUMERIC(10, 2),
    overtime_eligible BOOLEAN,
    benefits_eligible BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS contract (
    id_contract UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_role UUID NOT NULL,
    id_contract_type UUID NOT NULL,
    FOREIGN KEY (id_role) REFERENCES roles(id_role),
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_contract_type) REFERENCES contract_type(id_contract_type),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS type_benefit (
    id_type_benefit UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS contract_benefits (
    id_contract_benefit UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_contract UUID NOT NULL,
    id_type_benefit UUID NOT NULL,
    benefit_amount NUMERIC(10, 2),
    FOREIGN KEY (id_contract) REFERENCES contract(id_contract),
    FOREIGN KEY (id_type_benefit) REFERENCES type_benefit(id_type_benefit),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS salary_history (
    id_salary_history UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_contract UUID NOT NULL,
    id_employee_aproved_by UUID NOT NULL,
    base_salary NUMERIC(10, 2),
    extra_hour_rate NUMERIC(10, 2),
    start_date DATE,
    FOREIGN KEY (id_contract) REFERENCES contract(id_contract),
    FOREIGN KEY (id_employee_aproved_by) REFERENCES employees(id_employee),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS contract_state (
    id_contract_state UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    icon VARCHAR(100) NOT NULL,
    hex_color VARCHAR(7) NOT NULL,
    state VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS contract_state_contract (
    id_contract_state_contract UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_contract_state UUID NOT NULL,
    id_contract UUID NOT NULL,
    FOREIGN KEY (id_contract_state) REFERENCES contract_state(id_contract_state),
    FOREIGN KEY (id_contract) REFERENCES contract(id_contract),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS contract_leave_type (
    id_leave_type UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    leave_type VARCHAR(100),
    description TEXT,
    is_paid BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS contract_leaves (
    id_contract_leave UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_contract UUID NOT NULL,
    id_leave_type UUID NOT NULL,
    hours NUMERIC(10, 2),
    hours_taken NUMERIC(10, 2),
    FOREIGN KEY (id_contract) REFERENCES contract(id_contract),
    FOREIGN KEY (id_leave_type) REFERENCES contract_leave_type(id_leave_type),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS vacations (
    id_vacation UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    aproved_date DATE DEFAULT CURRENT_TIMESTAMP,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS certificate_types (
    id_certificate_type UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(100) NOT NULL,
    hex_color VARCHAR(7) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS certifications (
    id_certification UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_certificate_type UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_certificate_type) REFERENCES certificate_types(id_certificate_type),
    issuing_organization VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    expiration_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS employee_hierarchy (
    id_employee_hierarchy UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_employee_superior UUID,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_employee_superior) REFERENCES employees(id_employee),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS trainings (
    id_training UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_training_type UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_training_type) REFERENCES training_types(id_training_type),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS absence_reason (
    id_absence_reason UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_employee_supervisor UUID NOT NULL,
    id_employee_substitute UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_employee_supervisor) REFERENCES employees(id_employee),
    FOREIGN KEY (id_employee_substitute) REFERENCES employees(id_employee),
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS payment_methods (
    id_payment_method UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(100) NOT NULL,
    hex_color VARCHAR(7) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id_payment UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_employee_supervisor UUID NOT NULL,
    id_payment_method UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_employee_supervisor) REFERENCES employees(id_employee),
    FOREIGN KEY (id_payment_method) REFERENCES payment_methods(id_payment_method),
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    extra_amount DECIMAL(10,2),
    deduction_amount DECIMAL(10,2),
    bonus_amount DECIMAL(10,2),
    payment_note TEXT,
    src VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS deductions (
    id_deduction UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_payment UUID,
    id_absence_reason UUID NOT NULL,
    FOREIGN KEY (id_payment) REFERENCES payments(id_payment),
    FOREIGN KEY (id_absence_reason) REFERENCES absence_reason(id_absence_reason),
    deduction_note TEXT,
    amount DECIMAL(10,2) NOT NULL,
    deduction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS bonuses (
    id_bonus UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_payment UUID,
    id_employee UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_payment) REFERENCES payments(id_payment),
    bonus_note TEXT,
    amount DECIMAL(10,2) NOT NULL,
    bonus_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
