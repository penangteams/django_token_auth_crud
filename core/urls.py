from django.contrib import admin
from django.urls import include, path
from appprofile import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("auth1.urls")),
    path("profile/", views.ProfileList.as_view()),
    path(
        "profile/delete/<int:pk>/",
        views.ProfileDeleteView.as_view(),
        name="profile-delete",
    ),
    path("profile/<int:pk>/", views.ProfileDetailView.as_view(), name="profile_detail"),
    path(
        "profile/update/<int:pk>/",
        views.ProfileUpdateView.as_view(),
        name="profile-update",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
