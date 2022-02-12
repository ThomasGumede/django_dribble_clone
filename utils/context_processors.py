from django.http import request
from shots.models import ShotCategory

def categories(request):
    categories = ShotCategory.objects.all()
    return {"categories" : categories}