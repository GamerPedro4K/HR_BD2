import type { TrainingType } from "./training";

export interface Role {
    id_role: string;
    role_name: string;
    hex_color: string;
    description: string;
    training_types: TrainingType[]; 
}