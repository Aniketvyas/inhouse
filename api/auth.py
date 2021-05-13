from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from academics.models import *
from .serializers import *

class CustomAuthToken(ObtainAuthToken):
    def post(self,request,**kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        info= stud_details.objects.get(UniversityEmailID=Token.objects.get(key=token.key).user.email)
        sinfo=stud_detailsSerializer(info)
        return Response({
            'token': token.key,
            'user_id':user.pk,
            'email':user.email,
            'name':(user.first_name+' '+ user.last_name),
            'info':sinfo.data,
        })