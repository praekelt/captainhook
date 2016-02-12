import json

from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer

from captainhook.models import Hook


class HookView(GenericAPIView):
    renderer_classes = [JSONRenderer]

    @csrf_exempt
    def post(self, request, name):
        payload = json.loads(request.DATA.get('payload', "{}"))

        '''
        # GitHub: repository['owner'] = {'name': name, 'email': email}
        # BitBucket: repository['owner'] = name
        user = info.get('owner', {})
        if isinstance(user, dict):
            user = user.get('name', None)
        '''

        Hook.objects.get(name=name).execute(payload)

        return Response({})
