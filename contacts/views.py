from rest_framework.generics import ListAPIView, CreateAPIView
from .models import ContactDetails
from .serializers import ShowContactDetailSerializer


class ShowContacts(ListAPIView):
    """
    This view is to show the details of a contact.
    """

    queryset = ContactDetails.objects.all()
    serializer_class = ShowContactDetailSerializer


# class AddContacts(CreateAPIView):

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

