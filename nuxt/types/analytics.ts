export interface PaymentAnalytics {
    month_name: string;
    total_employees_paid: number;
    total_base_salary: string;
    total_bonus_amount: string;
    total_deduction_amount: string;
    net_payment_amount: string;
    average_payment: string;
    min_payment: string;
    max_payment: string;
    employees_with_bonus: number;
    employees_with_deduction: number;
}

export interface AbsenceAnalytics {
    employee_name: string;
    total_absences: number;
    total_days_absent: number;
}

export interface DepartmentSalary {
    department_name: string;
    employee_count: number;
    avg_salary: string;
    min_salary: string;
    max_salary: string;
}

export interface DepartmentCount {
    department_name: string;
    total_employees: number;
}

export interface DashboardData {
    current_month_payments: PaymentAnalytics[];
    top_absences: AbsenceAnalytics[];
    department_salaries: DepartmentSalary[];
    department_counts: DepartmentCount[];
}