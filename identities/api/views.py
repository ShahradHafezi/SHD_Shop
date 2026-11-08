from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer, SigninSerializer, SignupSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, _ = Token.objects.get_or_create(user_id=response.data["id"])
        response.data["token"] = token.key
        return response


class SigninView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SigninSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token, _ = Token.objects.get_or_create(user=serializer.validated_data["user"])
        return Response({"token": token.key})


class SignoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile

    def perform_destroy(self, instance):
        instance.user.delete()

