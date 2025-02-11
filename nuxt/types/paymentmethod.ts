export interface PaymentMethod {
    id_payment_method: string;
    name: string;
    description: string;
    icon: string;
    hex_color: string;
}

export interface PaymentMethodListResponse {
    payment_methods: PaymentMethod[];
    total_count: number;
}

export interface PaymentMethodQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}