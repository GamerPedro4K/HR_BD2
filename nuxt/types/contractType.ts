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
}

export interface ContractTypeQueryParams {
    contract_type_name?: string; // Optional filter by contract type name
    limit?: number;             // Optional limit for pagination
    offset?: number;            // Optional offset for pagination
}
