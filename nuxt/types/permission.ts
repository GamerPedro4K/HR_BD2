export interface Permission {
    id: number;
    name: string;
    codename: string;
}

export interface PermissionListResponse {
    permissions: Permission[];
    total_count: number;
}

export interface PermissionQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}