from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.db import connection
from .serializers import RegisterSerializer, LoginSerializer, UserObject
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.dotenv import is_debug_mode 
from api.utils.permissions import check_permission_decorator

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees WHERE id_auth_user = %s", [user.id])
            data = cursor.fetchone()

            print(f"\033[31mUser: {user.id}\033[m")
            print(f"\033[33mData: {data}\033[m")
            if data:
                token['sub'] = str(data[1])
                token['first_name'] = str(user.first_name)
                token['last_name'] = str(user.last_name)
                token['email'] = str(user.email)
            
                print(f"\033[31mToken: {token['sub']}\033[m")
                print(f"\033[32mToken: {token}\033[m")

        return token
    
class RegisterView(APIView):
    if not is_debug_mode():
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        
    @check_permission_decorator('create_employee')
    def post(self, request):
        """ request.data['user']['id'] = request.user.id """
        """ print(f"\033[31mRequest.auth dir: {dir(request.auth)}\033[m")
        print(f"\033[33mRequest.auth vars: {vars(request.auth)}\033[m")
        print(f"\033[31mRequest sub: {request.auth['sub']}\033[m") """
        serializer = RegisterSerializer(data=request.data, context={'auth': request.auth})
        if serializer.is_valid():
            user = serializer.save()
            refresh = CustomTokenObtainPairSerializer.get_token(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user = UserObject(user_id=user_data['id'], username=None, first_name=None, last_name=None, email=user_data['email'])
            refresh = CustomTokenObtainPairSerializer.get_token(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)