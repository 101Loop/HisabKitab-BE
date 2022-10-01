from rest_framework.views import APIView


def add_trans(user, amount, name, trans_date, mode, category, purpose=None):
    import datetime

    import iso8601

    from drf_transaction.models import TransactionDetail, TransactionMode

    from drf_contact.models import ContactDetail

    contact_obj, create = ContactDetail.objects.get_or_create(
        name=name, created_by=user
    )

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
    return f"{td.created_by.name}, your {td.get_category_display()} transaction of {td.amount} amount toward {td.contact.name} done on {td.transaction_date} via {td.mode.mode} has been recorded."


def future_value(p: float, r: float, t: float, freq: str, lumpsum=False):
    frequency_factor = {"month": 12, "year": 1, "quarter": 4, "half": 2}
    r = r / (frequency_factor[freq]) / 100
    n = t * frequency_factor[freq]
    fv = ((1 + r) ** n) - 1
    fv = fv / r
    fv = fv * (1 + r)
    fv = fv * p
    return f"Your future value will be approximately {round(fv, 2)}."


class MunsiJiCall(APIView):
    # from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
    # from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope
    from rest_framework.permissions import AllowAny

    from django.views.decorators.csrf import csrf_exempt

    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser

    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)

    def parse_query_result(self, query_result):
        user = self.request.user

        params = query_result["parameters"]
        query_text = query_result["queryText"]
        intent = query_result["intent"]
        lang = query_result["languageCode"]

        response = {
            "fulfillmentText": "Some error occurred while processing your request. Kindly try again later."
        }
        try:
            intent_obj = intent_details[intent["displayName"]]
        except KeyError:
            response[
                "fulfillmentText"
            ] = "Currently server is unable to handle provided intent request."
        else:
            response["fulfillmentText"] = intent_obj["func"](user, params)
        return response

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        from rest_framework import status

        import logging

        from rest_framework.response import Response

        logger = logging.getLogger(__name__)

        logger.info("HERE ARE ALL THE DATA! ---- HIMANSHU ----")
        logger.debug({"data": request.data, "header": request.META})

        data = request.data
        query_result = data["queryResult"]
        response = self.parse_query_result(query_result)
        return Response(
            response,
            status=status.HTTP_200_OK,
            headers={"Content-type": "application/json"},
        )


intent_details = {
    "AddDebit": {
        "func": lambda user, parameters: add_trans(
            user,
            parameters["debit"]["amount"],
            parameters["person"],
            parameters["date"],
            int(parameters["mode"]),
            "D",
            parameters["purpose"],
        )
    },
    "AddCredit": {
        "func": lambda user, parameters: add_trans(
            user,
            parameters["debit"]["amount"],
            parameters["person"],
            parameters["date"],
            int(parameters["mode"]),
            "C",
            parameters["purpose"],
        )
    },
    "SIPCalculator_Return": {
        "func": lambda user, parameters: future_value(
            parameters["amount"]["amount"],
            parameters["rate"],
            parameters["years"],
            parameters["freq"],
        )
    },
}
