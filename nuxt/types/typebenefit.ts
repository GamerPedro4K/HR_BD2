export interface TypeBenefit {
    id_type_benefit: string;
    name: string;
    description: string;
}

export interface TypeBenefitListResponse {
    type_benefits: TypeBenefit[];
    total_count: number;
}

export interface TypeBenefitQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}