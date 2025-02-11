export interface TrainingType {
    id_training_type: string;
    name: string;
    description: string;
    hours?: number;
}
export interface TrainingTypeListResponse {
    training_types: TrainingType[];
    total_count: number;
}

export interface TrainingTypeQueryParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    global_search?: string;
}

export interface TrainingTypeSubmission {
    name: string;
    description: string;
    hours?: number;
}