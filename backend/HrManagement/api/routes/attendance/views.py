from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId  
from api.utils.mongo_client import get_mongo_db
from datetime import datetime

from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator, check_permission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class AttendanceViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        
    """
    ViewSet para manipular a coleção 'attendance' no MongoDB.
    """
    @check_permission_decorator('view_all_attendance')
    def list(self, request):
        db = get_mongo_db()
        collection = db['attendance']

        documents = list(collection.find({}, {'_id': 0})) 

        return Response(documents, status=status.HTTP_200_OK)

    """
        Retrieve by date e.g attendance/2024-12-26/ or by id_employee e.g attendance/687544c7-07a8-404b-b011-a4653d3329c7
        and both e.g attendance/2024-12-26/?id_employee=687544c7-07a8-404b-b011-a4653d3329c7
    """
    @check_permission_decorator('view_attendance')
    def retrieve(self, request, pk=None):
        db = get_mongo_db()
        collection = db['attendance']

        try:
            date = datetime.strptime(pk, "%Y-%m-%d").date() # if not valid, raise ValueError
            documents = list(collection.find({'date': pk}, {'_id': 0}))
            if documents:
                return Response(documents, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'No records found for the given date'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            #id_employee PostgreSQL
            documents = list(collection.find({'id_employee': pk}, {'_id': 0}))
            if documents:
                return Response(documents, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Document not found for the given ID'}, status=status.HTTP_404_NOT_FOUND)

    @check_permission_decorator('create_attendance')
    def create(self, request):
        db = get_mongo_db()
        collection = db['attendance']

        try:
            data = request.data
            result = collection.insert_one(data)
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    """
        Update e.g attendance/687544c7-07a8-404b-b011-a4653d3329c7
    """
    @check_permission_decorator('update_attendance')
    def update(self, request, pk=None):
        db = get_mongo_db()
        collection = db['attendance']

        try:
            data = request.data
            # Atualizar o documento usando o id_employee (UUID)
            result = collection.update_one({'id_employee': pk}, {'$set': data})
            if result.matched_count:
                return Response({'detail': 'Document updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    """
        Retrieve, update, or delete by id_employee and date
        e.g GET attendance/687544c7-07a8-404b-b011-a4653d3329c7/2024-12-26
        e.g DELETE attendance/687544c7-07a8-404b-b011-a4653d3329c7/2024-12-26
        e.g PUT attendance/687544c7-07a8-404b-b011-a4653d3329c7/2024-12-26
    """
    @action(detail=False, methods=['get', 'delete', 'put'], url_path=r'(?P<id_employee>[^/]+)/(?P<date>\d{4}-\d{2}-\d{2})')
    def handle_by_id_date(self, request, id_employee, date):
        db = get_mongo_db()
        collection = db['attendance']

        try:
            # Validar a data
            date = datetime.strptime(date, "%Y-%m-%d").date()

            if request.method == 'GET':
                check_permission(request.user, 'view_attendance')

                # Buscar o documento usando id_employee e a data
                document = collection.find_one({'id_employee': id_employee, 'date': date.isoformat()}, {'_id': 0})
                if document:
                    return Response(document, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'DELETE':
                check_permission(request.user, 'delete_attendance')

                # Deletar o documento usando id_employee e a data
                result = collection.delete_one({'id_employee': id_employee, 'date': date.isoformat()})
                if result.deleted_count:
                    return Response({'detail': 'Document deleted successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'PUT':
                check_permission(request.user, 'update_attendance')

                # Atualizar o documento usando id_employee e a data
                data = request.data
                result = collection.update_one(
                    {'id_employee': id_employee, 'date': date.isoformat()},
                    {'$set': data}
                )
                if result.matched_count:
                    return Response({'detail': 'Document updated successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'detail': f'Method {request.method} not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except ValueError:
            return Response({'detail': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)