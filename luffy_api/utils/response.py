from rest_framework.response import Response


class CommonResponse(Response):

    def __init__(self, code=None, status=None, exception=False, content_type=None):
        super().__init__()
        pass