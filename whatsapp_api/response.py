from rest_framework.response import Response


def returnSuccess():
    return Response(
            {
            'code': 200,
            'status': True,
            'message': "Sucess"
            }
        )

def returnFailure():
    return Response(
            {
            'code': 400,
            'status': False,
            'message': "Failure"
            }
        )
