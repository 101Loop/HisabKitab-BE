from rest_framework import serializers


class ShowModeSerializer(serializers.ModelSerializer):
    """
    ShowModeSerializer is a model serializer that shows the modes of transaction.
    Returns
    -------
        returns a dictionary containing::
            'id' : int
            'mode' : str
    """
    class Meta:
        from .models import TransactionModes

        model = TransactionModes
        fields = ('id', 'mode')
        read_only_fields = ('id', 'mode')


class AddTransactionDetailsSerializer(serializers.ModelSerializer):
    """
    AddTransactionDetailsSerializer is a model serializer that includes the attributes required for creating a new transaction.
    Returns
    -------
        returns a dictionary containing::
            'category' : str
            'amount' : float
            'mode' : str
            'contact' : str
            'transaction_date' : date
    """
    contact = serializers.CharField(required=True, max_length=254)

    class Meta:
        from .models import TransactionDetails

        model = TransactionDetails
        fields = ('category', 'amount', 'mode', 'contact', 'transaction_date')


class ShowTransactionDetailsSerializer(serializers.ModelSerializer):
    """
    ShowTransactionDetailsSerializer  is a model serializer that shows the attributes of a transaction.
    """
    from contacts.serializers import ShowContactDetailSerializer

    mode = ShowModeSerializer(many=False)
    contact = ShowContactDetailSerializer(many=False)

    class Meta:
        from .models import TransactionDetails

        model = TransactionDetails
        fields = '__all__'
