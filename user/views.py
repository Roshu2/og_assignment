from django.shortcuts import render
from rest_framework.views import APIView


class UserView(APIView):
    
    def get(self, request):
        
        return render(request, 'base/base.html',)