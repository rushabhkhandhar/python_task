# taskmanager/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import scrape_coin_data

class StartScrapingView(APIView):
    def post(self, request, *args, **kwargs):
        coins = request.data.get('coins')
        if not coins:
            return Response({"error": "Coin list is required."}, status=status.HTTP_400_BAD_REQUEST)

        job_ids = []
        for coin in coins:
            task = scrape_coin_data.delay(coin)
            job_ids.append(task.id)
        
        return Response({'job_ids': job_ids}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id, *args, **kwargs):
        result = AsyncResult(job_id)
        if result.ready():
            return Response(result.result, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'pending'}, status=status.HTTP_200_OK)
