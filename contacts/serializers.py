from rest_framework import serializers
from .models import ContactDetails


class ShowContactDetailSerializer(serializers.ModelSerializer):
    """
    ShowContactDetailSerializer is a model serializer that includes the details of a contact.
    Returns
    -------
        returns a dictionary containing::
            'id' : int
            'name' : str
            'email' : str
            'mobile' : str
    """

    class Meta:
        model = ContactDetails
        fields = ('id', 'name', 'email', 'mobile')


# class AddContactDetailSerializer(serializers.ModelSerializer):

