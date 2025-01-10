from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from api.utils.mongo_client import get_mongo_db
from datetime import datetime

from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator, check_permission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ExtraHoursViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    """
    ViewSet para manipular a coleção 'extrahours' no MongoDB.
    """
    @check_permission_decorator('view_all_extra_hours')
    def list(self, request):
        db = get_mongo_db()
        collection = db['extrahours']

        documents = list(collection.find({}, {'_id': 0}))

        return Response(documents, status=status.HTTP_200_OK)

    @check_permission_decorator('view_extra_hours')
    def retrieve(self, request, pk=None):
        db = get_mongo_db()
        collection = db['extrahours']

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

    @check_permission_decorator('create_extra_hours')
    def create(self, request):
        db = get_mongo_db()
        collection = db['extrahours']

        try:
            data = request.data
            result = collection.insert_one(data)
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    """
        Retrieve, update, or delete by id_employee and date
        e.g GET /api/extra_hours/01d0e2d3-7972-4ba1-9ccc-35e9b4415ae1/2024-12-26/
        e.g PUT /api/extra_hours/01d0e2d3-7972-4ba1-9ccc-35e9b4415ae1/2024-12-26/
        e.g DELETE /api/extra_hours/01d0e2d3-7972-4ba1-9ccc-35e9b4415ae1/2024-12-26/
    """
    @action(detail=False, methods=['get', 'put', 'delete'], url_path=r'(?P<id_employee>[^/]+)/(?P<date>\d{4}-\d{2}-\d{2})')
    def handle_by_id_date(self, request, id_employee, date):
        db = get_mongo_db()
        collection = db['extrahours']

        try:
            # Validar a data
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return Response({'detail': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

            if request.method == 'GET':
                check_permission(request.user, 'view_extra_hours')

                # Buscar o documento usando id_employee e a data
                document = collection.find_one({'id_employee': id_employee, 'date': date.isoformat()}, {'_id': 0})
                if document:
                    return Response(document, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'PUT':
                check_permission(request.user, 'update_extra_hours')

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

            elif request.method == 'DELETE':
                check_permission(request.user, 'delete_extra_hours')

                # Deletar o documento usando id_employee e a data
                result = collection.delete_one({'id_employee': id_employee, 'date': date.isoformat()})
                if result.deleted_count:
                    return Response({'detail': 'Document deleted successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'detail': f'Method {request.method} not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
