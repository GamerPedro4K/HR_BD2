export interface Employee {
    id: number;
    employee_name: string;
    role_name: string;
    department_name: string;
    status_name: string;
    role_hex_color?: string;
    state_hex_color?: string;
    icon?: string;
}

export interface EmployeeListResponse {
    value: EmployeeListResponse | null;
    employees: Employee[];
    total_count: number;
}

export interface EmployeeQueryParams {
    name?: string;
    id?: number;
    department_id?: number; 
    role_id?: number;
    status_id?: number;
    order_by?: string;
    order_direction?: 'ASC' | 'DESC';
    limit?: number;
    offset?: number;
    global_search?: string;
}

export interface EmployeeSubmission {
    employee: {
      id_employee: string | null | undefined;
      username: string;
      password: string;
      first_name: string;
      last_name: string;
      email: string;
      phone: string;
      img_src: string;
      birth_date: string | Date;
      id_group: number;
    };
    employee_address: {
      street: string;
      zip_code: string;
      city: string;
      district: string;
      country: string;
    };
    trainings: {
      start_date: string | Date;
      end_date: string | Date;
      id_training_type: string;
    }[];
    certificates: {
      id_certificate_type: string;
      name: string;
    }[];
    vacations:{
      start_date: string | Date | undefined;
      end_date: string | Date | undefined;
    };
    salary:{
      base_salary: number,
      extra_hour_rate: number,
      start_date: String | Date,
    }
    contract:{
      id_contract_type: string | null;
      id_contract_state: string | null;
      id_role: string | null;
    }
  }
  
  export interface FindEmployee {
    id_employee: string;
    employee_name: string;
    phone: string;
    photo: string;
    email: string;
    birth_date: string;
    date_joined: string;
    location: {
      city: string;
      country: string;
      district: string;
      address: string;
      zip_code: string;
    };
    contract: {
      id_contract: string;
      created_at: string;
      salary: {
        id_salary: string;
        id_aproved_by: string;
        base_salary: number;
        extra_hour_rate: number;
        start_date: string;
      };
      contract_type: {
        id_contract_type: string;
        contract_type_name: string;
        description: string;
      };
      contract_state: {
        id_contract_state_contract: string;
        id_contract_state: string;
        state_name: string;
        description: string;
        hex_color: string;
        icon: string;
      };
      role: {
        id_role: string;
        role_name: string;
        hex_color: string;
        description: string;
      };
      department: {
        id_department: string;
        department_name: string;
        description: string;
      };
    };
    trainings: {
      id_training: string;
      start_date: string;
      end_date: string;
      training_type: {
        id_training_type: string;
        training_type_name: string;
        description: string;
        hours: number;
      };
    }[];
    certifications: {
      id_certification: string;
      issue_date: string;
      expiration_date: string | null;
      certificate_type: {
        id_certificate_type: string;
        certificate_type_name: string;
        description: string;
        icon: string;
        hex_color: string;
      };
      issuing_organization: string;
    }[];
  }
  