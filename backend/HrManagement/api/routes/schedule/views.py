from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from api.utils.mongo_client import get_mongo_db

from api.utils.dotenv import is_debug_mode
from api.utils.permissions import check_permission_decorator, check_permission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ScheduleViewSet(ViewSet):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

    """
    ViewSet para manipular a coleção 'schedule' no MongoDB.
    """

    @check_permission_decorator('view_all_schedule')
    def list(self, request):
        db = get_mongo_db()
        collection = db['schedule']

        documents = list(collection.find({}, {'_id': 0}))

        return Response(documents, status=status.HTTP_200_OK)

    """
        Retrieve, update, or delete by id_employee
        e.g GET /api/schedule/<id_employee>/
        e.g PUT /api/schedule/<id_employee>/
        e.g DELETE /api/schedule/<id_employee>/
    """
    @action(detail=False, methods=['get', 'put', 'delete'], url_path=r'(?P<id_employee>[^/]+)')
    def handle_by_id_employee(self, request, id_employee):
        db = get_mongo_db()
        collection = db['schedule']

        try:
            if request.method == 'GET':
                check_permission(request.user, 'view_schedule')

                # Buscar o documento usando id_employee
                document = collection.find_one({'id_employee': id_employee}, {'_id': 0})
                if document:
                    return Response(document, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'PUT':
                check_permission(request.user, 'update_schedule')

                # Atualizar o documento usando id_employee
                data = request.data
                result = collection.update_one({'id_employee': id_employee}, {'$set': data})
                if result.matched_count:
                    return Response({'detail': 'Document updated successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            elif request.method == 'DELETE':
                check_permission(request.user, 'delete_schedule')

                # Deletar o documento usando id_employee
                result = collection.delete_one({'id_employee': id_employee})
                if result.deleted_count:
                    return Response({'detail': 'Document deleted successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'detail': f'Method {request.method} not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @check_permission_decorator('create_schedule')
    def create(self, request):
        db = get_mongo_db()
        collection = db['schedule']

        try:
            data = request.data
            result = collection.insert_one(data)
            return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
