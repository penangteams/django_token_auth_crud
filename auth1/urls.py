from django.urls import path, include
from auth1.views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    EmployerRegistrationView,
    OwnerRegistrationView,
    JobseekerRegistrationView,
    User_allViewSet,
    owners_list,
    jobseekers_list,
    employers_list,
    changeuserpwd,
    UserDetailView,
    UserDeleteView,
    UserUpdateView,
    ChangePasswordView,
)

urlpatterns = [
    # use api
    path("register/", UserRegistrationView.as_view(), name="user_registration"),  # post
    path("login/", UserLoginView.as_view(), name="user_login"),  # post
    path("logout/", UserLogoutView.as_view(), name="user_logout"),  # post
    path(
        "register/jobseeker/",
        JobseekerRegistrationView.as_view(),
        name="jobseeker-registration",
    ),
    path(
        "register/employer/",
        EmployerRegistrationView.as_view(),
        name="employer-registration",
    ),
    path("register/owner/", OwnerRegistrationView.as_view(), name="owner-registration"),
    path("userslist/", User_allViewSet.as_view({"get": "list"}), name="users-list"),
    path("ownerslist/", owners_list, name="owners_list"),
    path("employerslist/", employers_list, name="employers_list"),
    path("jobseekerslist/", jobseekers_list, name="jobseekers_list"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/delete/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="user-update"),
    path(
        "user/change-password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path(
        "user/must-change-password/",
        changeuserpwd,
        name="must-change_password",
    ),
    # Add other URLs here
]
