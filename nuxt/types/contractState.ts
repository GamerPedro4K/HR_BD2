export interface ContractState {
    id_contract_state: string;
    icon: string;
    hex_color: string;
    state: string;
    description?: string;
}

export interface ContractStateListResponse {
    contract_states: ContractState[];
}