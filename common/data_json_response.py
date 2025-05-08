from django.http import JsonResponse

class DataJsonResponse(JsonResponse):
    """
    A standard JSON response class that wraps the data in a standard format.
    """

    def __init__(self, data=None, status=200, **kwargs):
        """
        Initialize the response with the given data and status code.
        """
        # Wrap the data in a standard format
        response_data = {
            "data": data,
        }
        super().__init__(response_data, status=status, **kwargs)