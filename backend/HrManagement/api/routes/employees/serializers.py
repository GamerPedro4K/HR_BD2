from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection, transaction
from django.db.utils import IntegrityError
from api.global_serializers.AddressSerializer import AddressSerializerUpdate
from api.global_serializers.AuthUserSerializer import AuthUserSerializerUpdate
from api.global_serializers.ContractSerializer import ContractSerializerUpdate
from api.global_serializers.CertificatesSerializer import CertificatesSerializerUpdate
from api.global_serializers.SalaryHistorySerializer import SalaryHistorySerializerUpdate
from api.global_serializers.TrainingsSerializer import TrainingsSerializerUpdate
from api.global_serializers.VacationsSerializer import VacationsSerializerUpdate
from datetime import date

# Custom user-like object to pass to JWT
class UserObject:
    def __init__(self, user_id, username, first_name, last_name, email):
        self.id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        
class UpdateSerializer(serializers.Serializer):
    employee = AuthUserSerializerUpdate(required=True)
    employee_address = AddressSerializerUpdate(required=True)

    contract = ContractSerializerUpdate(required=False)
    salary = SalaryHistorySerializerUpdate(required=False)
    vacations = VacationsSerializerUpdate(required=False)
    trainings = serializers.ListField(child=TrainingsSerializerUpdate(required=False), required=False)
    salary = SalaryHistorySerializerUpdate(required=False)
    certificates = serializers.ListField(child=CertificatesSerializerUpdate(required=False), required=False)
    

    def validate(self, data):
        instance = self.instance 
        employee = data['employee']
        username = employee.get('username')
        email = employee['email']
        
        
        with connection.cursor() as cursor:
            # 1) Verifica se já existe outro user com o mesmo username.
            if username:
                cursor.execute("""
                    SELECT id 
                    FROM auth_user 
                    WHERE username = %s 
                    AND id <> (
                        SELECT id_auth_user FROM employees WHERE id_employee = %s
                    )
                """, [username, instance.id_employee])
                if cursor.fetchone():
                    raise serializers.ValidationError("Já existe um user com este username.")

            # 2) Verifica se já existe outro user com o mesmo email.
            if email:
                cursor.execute("""
                    SELECT id 
                    FROM auth_user 
                    WHERE email = %s
                    AND id <> (
                        SELECT id_auth_user FROM employees WHERE id_employee = %s
                    )
                """, [email, instance.id_employee])
                if cursor.fetchone():
                    raise serializers.ValidationError("Já existe um user com este e-mail.")
            
            if employee.get('id_group'):
                cursor.execute("SELECT 1 FROM auth_group WHERE id = %s", [employee['id_group']])
                if not cursor.fetchone():
                    raise serializers.ValidationError("O grupo especificado não existe.")

        return data

    def update(self, instance, validated_data):
        def not_empty(val):
            return val not in (None, "")
        
        print("hiiiiiiiiiiiiiiiiii")
        print(self.context['auth'])
        
        validated_data['auth'] = self.context['auth']
        

        employee = validated_data.get('employee', {})
        employee_address = validated_data.get('employee_address', {})

        vacations = validated_data.get('vacations', {})
        trainings = validated_data.get('trainings', {})
        contract = validated_data.get('contract', {})
        salary = validated_data.get('salary', {})
        certificates = validated_data.get('certificates', {})

        print("AAAAAAAAAAAAAAA")
        print(f"Valor: {validated_data['auth']['sub']}")
        print("AAAAAAAAAAAAAAA")
        if vacations:
            vacations['aproved_date'] = date.today()
            vacations['aproved_by_employee_id'] =  validated_data['auth']['sub']
        
        if salary:
            salary['id_employee_aproved_by'] =  validated_data['auth']['sub']
        
        user_id = instance.id_auth_user
        print(f"User ID: {user_id}")
        employee_id = instance.id_employee
        print(f"Employee ID: {employee_id}")

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # update table auth_user
                    if not_empty(employee.get('password', '')):
                        cursor.execute("""
                            UPDATE auth_user
                            SET username = %s, password = %s, first_name = %s, last_name = %s, email = %s
                            WHERE id = %s
                        """, [employee['username'], make_password(employee['password']), employee['first_name'], employee['last_name'], employee['email'], user_id])
                    else:
                        cursor.execute("""
                            UPDATE auth_user
                            SET username = %s, first_name = %s, last_name = %s, email = %s
                            WHERE id = %s
                        """, [employee['username'], employee['first_name'], employee['last_name'], employee['email'], user_id])
                    
                    # update table employees
                    cursor.execute("""
                        UPDATE employees
                        SET phone = %s, src = %s, birth_date = %s, updated_at = NOW()
                        WHERE id_employee = %s
                    """, [employee['phone'], employee['img_src'], employee['birth_date'], employee_id])

                    # update table employee_location
                    cursor.execute("""
                        UPDATE employee_location
                        SET address = %s, city = %s, district = %s, country = %s, zip_code = %s
                        WHERE id_employee = %s
                    """, [employee_address['street'], employee_address['city'], employee_address['district'], employee_address['country'], employee_address['zip_code'], employee_id])

                    # update table auth_user_groups
                    cursor.execute("""
                        UPDATE auth_user_groups
                        SET group_id = %s
                        WHERE user_id = %s
                    """, [employee['id_group'], user_id])

                    # update table vacations
                    if vacations:
                        cursor.execute("""
                            DELETE FROM vacations
                            WHERE id_employee = %s
                            AND start_date >= NOW()
                        """, [employee_id])
                        cursor.execute("""
                            INSERT INTO vacations (id_employee, start_date, end_date)
                            VALUES (%s, %s, %s)
                        """, [employee_id, vacations['start_date'], vacations['end_date']])
                    else:
                        cursor.execute("""
                            DELETE FROM vacations
                            WHERE id_employee = %s
                            AND start_date >= NOW()
                        """, [employee_id])
                    
                    # update table trainings
                    if trainings:
                        cursor.execute("""
                            DELETE FROM trainings
                            WHERE id_employee = %s
                        """, [employee_id])
                        for training in trainings:
                            cursor.execute("""
                                INSERT INTO trainings (id_employee, id_training_type, start_date, end_date)
                                VALUES (%s, %s, %s, %s)
                            """, [employee_id, training['id_training_type'], training['start_date'], training['end_date']])
                    else:
                        cursor.execute("""
                            DELETE FROM trainings
                            WHERE id_employee = %s
                        """, [employee_id])
                    # add row in contract
                    if contract:
                        cursor.execute("""
                            INSERT INTO contract (id_employee, id_role, id_contract_type)
                            VALUES (%s, %s, %s) RETURNING id_contract
                        """, [employee_id, contract['id_role'], contract['id_contract_type']])
                        contract_id_row = cursor.fetchone()
                        if not contract_id_row:
                            raise serializers.ValidationError("Erro ao criar o contrato.")
                        id_contract = contract_id_row[0]

                        cursor.execute("""
                            INSERT INTO contract_state_contract (id_contract, id_contract_state)
                            VALUES (%s, %s)
                        """, [id_contract, contract['id_contract_state']])
                        print(f"Contract ID: {id_contract}")

                    # add row in salary_history
                    if salary:
                        cursor.execute("""
                            INSERT INTO salary_history (id_contract, id_employee_aproved_by, base_salary, extra_hour_rate, start_date)
                            VALUES (%s, %s, %s, %s, %s)
                        """, [id_contract, salary['id_employee_aproved_by'], salary['base_salary'], salary['extra_hour_rate'], salary['start_date']])

                    # add row in certificates
                    if certificates:
                        cursor.execute("""
                            DELETE FROM certifications
                            WHERE id_employee = %s
                        """, [employee_id])
                        for certificate in certificates:
                            if certificate.get('expiration_date', None) is None:
                                cursor.execute("""
                                    INSERT INTO certifications (id_employee, id_certificate_type, issuing_organization, issue_date)
                                    VALUES (%s, %s, %s, %s)
                                """, [employee_id, certificate['id_certificate_type'], certificate['issuing_organization'], certificate['issue_date']])
                            else:
                                cursor.execute("""
                                    INSERT INTO certifications (id_employee, id_certificate_type, issuing_organization, issue_date, expiration_date)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, [employee_id, certificate['id_certificate_type'], certificate['issuing_organization'], certificate['issue_date'], certificate['expiration_date']])
                    else:
                        cursor.execute("""
                            DELETE FROM certifications
                            WHERE id_employee = %s
                        """, [employee_id])

        except IntegrityError as e:
            print(e)
            raise serializers.ValidationError("Ocorreu um erro ao criar o utilizador.")
        
        return {
            "id": user_id,
            "username": employee['username'],
            "first_name": employee['first_name'],
            "last_name": employee['last_name'],
            "email": employee['email'],
        }