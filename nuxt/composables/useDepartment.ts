import { useRuntimeConfig } from '#app';
import type { Department, DepartmentCreateResponse, DepartmentFormData, DepartmentListResponse, DepartmentParams } from '~/types/department';

export function useDepartment() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: {
          severity: 'error',
          summary: 'Erro de Ligação',
          detail: 'Por favor, verifique a sua ligação à Internet.',
          life: 3000
        },
        errorGeneric: {
          severity: 'error',
          summary: 'Erro',
          detail: 'Ocorreu um erro.',
          life: 3000
        },
        successCreate: {
          severity: 'success',
          summary: 'Sucesso',
          detail: 'Departamento criado com sucesso.',
          life: 3000
        },
        successUpdate: {
          severity: 'success',
          summary: 'Sucesso',
          detail: 'Departamento atualizado com sucesso.',
          life: 3000
        },
        successDelete: {
          severity: 'success',
          summary: 'Sucesso',
          detail: 'Departamento eliminado com sucesso.',
          life: 3000
        }
      };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getDepartments = async (params: DepartmentParams): Promise<DepartmentListResponse> => {
        try {
            const config = useRuntimeConfig();
            const queryParams = new URLSearchParams();
            
            if (params.limit) queryParams.append('limit', params.limit.toString());
            if (params.offset) queryParams.append('offset', params.offset.toString());
            if (params.order_by) queryParams.append('order_by', params.order_by);
            if (params.order_direction) queryParams.append('order_direction', params.order_direction);
            if (params.global_search) queryParams.append('global_search', params.global_search);
     
            const url = `${config.public.apiUrl}/api/departments/?${queryParams.toString()}`;
     
            const response = await $fetch<DepartmentListResponse>(url, {
                method: 'GET',
                headers: getAuthHeaders(),
            });
     
            return response || { departments: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { departments: [], total_count: 0 };
        }
    };

    const getDepartment = async (id: string): Promise<Department | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<Department>(`${config.public.apiUrl}/api/departments/${id}/`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return null;
        }
    };

    const createDepartment = async (data: DepartmentFormData): Promise<DepartmentCreateResponse> => {
        try {
          const config = useRuntimeConfig();
          const response = await $fetch<DepartmentCreateResponse>(`${config.public.apiUrl}/api/departments/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              ...getAuthHeaders(),
            },
            body: data,
          });
    
          $toast.add(message.successCreate);
          return response;
        } catch (error) {
          console.error('Error creating department:', error);
          $toast.add(message.errorGeneric);
          throw error;
        }
      };
    
      const updateDepartment = async (id: string, data: DepartmentFormData) => {
        try {
          const config = useRuntimeConfig();
          const response = await $fetch(`${config.public.apiUrl}/api/departments/${id}/`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              ...getAuthHeaders(),
            },
            body: data,
          });
    
          $toast.add(message.successUpdate);
          return response;
        } catch (error) {
          console.error('Error updating department:', error);
          $toast.add(message.errorGeneric);
          throw error;
        }
      };
    
      const deleteDepartment = async (id: string) => {
        try {
          const config = useRuntimeConfig();
          await $fetch(`${config.public.apiUrl}/api/departments/${id}/`, {
            method: 'DELETE',
            headers: getAuthHeaders(),
          });
    
          $toast.add(message.successDelete);
        } catch (error) {
          console.error('Error deleting department:', error);
          $toast.add(message.errorGeneric);
          throw error;
        }
      };
    
    return { getDepartments, getDepartment, createDepartment, updateDepartment, deleteDepartment };
}
