from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response

from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope


def addTrans(user, amount, name, trans_date, mode, category, purpose=None):
    import datetime

    import iso8601

    from drf_transaction.models import TransactionDetail, TransactionMode

    from drf_contact.models import ContactDetail

    contact_obj, create = ContactDetail.objects.get_or_create(name=name, created_by=user)

    td = TransactionDetail()
    td.created_by = user
    td.create_date = datetime.datetime.now()
    td.update_date = td.create_date
    td.amount = amount
    td.contact = contact_obj
    td.comments = purpose
    td.transaction_date = iso8601.parse_date(trans_date).date()
    td.category = category
    td.mode = TransactionMode.objects.get(pk=mode)
    td.save()
    return td


class MunsiJiCall(APIView):
    renderer_classes = (JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (TokenHasReadWriteScope, )
    authentication_classes = (OAuth2Authentication, )
    intent_names = {
        'AddDebit': 'D'
    }

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        query_result = data['queryResult']
        query_text = query_result['queryText']
        params = query_result['parameters']
        intent = query_result['intent']
        lang = query_result['languageCode']
        if intent['displayName'].startswith('Add'):
            trans = addTrans(user, params['debit']['amount'], params['person'], params['date'], int(params['mode']),
                             self.intent_names[intent['displayName']], params['purpose'])
            response = '%s, your %s transaction of %s amount toward %s done on %s via %s has been recorded.' % (
                trans.created_by.name, trans.get_category_display(), trans.amount, trans.contact.name,
                trans.transaction_date, trans.mode.mode)
            response = {
                "fulfillmentText": response,
            }
        return Response(response, status=status.HTTP_200_OK, headers={'Content-type': 'application/json'})
