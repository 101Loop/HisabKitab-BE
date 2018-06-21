from rest_framework.generics import ListAPIView, CreateAPIView
from .models import ContactDetails
from .serializers import ShowContactDetailSerializer


class ShowContacts(ListAPIView):

    queryset = ContactDetails.objects.all()
    serializer_class = ShowContactDetailSerializer

    # def post(self, request):
    #     serializer = ContactDetailSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
#
#
# class AddContacts(CreateAPIView):
#
#     serializer_class = ContactDetailSerializer

