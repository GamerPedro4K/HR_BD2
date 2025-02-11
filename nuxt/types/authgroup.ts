export interface AuthGroup {
    id: number;
    name: string;
    permissions?: Permission[];

}

export interface AuthGroupListResponse {
    auth_groups: AuthGroup[];
    total_count: number;
}

export interface AuthGroupFormData {
    name: string;
}


export interface Permission {
    id: number;
    name: string;
    codename: string;
    content_type: string;
}

export interface AuthGroupQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}