from typing import Dict, Any

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch

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
        print("someone called me")
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

            return redirect('shots:shot_details', shot_uuid=shot.shot_uuid)

        else:
            return render(request, 'shots/create_shot.html', {'form': form})

class DeleteShotView(LoginRequiredMixin, DeleteView):
    slug_field = 'shot_uuid'
    slug_url_kwarg = 'shot_uuid'
    template_name = 'shots/delete_shot.html'
    model = Shot
    success_url = reverse_lazy('shots:shot_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponseServerError()
