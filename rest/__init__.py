import rest_framework

from rest.settings import MySettings
from rest.forms import MyForms
from rest.models import MyModels
from rest.requests import MyRequests
from rest.responses import MyResponses
from rest.serializers import MySerializers

class Rest:
    
    Settings = MySettings
    Forms = MyForms
    Models = MyModels
    Requests = MyRequests
    Responses = MyResponses
    Serializers = MySerializers

