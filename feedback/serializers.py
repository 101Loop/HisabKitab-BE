from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """
    A FeedbackSerializer is a model serializer that shows the user feedback.
    Returns
    -------
        returns a dictionary containing::
            'message' : str
            'name' : str
            'mobile' : str
            'email' : str
            'create_date' : date
    """

    class Meta:

        model = Feedback
        fields = '__all__'