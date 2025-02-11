import type { TrainingType } from "./training";

export interface Role {
    id_role: string;
    role_name: string;
    hex_color: string;
    description: string;
    training_types: TrainingType[]; 
}

export interface RoleRequst {
    id_role: string;
    id_department: string;
    id_auth_group: number;
    role_name: string;
    hex_color?: string;
    description?: string;
    department_name: string;
    training_types: TrainingType[];
}

export interface RoleQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}

export interface RoleListResponse {
    roles: RoleRequst[];
    total_count: number;
}

export interface RoleSubmission {
    id_department: string;
    id_auth_group: number;
    role_name: string;
    hex_color?: string;
    description?: string;
}