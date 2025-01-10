export interface CertificateType {
    id_certificate_type: string;
    name: string;
    description: string;
    icon: string;
    hex_color: string;
}

export interface CertificateTypesResponse {
    certificate_types: CertificateType[];
}
