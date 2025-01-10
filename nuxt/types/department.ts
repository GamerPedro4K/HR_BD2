import type { Role } from './roles';

export interface Department {
    id_department: string;
    name: string;
    description: string;
    roles: Role[]; // Array of roles within the department
}

export interface DepartmentListResponse {
    departments: Department[];
}



