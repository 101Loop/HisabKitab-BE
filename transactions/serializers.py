from rest_framework import serializers


class ShowModeSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import TransactionModes

        model = TransactionModes
        fields = ('id', 'mode')
        read_only_fields = ('id', 'mode')


class AddTransactionDetailsSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(required=True, max_length=254)

    class Meta:
        from .models import TransactionDetails

        model = TransactionDetails
        fields = ('category', 'amount', 'mode', 'contact')


class ShowTransactionDetailsSerializer(serializers.ModelSerializer):
    from contacts.serializers import ShowContactDetailSerializer

    mode = ShowModeSerializer(many=False)
    contact = ShowContactDetailSerializer(many=False)

    class Meta:
        from .models import TransactionDetails

        model = TransactionDetails
        fields = '__all__'
