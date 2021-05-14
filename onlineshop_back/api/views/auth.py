import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics, status, viewsets, mixins
from rest_framework.decorators import action, api_view
from django.contrib.auth.models import User
from api.models import Profile
from api.serializers import UserSerializer, UserProfileSerializer, RefreshTokenSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models.signals import post_save

logger = logging.getLogger('api')

class SignUpViewSet(viewsets.ViewSet):

   def create(self, request):
        if request.method == 'POST':
            user_data = request.data
            new_user = User.objects.create(email=user_data['email'], username=user_data['username'], first_name=user_data['first_name'],
                                            last_name = user_data['last_name'])            
            new_user.set_password(user_data['password'])
            new_user.save()
            serializer = UserSerializer(new_user)
            logger.info(f'User with ID {serializer.instance} was created')
            logger.debug(f'User with ID {serializer.instance} was created')
            return Response(serializer.data)

class LogoutViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f'User {serializer.instance} was logged out')
        logger.debug(f'User {serializer.instance} was logged out')
        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserInfo(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return self.request.user

class UserProfileViewSet(viewsets.GenericViewSet):  #6 viewset
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user_profile = self.get_queryset().get(user=request.user)
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)
    