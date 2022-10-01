import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from munsiji.utils import add_trans, future_value

logger = logging.getLogger(__name__)


class MunsiJiCall(APIView):
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)

    def parse_query_result(self, query_result):
        user = self.request.user

        params = query_result["parameters"]
        intent = query_result["intent"]

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
