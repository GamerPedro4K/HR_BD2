#! permissions.py
#? python manage.py seed --seeder 2_permissions
# This file is used to seed the permissions table with fake data.

from django.db import connection

PERMISSIONS = [
    ## Tipos de Certificado
    ("view_all_certificate_types", "Pode visualizar todos os tipos de certificado"),
    ("view_certificate_type", "Pode visualizar um tipo de certificado"),
    ("create_certificate_type", "Pode criar um tipo de certificado"),
    ("update_certificate_type", "Pode atualizar um tipo de certificado"),
    ("delete_certificate_type", "Pode deletar um tipo de certificado"),
    
    ## Tipos de Licença Contratual
    ("view_all_contract_leave_types", "Pode visualizar todos os tipos de licença contratual"),
    ("view_contract_leave_type", "Pode visualizar um tipo de licença contratual"),
    ("create_contract_leave_type", "Pode criar um tipo de licença contratual"),
    ("update_contract_leave_type", "Pode atualizar um tipo de licença contratual"),
    ("delete_contract_leave_type", "Pode deletar um tipo de licença contratual"),
    
    ## Estados Contratuais
    ("view_all_contract_states", "Pode visualizar todos os estados contratuais"),
    ("view_contract_state", "Pode visualizar um estado contratual"),
    ("create_contract_state", "Pode criar um estado contratual"),
    ("update_contract_state", "Pode atualizar um estado contratual"),
    ("delete_contract_state", "Pode deletar um estado contratual"),
    
    ## Tipos de Contrato
    ("view_all_contract_types", "Pode visualizar todos os tipos de contrato"),
    ("view_contract_type", "Pode visualizar um tipo de contrato"),
    ("create_contract_type", "Pode criar um tipo de contrato"),
    ("update_contract_type", "Pode atualizar um tipo de contrato"),
    ("delete_contract_type", "Pode deletar um tipo de contrato"),
    
    ## Departamentos
    ("view_all_departments", "Pode visualizar todos os departamentos"),
    ("view_department", "Pode visualizar um departamento"),
    ("create_department", "Pode criar um departamento"),
    ("update_department", "Pode atualizar um departamento"),
    ("delete_department", "Pode deletar um departamento"),
    
    ## Funcionários
    ("view_all_employees", "Pode visualizar todos os funcionários"),
    ("view_employee", "Pode visualizar um funcionário"),
    ("view_employee_contracts", "Pode visualizar os contratos de funcionários"),
    ("create_employee", "Pode criar um funcionário"),
    ("update_employee", "Pode atualizar um funcionário"),
    
    ## Métodos de Pagamento
    ("view_all_payment_methods", "Pode visualizar todos os métodos de pagamento"),
    ("view_payment_method", "Pode visualizar um método de pagamento"),
    ("create_payment_method", "Pode criar um método de pagamento"),
    ("update_payment_method", "Pode atualizar um método de pagamento"),
    ("delete_payment_method", "Pode deletar um método de pagamento"),
    
    ## Tipos de Treinamento
    ("view_all_training_types", "Pode visualizar todos os tipos de treinamento"),
    ("view_training_type", "Pode visualizar um tipo de treinamento"),
    ("create_training_type", "Pode criar um tipo de treinamento"),
    ("update_training_type", "Pode atualizar um tipo de treinamento"),
    ("delete_training_type", "Pode deletar um tipo de treinamento"),
    
    ## Benefícios
    ("view_all_type_benefits", "Pode visualizar todos os tipos de benefícios"),
    ("view_type_benefit", "Pode visualizar um tipo de benefício"),
    ("create_type_benefit", "Pode criar um tipo de benefício"),
    ("update_type_benefit", "Pode atualizar um tipo de benefício"),
    ("delete_type_benefit", "Pode deletar um tipo de benefício"),

    ## Horas Extras
    ("view_all_extra_hours", "Pode visualizar todas as horas extras"),
    ("view_extra_hours", "Pode visualizar uma hora extra"),
    ("create_extra_hours", "Pode criar uma hora extra"),
    ("update_extra_hours", "Pode atualizar uma hora extra"),
    ("delete_extra_hours", "Pode deletar uma hora extra"),

    ## Schedule
    ("view_all_schedules", "Pode visualizar todos os horários"),
    ("view_schedule", "Pode visualizar um horário"),
    ("create_schedule", "Pode criar um horário"),
    ("update_schedule", "Pode atualizar um horário"),
    ("delete_schedule", "Pode deletar um horário"),

    ## Attendance
    ("view_all_attendance", "Pode visualizar todas as presenças"),
    ("view_attendance", "Pode visualizar uma presença"),
    ("create_attendance", "Pode criar uma presença"),
    ("update_attendance", "Pode atualizar uma presença"),
    ("delete_attendance", "Pode deletar uma presença"),

    ## Vacations
    ("view_all_vacations", "Pode visualizar todas as férias"),
    ("view_vacation", "Pode visualizar uma férias"),
    ("create_vacation", "Pode criar uma férias"),
    ("update_vacation", "Pode atualizar uma férias"),
    ("delete_vacation", "Pode deletar uma férias"),

    ## Absence Reason
    ("view_all_absence_reasons", "Pode visualizar todos os motivos de ausência"),
    ("view_absence_reason", "Pode visualizar um motivo de ausência"),
    ("create_absence_reason", "Pode criar um motivo de ausência"),
    ("update_absence_reason", "Pode atualizar um motivo de ausência"),
    ("delete_absence_reason", "Pode deletar um motivo de ausência"),

    ## Salary History
    ("view_all_salary_history", "Pode visualizar todos os históricos de salário"),
    ("view_salary_history", "Pode visualizar um histórico de salário"),
    ("create_salary_history", "Pode criar um histórico de salário"),
    ("update_salary_history", "Pode atualizar um histórico de salário"),
    ("delete_salary_history", "Pode deletar um histórico de salário"),

    ## Deductions
    ("view_all_deductions", "Pode visualizar todas as deduções"),
    ("view_deduction", "Pode visualizar uma dedução"),
    ("create_deduction", "Pode criar uma dedução"),
    ("update_deduction", "Pode atualizar uma dedução"),
    ("delete_deduction", "Pode deletar uma dedução"),

    ## Bonuses
    ("view_all_bonuses", "Pode visualizar todos os bônus"),
    ("view_bonus", "Pode visualizar um bônus"),
    ("create_bonus", "Pode criar um bônus"),
    ("update_bonus", "Pode atualizar um bônus"),
    ("delete_bonus", "Pode deletar um bônus"),
    
    ## Cargos (Roles)
    ("view_all_roles", "Pode visualizar todos os cargos"),
    ("view_role", "Pode visualizar um cargo"),
    ("create_role", "Pode criar um cargo"),
    ("update_role", "Pode atualizar um cargo"),
    ("delete_role", "Pode deletar um cargo"),

    ## contract_state_contract
    ("view_all_contract_states", "Pode visualizar todos os contratos de estado contratual"),
    ("view_contract_state_contract", "Pode visualizar um contrato de estado contratual"),
    ("create_contract_state_contract", "Pode criar um contrato de estado contratual"),
    ("update_contract_state_contract", "Pode atualizar um contrato de estado contratual"),
    ("delete_contract_state_contract", "Pode deletar um contrato de estado contratual"),
    
    ## Grupos de Autenticação
    ("view_all_auth_groups", "Pode visualizar todos os grupos de autenticação"),
    ("view_auth_group", "Pode visualizar um grupo de autenticação"),
    ("create_auth_group", "Pode criar um grupo de autenticação"),
    ("update_auth_group", "Pode atualizar um grupo de autenticação"),
    ("delete_auth_group", "Pode deletar um grupo de autenticação"),
    
    ## Permissões
    ("view_all_permissions", "Pode visualizar todas as permissões"),
    ("add_group_permissions", "Pode adicionar permissões a um grupo"),
    ("delete_group_permissions", "Pode deletar permissões de um grupo"),

    ## analytics
    ("view_analytics", "Pode visualizar as análises"),
    
    ## Permissoes User Grupo
    ("view_all_permissions_user_group", "Pode visualizar todas as permissões de utilizador de grupo"),
    
]

DEFAULT_CONTENT_TYPE_ID = 5

def seed(quantity):
    with connection.cursor() as cursor:
        total_permissions = len(PERMISSIONS)

        for idx, (codename, name) in enumerate(PERMISSIONS, start=1):
            # Check if the permission already exists
            cursor.execute(
                """
                SELECT id FROM auth_permission
                WHERE content_type_id = %s AND codename = %s;
                """,
                [DEFAULT_CONTENT_TYPE_ID, codename]
            )
            permission = cursor.fetchone()

            if not permission:  # Only insert if the permission does not exist
                cursor.execute(
                    """
                    INSERT INTO auth_permission (name, content_type_id, codename)
                    VALUES (%s, %s, %s);
                    """,
                    [name, DEFAULT_CONTENT_TYPE_ID, codename]
                )

            # Print progress at 25% intervals
            if total_permissions >= 4 and (idx % (total_permissions // 4) == 0):
                print(f"Progress: {(idx / total_permissions) * 100:.0f}% completed.")

        print("Progress: 100% completed.")

def delete_all():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM auth_permission
            WHERE content_type_id = %s;
            """,
            [DEFAULT_CONTENT_TYPE_ID]
        )
        print("Todas as permissões deletadas para o content_type_id especificado.")
