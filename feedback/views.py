from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework.generics import CreateAPIView


class AddFeedback(CreateAPIView):

    serializer_class = FeedbackSerializer
