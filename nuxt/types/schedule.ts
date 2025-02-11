export interface ScheduleInterface {
    id_employee: string;
    workSchedule: WorkSchedule;    
}

export interface WorkSchedule {
    mondey: WorkShift;
    tuesday: WorkShift;
    wednesday: WorkShift;
    thursday: WorkShift;
    friday: WorkShift;
    saturday: WorkShift;
    sunday: WorkShift;
}

export interface WorkShift {
    start: string;
    end: string;
}