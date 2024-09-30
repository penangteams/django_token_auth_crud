from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import generics
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import os
import shutil


class ProfileList(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileDeleteView(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        img = Profile.objects.get(pk=instance.id)
        mypath = img.media_file.path
        dirs = os.path.dirname(mypath)
        if img.media_file:
            if os.path.isfile(mypath) or os.path.islink(mypath):
                os.unlink(mypath)
            if os.path.isdir(dirs):
                # os.rmdir(dirs)
                shutil.rmtree(dirs)
            else:
                raise ValueError("file {} is not a file or dir.".format(mypath))
        instance.delete()
        return Response({"detail": "deleted Profile."}, status=status.HTTP_200_OK)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    partial = True

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_img = Profile.objects.get(pk=instance.id)
        mypath = old_img.media_file.path
        if request.FILES.get("media_file"):
            if old_img.media_file:
                if os.path.isfile(mypath) or os.path.islink(mypath):
                    os.unlink(mypath)
                else:
                    raise ValueError("file {} is not a file or dir.".format(mypath))
            instance.media_file = request.FILES.get("media_file")
            instance.save()
        for key, value in request.data.items():
            setattr(instance, key, value)
        instance.save()
        return Response({"detail": "updated Profile."}, status=status.HTTP_200_OK)
