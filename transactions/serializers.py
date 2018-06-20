from rest_framework import serializers


class AddTransactionDetailsSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(required=True, max_length=254)

    class Meta:
        from .models import TransactionDetails

        model = TransactionDetails
        fields = ('category', 'amount', 'mode', 'contact')


class ShowTransactionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import TransactionDetails

        model = TransactionDetails
        fields = '__all__'