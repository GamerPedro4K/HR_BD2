export interface Department {
    id_department: string;
    name: string;
    description: string;
    roles: Role[];
 }
 
 export interface Role {
    id_role: string;
    role_name: string;
    hex_color: string;
    description: string;
    training_types: TrainingType[];
 }
 
 export interface TrainingType {
    id_training_type: string;
    name: string;
    description: string;
    hours: number;
 }
 
 export interface DepartmentListResponse {
    departments: Department[];
    total_count: number;
 }
 
 export interface DepartmentParams {
    limit?: number;
    offset?: number;
    order_by?: string;
    order_direction?: string;
    global_search?: string;
 }
 export interface DepartmentFormData {
   name: string;
   description?: string;
 }
 
 export interface DepartmentCreateResponse {
   id_department: string;
   message: string;
 }