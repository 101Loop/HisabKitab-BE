from rest_framework import serializers
from .models import ContactDetails

class ContactDetailSerializer(serializers.ModelSerializer):

    class meta:
        model = ContactDetails
        fields = '__all__'