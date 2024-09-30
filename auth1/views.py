from auth1.models import User, Owner, Employer, Jobseeker
from auth1.serializers import (
    UserSerializer,
    JobseekerSerializer,
    EmployerSerializer,
    OwnerSerializer,
    ChangePasswordSerializer,
)
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

# https://dev.to/forhadakhan/multi-role-user-authentication-in-django-rest-framework-3nip


class JobseekerRegistrationView(APIView):
    def post(self, request):
        serializer = JobseekerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnerRegistrationView(APIView):
    def post(self, request):
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerRegistrationView(APIView):
    def post(self, request):
        serializer = EmployerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)
            response_data = {
                "token": token.key,
                "username": user.username,
                "role": user.role,
                "status": "ok",
            }
            if user.role == "jobseeker":
                jobseeker = (
                    user.jobseeker_account
                )  # Assuming the related name is "jobseeker_account"
                if jobseeker is not None:
                    # Add jobseeker data to the response data
                    jobseeker_data = JobseekerSerializer(jobseeker).data
                    response_data["data"] = jobseeker_data

            if user.role == "employer":
                employer = (
                    user.employer_account
                )  # Assuming the related name is "employer_account"
                if employer is not None:
                    # Add employee data to the response data
                    empl_data = EmployerSerializer(employer).data
                    response_data["data"] = empl_data

            if user.role == "owner":
                owner = (
                    user.owner_account
                )  # Assuming the related name is "owner_account"
                if owner is not None:
                    # Add owner data to the response data
                    owner_data = OwnerSerializer(owner).data
                    response_data["data"] = owner_data

            return Response(response_data)
        else:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


# get all users, all roles
class User_allViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# get all owners
@api_view(("GET",))  # need this as this a fn call
@permission_classes([IsAuthenticated])
def owners_list(request):
    owners = Owner.objects.values()
    return JsonResponse(status=200, data={"owners_list": list(owners)})


# get all employers
@api_view(("GET",))  # need this as this a fn call
@permission_classes([IsAuthenticated])
def employers_list(request):
    employers = Employer.objects.values()
    return JsonResponse(status=200, data={"employers_list": list(employers)})


# get all jobseekers
@api_view(("GET",))  # need this as this a fn call
@permission_classes([IsAuthenticated])
def jobseekers_list(request):
    js = Jobseeker.objects.values()
    return JsonResponse(status=200, data={"jobseekers_list": list(js)})


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "deleted User."}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            # old_password = serializer.data.get("old_password")
            # if not self.object.check_password(old_password):
            #     return Response(
            #         {"old_password": ["Wrong password."]},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("password"))
            self.object.save()
            return Response(
                {"detail": "Password changed"}, status=status.HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    partial = True


# used by admin only to set other user passwords, no auth
@api_view(("PUT",))  # need this as this a fn call
@csrf_exempt
# @permission_classes([IsAuthenticated])
def changeuserpwd(request):
    username = request.data.get("username")
    password = request.data.get("password")
    u = User.objects.get(username__exact=username)
    u.set_password(password)
    u.save()
    return JsonResponse(
        status=200,
        data={
            "details": [
                {
                    "user_details": model_to_dict(
                        u, fields=["id", "username", "email", "role", "isActive"]
                    )
                },
                {"details": "Password changed!"},
            ]
        },
    )
