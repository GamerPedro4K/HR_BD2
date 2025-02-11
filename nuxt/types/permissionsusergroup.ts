interface Permission {
    id: number;
    name: string;
    codename: string;
}

interface Group {
    group_id: number;
    group_name: string;
    permissions: Permission[];
}

export interface Employee {
    id_employee: string;
    src: string;
    name: string;
    groups: Group[];
}

export interface EmployeePermissionsResponse {
    employees: Employee[];
    total_count: number;
}

export interface EmployeePermissionsQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}