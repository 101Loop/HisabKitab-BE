
from rest_framework  import generics
from .models import ContactDetails
from .serializers import ContactDetailSerializer
from rest_framework.response import Response


class Contact(generics.ListCreateAPIView):

    def list(self, request):
        queryset = ContactDetails.objects.all()
        serializer = ContactDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
