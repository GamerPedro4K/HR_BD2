export interface Vacation {
    id_vacation: string;
    id_employee: string;
    id_employee_substitute: string;
    aproved_by_employee_id: string;
    aproved_date: string;
    start_date: string;
    end_date: string;
    created_at: string;
    updated_at: string;
    deleted_at: string | null;
    id_department: string;
    department_name: string;
    employee_name: string;
    email: string;
  }
  
  export interface VacationListResponse {
    vacations: Vacation[];
  }
  