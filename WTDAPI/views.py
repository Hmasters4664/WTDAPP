from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from user.models import User
from .models import Event
from django.http import Http404
from Profile.models import Profile, Relationship
from WTDAPI.serializers import UserSerializer, ProfileSerializer, EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .functions import scrapeQuicket


@csrf_exempt
@api_view(['POST'])
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        content = {'200': 'Ok'}
        return Response(serialized.data,status=status.HTTP_200_OK)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class GetProvinceEvents(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        province = self.kwargs['province']
        events = Event.objects.get_queryset(province=province)
        EvSerial = EventSerializer(events,many=True)
        return Response(EvSerial.data)


class Scrape(APIView):
    #permission_classes(IsAdminUser)

    def get(self, request, format=None):
        scrapeQuicket('gauteng')
        return Response(status=status.HTTP_200_OK)