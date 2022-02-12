from django.urls import path
from shots.views import ShotListView, CreateShotView, ShotDetailsView, DeleteShotView


app_name = "shots"
urlpatterns = [
    path('', ShotListView.as_view(), name='shot_list'),
    path('uploads/new', CreateShotView.as_view(), name="create_shot"),
    path('<slug:category>/', ShotListView.as_view(), name='shot_list_category'),
    path('details/<uuid:shot_uuid>', ShotDetailsView.as_view(), name="shot_details"),
    path('delete/<uuid:shot_uuid>', DeleteShotView.as_view(), name='delete_shot')
]
