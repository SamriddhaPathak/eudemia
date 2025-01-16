from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.utils import get_leaderboard

# Create your views here.

class LeaderboardView(APIView):
    """
    API endpoint that returns the leaderboard as the GET response.
    """
    def get(self, request, *args, **kwargs):
        leaderboard = get_leaderboard()
        return Response(leaderboard, status=status.HTTP_200_OK)
