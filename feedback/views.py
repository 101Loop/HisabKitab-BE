from .serializers import FeedbackSerializer
from rest_framework.generics import CreateAPIView


class AddFeedback(CreateAPIView):
    """
    This view is to add user feedback.
    """

    serializer_class = FeedbackSerializer
