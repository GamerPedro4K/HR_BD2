export interface ContractState {
    id_contract_state: string;
    icon: string;
    hex_color: string;
    state: string;
    description?: string;
}

export interface ContractStateListResponse {
    contract_states: ContractState[];
    total_count: number;
}

export interface ContractStateContractParams {
    limit?: number;
    offset?: number;
}

export interface ContractStateContract {
    id_contract_state_contract: string;
    id_contract: string;
    created_at: string;
    updated_at: string;
}
export interface ContractStateContractItem {
    contract_state: ContractStateContract;
    state: ContractState;
}

export interface ContractStateContractResponse {
    data: ContractStateContractItem[];
    count: number;
}

export interface ContractStateQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}