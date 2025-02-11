export interface AttendanceInterfaceParams {
    limit?: number;
    offset?: number;
}

export interface AttendanceInterfaceResponse {
    data: AttendanceInterface[];
    count: number;
}

export interface AttendanceInterface {
    id_employee: string; 
    date: string; 
    sessions: Session[]; 
}

export interface Session {
    checkin: string; 
    checkout: string; 
}