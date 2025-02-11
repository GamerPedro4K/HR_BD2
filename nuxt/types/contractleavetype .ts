export interface ContractLeaveType {
    id_leave_type: string;
    leave_type: string;
    description: string;
    is_paid: boolean;
}

export interface ContractLeaveTypeListResponse {
    contract_leave_types: ContractLeaveType[];
    total_count: number;
}

export interface ContractLeaveTypeQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}