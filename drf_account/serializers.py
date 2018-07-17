from rest_framework import serializers


class AddBankAccountSerializer(serializers.ModelSerializer):
    bank = serializers.CharField(max_length=254, required=True, allow_null=False, allow_blank=False)

    class Meta:
        from .models import BankAccount
        model = BankAccount
        fields = ('nickname', 'bank', 'description', 'accnumber')


class ShowBankSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import BankMaster
        model = BankMaster
        fields = ('name', 'bank_aliases')


class ShowBankAccountSerializer(serializers.ModelSerializer):

    bank = ShowBankSerializer(many=False)

    class Meta:
        from .models import BankAccount
        model = BankAccount
        fields = ('id', 'nickname', 'bank', 'description', 'accnumber', 'update_date', 'create_date')
