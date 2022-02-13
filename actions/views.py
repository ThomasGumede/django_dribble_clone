from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from actions.models import Feedback
from actions.forms import FeedbackForm
from shots.models import Shot
from accounts.models import Contact

class CreateFeedbackView(LoginRequiredMixin, FormView):
    form_class = FeedbackForm
    def form_invalid(self, form):
        return JsonResponse({"error": form.errors}, status=400)
        

    def form_valid(self, form):
        try:
            post = get_object_or_404(Shot, shot_uuid=self.kwargs['shot_uuid'])
            form.instance.user = self.request.user
            form.instance.shot = post
            feedback_instance = form.save()
                
            feedback = serializers.serialize("json", [feedback_instance, ])
            return JsonResponse({'new_feedback': feedback}, status=200)
        except Shot.DoesNotExist:
            pass

class LikeShot(View):
    def post(self, request, *args, **kwargs):
        if request.headers['X-Requested-With'] ==  'XMLHttpRequest':
            shot_uuid = request.POST.get("shot_uuid", None)
            shot_id = request.POST.get("id", None)
            action = request.POST.get("action", None)
            if shot_uuid and action and shot_id:
                post = get_object_or_404(Shot, shot_uuid=shot_uuid, pk=shot_id)
                if action == "like" and request.user not in post.user_like.all():
                    post.user_like.add(request.user)   
                else:
                    post.user_like.remove(request.user)
                return JsonResponse({'success': True}, status=200)
                
            else:
                return JsonResponse({"success": False}, status=500)
        else:
            return JsonResponse({"Error": True}, status=400)

class FollowUser(View):
    model = get_user_model()
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id", None)
        username = request.POST.get("username", None)
        action = request.POST.get('action')
        if action and user_id:
            user = get_object_or_404(self.model, pk=user_id, username=username)
            if request.user != user:
                if action == 'follow' and request.user not in user.followers.all():
                    Contact.objects.get_or_create(user_from=request.user, user_to=user)
                else:
                    Contact.objects.filter(user_from=request.user, user_to=user).delete()
                return JsonResponse({"success": True}, status=200)
            else:
                pass
        else:
            return JsonResponse({"success": False}, status=404)

class DeleteFeedbackView(View):
    model = Feedback

    def get(self, request, *args, **kwargs):
        if request.headers['X-Requested-With'] ==  'XMLHttpRequest':
            feedback_id = request.GET.get("feedback_id", None)
            feedback_uuid = request.GET.get("feedback_uuid", None)

            if feedback_id and feedback_uuid:
                feedback_instance = get_object_or_404(self.model, pk=feedback_id)
                if feedback_instance.user == request.user:
                    feedback_instance.delete()
                    data = {
                        'deleted': True
                    }
                    return JsonResponse(data)
                else:
                    return JsonResponse({'error': 'Bad request'}, status=400)

            else:
                return 
        else:
            return JsonResponse({'error': 'Bad request'}, status=400)