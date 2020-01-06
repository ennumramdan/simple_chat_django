import logging

from django.shortcuts import render
from rest_framework.views import APIView
from django.forms.models import model_to_dict

from .models import Broadcast
from .utils import (success_response,
                    created_response,
                    general_error_response,
                    server_error_response,
                    not_found_response)

logger = logging.getLogger(__name__)


# Create your views here.
class SendBroadcastView(APIView):

    def post(self, request):
        data = request.data

        if not 'text' in data:
            return general_error_response('field text is required')

        try:
            params = {
                'message': data['text']
            }

            broadcast = Broadcast.objects.create(**params)
            response_data = {
                'id': broadcast.id,
                'message': broadcast.message
            }
            return created_response(response_data)
        except Exception as e:
            logger.error({
                'action_view': 'SendBroadcastView',
                'data': request.data,
                'errors': str(e)
            })
            return server_error_response()


class ListBroadcastView(APIView):

    def get(self, request):
        broadcasts = Broadcast.objects.values('id', 'message')

        if not broadcasts:
            return not_found_response('broadcast is empty')

        return success_response(broadcasts)


class RoomView(APIView):

    def get(self, request):
        # define chat only for one room
        return render(request, 'room.html', {
            'room_name': 'simple_room'
        })