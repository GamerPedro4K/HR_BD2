export interface TrainingType {
    id_training_type: string;
    name: string;
    description: string;
    hours: number;
}

export interface TrainingTypesResponse {
    training_types: TrainingType[];
}
