export interface ContractType {
    id_contract_type: string;
    contract_type_name: string;
    description: string;
    termination_notice_period: number;
    overtime_eligible: boolean;
    benefits_eligible: boolean;
}

export interface ContractTypeListResponse {
    contract_types: ContractType[];
    total_count: number;
}

export interface ContractTypeQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}