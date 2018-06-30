from rest_framework import serializers
from .models import TransactionDetails


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
            'comments' : str
    """
    contact = serializers.CharField(required=True, max_length=254)

    class Meta:
        model = TransactionDetails
        fields = ('category', 'amount', 'mode', 'contact', 'transaction_date', 'comments')


class ShowTransactionDetailsSerializer(serializers.ModelSerializer):
    """
    ShowTransactionDetailsSerializer  is a model serializer that shows the attributes of a transaction.
    """
    from contacts.serializers import ShowContactDetailSerializer

    mode = ShowModeSerializer(many=False)
    contact = ShowContactDetailSerializer(many=False)
    transaction_date = serializers.DateField()

    class Meta:
        model = TransactionDetails
        fields = '__all__'


class DeleteTransactionDetailsSerializer(serializers.ModelSerializer):
    """
    It is a model serializer to delete a particular transaction.
    """

    class Meta:
        model = TransactionDetails
        fields = ('id',)


class UpdateTransactionDetailsSerializer(serializers.ModelSerializer):
    """
    It is a model serializer to update a particular serializer.
    """
    from .models import TransactionModes

    contact = serializers.CharField(required=False, max_length=254)
    transaction_date = serializers.DateField(required=False)
    amount = serializers.FloatField(required=False)
    category = serializers.CharField(required=False)
    mode = serializers.PrimaryKeyRelatedField(required=False, queryset=TransactionModes.objects.all())

    class Meta:
        model = TransactionDetails
        fields = ('mode', 'amount', 'transaction_date', 'contact', 'category', 'comments')
        read_only_fields = ('created_by', 'create_date', 'last_modified')
