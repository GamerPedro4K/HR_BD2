export interface CertificateType {
    id_certificate_type: string;
    name: string;
    description: string;
    icon: string;
    hex_color: string;
}

export interface CertificateTypeListResponse {
    certificate_types: CertificateType[];
    total_count: number;
}

export interface CertificateTypeQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}