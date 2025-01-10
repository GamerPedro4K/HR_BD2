export interface SalaryHistory {
    id_salary_history: string;
    id_contract: string;
    id_employee_aproved_by: string;
    base_salary: number;
    extra_hour_rate: number;
    start_date: string;
    created_at: string;
    updated_at: string;
    deleted_at: string | null;
    id_employee: string;
}

export interface SalaryHistoryListResponse {
    salaryHistories: SalaryHistory[];
}
