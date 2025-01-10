from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection, transaction
from django.db.utils import IntegrityError
from api.global_serializers.AddressSerializer import AddressSerializer
from api.global_serializers.AuthUserSerializer import AuthUserSerializer
from api.global_serializers.ContractSerializer import ContractSerializer
from api.global_serializers.EmployeeHierarchySerializer import EmployeeHierarchySerializer
from api.global_serializers.SalaryHistorySerializer import SalaryHistorySerializer
from api.global_serializers.TrainingsSerializer import TrainingsSerializer
from api.global_serializers.VacationsSerializer import VacationsSerializer
from api.global_serializers.CertificatesSerializer import CertificatesSerializer
from datetime import date
from uuid import UUID

# Custom user-like object to pass to JWT
class UserObject:
    def __init__(self, user_id, username, first_name, last_name, email):
        self.id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        

class RegisterSerializer(serializers.Serializer):
    # Required fields
    employee = AuthUserSerializer(required=True)
    employee_address = AddressSerializer(required=True)

    # Optional fields
    #employee_hierarchy = EmployeeHierarchySerializer(required=False)
    contract = ContractSerializer(required=False)
    salary = SalaryHistorySerializer(required=False)
    vacations = VacationsSerializer(required=False)
    trainings = serializers.ListField(child=TrainingsSerializer(required=False), required=False)
    salary = SalaryHistorySerializer(required=False)
    certificates = serializers.ListField(child=CertificatesSerializer(required=False), required=False)

    def validate(self, data):
        employee = data['employee']
        username = employee['username']
        email = employee['email']
        id_group = employee['id_group']
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM auth_user WHERE username = %s", [username])
            if cursor.fetchone():
                raise serializers.ValidationError("A user with this username already exists.")
            cursor.execute("SELECT 1 FROM auth_user WHERE email = %s", [email])
            if cursor.fetchone():
                raise serializers.ValidationError("Já existe um utilizador com este e-mail.")
            cursor.execute("SELECT 1 FROM auth_group WHERE id = %s", [id_group])
            if not cursor.fetchone():
                raise serializers.ValidationError("O grupo especificado não existe.")
        return data

    def create(self, validated_data):
        validated_data['auth'] = self.context['auth']

        # Required fields
        employee = validated_data.get('employee')
        employee_address = validated_data.get('employee_address')

        # Optional fields
        #employee_hierarchy = validated_data.get('employee_hierarchy', None)
        vacations = validated_data.get('vacations', None)
        trainings = validated_data.get('trainings', None)
        contract = validated_data.get('contract', None)
        salary = validated_data.get('salary', None)
        certificates = validated_data.get('certificates', None)

        print("AAAAAAAAAAAAAAA")
        print(f"Valor: {validated_data['auth']['sub']}")
        print("AAAAAAAAAAAAAAA")
        if vacations:
            vacations['aproved_date'] = date.today()
            vacations['aproved_by_employee_id'] =  validated_data['auth']['sub']
        
        if salary:
            salary['id_employee_aproved_by'] =  validated_data['auth']['sub']


        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # add to table auth_user
                    cursor.execute("""
                        INSERT INTO auth_user (username, password, first_name, last_name, email, is_active, is_superuser, is_staff, date_joined) 
                        VALUES (%s, %s, %s, %s, %s, TRUE, FALSE, FALSE, NOW()) RETURNING id
                    """, [employee['username'], make_password(employee['password']), employee['first_name'], employee['last_name'], employee['email']])
                    user_id = cursor.fetchone()[0]
                    print(f"User ID: {user_id}")
                    
                    # add row in employees
                    cursor.execute("""
                        INSERT INTO employees (id_auth_user, phone, src, birth_date)
                        VALUES (%s, %s, %s, %s) RETURNING id_employee
                    """, [user_id, employee['phone'], employee['img_src'], employee['birth_date']])
                    employee_id = cursor.fetchone()[0]
                    print(f"Employee ID: {employee_id}")

                    # add row in address
                    cursor.execute("""
                        INSERT INTO employee_location (id_employee, address, city, district, country, zip_code)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, [employee_id, employee_address['street'], employee_address['city'], employee_address['district'], employee_address['country'], employee_address['zip_code']])

                    # add row in auth_user_groups
                    cursor.execute("""
                        INSERT INTO auth_user_groups (user_id, group_id)
                        VALUES (%s, %s)
                    """, [user_id, employee['id_group']])

                    # add row in vacations
                    if vacations:
                        cursor.execute("""
                            INSERT INTO vacations (id_employee, start_date, end_date)
                            VALUES (%s, %s, %s)
                        """, [employee_id, vacations['start_date'], vacations['end_date']])

                    # add row in trainings
                    if trainings:
                        for training in trainings:
                            cursor.execute("""
                                INSERT INTO trainings (id_employee, id_training_type, start_date, end_date)
                                VALUES (%s, %s, %s, %s)
                            """, [employee_id, training['id_training_type'], training['start_date'], training['end_date']])

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
                        print(f"Contract ID: {id_contract}")

                    # add row in salary_history
                    if salary:
                        cursor.execute("""
                            INSERT INTO salary_history (id_contract, id_employee_aproved_by, base_salary, extra_hour_rate, start_date)
                            VALUES (%s, %s, %s, %s, %s)
                        """, [id_contract, salary['id_employee_aproved_by'], salary['base_salary'], salary['extra_hour_rate'], salary['start_date']])

                    # add row in certificates
                    if certificates:
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

        except IntegrityError as e:
            print(e)
            raise serializers.ValidationError("Ocorreu um erro ao criar o utilizador.")
        
        return UserObject(user_id=user_id, username=employee['username'], first_name=employee['first_name'], last_name=employee['last_name'], email=employee['email'])


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, password FROM auth_user WHERE email = %s", [email])
            result = cursor.fetchone()

            if result is None:
                raise serializers.ValidationError("User with this email does not exist.")
            
            user_id, hashed_password = result
            if not check_password(password, hashed_password):
                raise serializers.ValidationError("Incorrect password.")
        
        return {'id': user_id, 'email': email}