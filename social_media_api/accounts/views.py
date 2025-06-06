from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import PersonalRegistrationSerializer, BusinessRegistrationSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.parsers import JSONParser # Optional but good practice to explicitly list parsers if not using defaults

class PersonalRegistrationView(APIView):
    """
    Register a new personal account and return a token.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=PersonalRegistrationSerializer, # <--- Tell Swagger to use this serializer for the request body
        responses={
            201: 'User created successfully',
            400: 'Bad request (validation errors)'
        }
    )
    def post(self, request):
        serializer = PersonalRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessRegistrationView(APIView):
    """
    Register a new business account and return a token.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=BusinessRegistrationSerializer, # <--- Tell Swagger to use this serializer for the request body
        responses={
            201: 'User created successfully',
            400: 'Bad request (validation errors)'
        }
    )
    def post(self, request):
        serializer = BusinessRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    Retrieve the authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)