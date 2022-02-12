from django.urls import path
from actions.views import LikeShot, FollowUser, DeleteFeedbackView

app_name="actions"
urlpatterns = [
    path('like/', LikeShot.as_view(), name='like_shot'),
    path('follow/', FollowUser.as_view(), name='follow_user'),
    path('delete/shot', DeleteFeedbackView.as_view(), name='delete_feedback')
]
