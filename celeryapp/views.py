from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import run_task


class CeleryView(APIView):
    def post(self, request):
        a = request.data.get('a')
        b = request.data.get('b')
        result = run_task.apply_async(args=[a, b])

        return Response({'status': True,
                         'message': 'successfully launch task',
                         'task_id': result.id
                         },
                        status=status.HTTP_200_OK)

    def get(self, request, task_id):
        pass
