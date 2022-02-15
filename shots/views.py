from typing import Dict, Any

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
from shots.models import Shot, ShotFile, ShotCategory
from shots.forms import ShotForm
from actions.forms import FeedbackForm
from actions.views import CreateFeedbackView
from actions.models import Feedback



class ShotListView(View):
    template_name = 'shots/shot_list.html'

    def get(self, request, category=None, *args, **kwargs):
        page = request.GET.get("page", 1)
        if category:
            category = get_object_or_404(ShotCategory, slug=category)
            qs = Shot.objects.filter(category=category).order_by('-created')
            shot_qs = qs.select_related('user').prefetch_related('user_like')
        else:
            shot_qs = Shot.objects.select_related("user").prefetch_related('user_like').order_by('-created')

        
        paginator = Paginator(shot_qs, 12)
        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)

            
        context = {
            "shots": qs
        }
        return render(request, self.template_name, context)

class ShotView(SingleObjectMixin, View):
    feedback_qs = Feedback.objects.select_related('user')
    shot_qs = Shot.objects.select_related('user')
    my_queryset = shot_qs.prefetch_related("user_like", "shot_files").prefetch_related(Prefetch('feedbacks', queryset=feedback_qs))
    context_object_name = 'shot'
    template_name = 'shots/shot_detail.html'
    slug_field = 'shot_uuid'
    slug_url_kwarg = 'shot_uuid'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.my_queryset)
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['feedbackform'] = FeedbackForm

        return context

class ShotDetailsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = ShotView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CreateFeedbackView.as_view()
        return view(request, *args, **kwargs)

class CreateShotView(LoginRequiredMixin, View):
    form_class = ShotForm
    template_name = 'shots/create_shot.html'

    def get(self, request, *args, **kwargs):
        
        return render(request, 'shots/create_shot.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            files = request.FILES.getlist('files')
            cd = form.cleaned_data
            
            shot, created = Shot.objects.get_or_create(user=request.user ,category=cd['category'], title=cd['title'], description=cd['description'], cover_shot=cd['cover_shot'])
            if created:
                
                if len(files) > 0:
                    
                    for file in files:
                        shot_file = ShotFile(shot=shot, file=file)
                        shot_file.save()
                else:
                    pass
            else:
                return HttpResponseServerError()
            messages.success(request, "Shot was created successfully")
            return redirect('shots:shot_details', shot_uuid=shot.shot_uuid)

        else:
            messages.error(request, "Something is missing, please fix below errors")
            return render(request, 'shots/create_shot.html', {'form': form})

class DeleteShotView(LoginRequiredMixin, SingleObjectMixin, View):
    slug_field = 'shot_uuid'
    slug_url_kwarg = 'shot_uuid'
    model = Shot
    success_url = reverse_lazy('shots:shot_list')
    deleted = False
    
    def delete(self, request):
        self.object = self.get_object()     
        if self.object.user == request.user:
            self.object.delete()     
            self.deleted = True
        else:
            self.deleted = False

    def post(self, request, shot_uuid, *args, **kwargs):
        self.delete(request)
        if self.deleted:
            messages.success(request, "Shot was deleted successfully")
            return JsonResponse({"success": True, "url": self.success_url}, status=200)
        else:
            messages.error(request, "Something isn't right")
            messages.warning(request, "You tried deleting someone ele\'s shot, You blocked")
            get_object_or_404(User, username=request.user.username).delete()

            return JsonResponse({"success": False, "url": reverse_lazy("accounts:signup")}, status=500)
