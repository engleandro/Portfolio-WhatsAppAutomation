from traceback import format_exc
from rest_framework.response import Response

class MyResponses():
    
    @classmethod
    def returnSuccess(cls):
        return Response(
                {
                'code': 200,
                'status': True,
                'message': "Sucess.",
                'log': None
                }
            )
    @classmethod
    def returnFailure(cls):
        return Response(
                {
                'code': 400,
                'status': False,
                'message': "Failure.",
                'log': format_exc()
                }
            )
    @classmethod
    def returnServerError(cls):
        return Response(
                {
                'code': 500,
                'status': False,
                'message': "Server Error.",
                'log': format_exc()
                }
            ) 