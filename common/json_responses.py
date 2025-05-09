from django.http import JsonResponse

class DataJsonResponse(JsonResponse):
    """
    A standard JSON response class that wraps the data in a standard format.
    """

    def __init__(self, data=None, status=200, **kwargs):
        """
        Initialize the response with the given data and status code.
        """

        if isinstance(data, str):
            data = {"data": data}

        d = data["data"] if 'data' in data else None
        m = data["message"] if 'message' in data else None

        # delete data and message from data
        if d:
            del data["data"]
        if m:
            del data["message"]

        # Wrap the data in a standard format
        response_data = {
            "data": d if d else data, 
            "message": m if m else None,
        }
        super().__init__(response_data, status=status, **kwargs)


class ErrorJsonResponse(JsonResponse):
    """
    A standard JSON response class that wraps the error in a standard format.
    """

    def __init__(self, error=None, status=400, **kwargs):
        """
        Initialize the response with the given error and status code.
        """
        if isinstance(error, str):
            error = {"error": error}
        
        e = error["error"] if 'error' in error else None
        m = error["message"] if 'message' in error else None
        if e:
            del error["error"]
        if m:
            del error["message"]

        # Wrap the error in a standard format
        response_data = {
            "error": e if e else error,
            "message": m if m else None,
        }
        super().__init__(response_data, status=status, **kwargs)