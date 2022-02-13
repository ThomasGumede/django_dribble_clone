from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.urls.base import reverse_lazy
from .forms import RegistrationForm, PwdResetConfirmForm, AccountUpdateForm, GeneralEditForm
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()
# Create your views here.
from django.views.generic import View, CreateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from shots.models import Shot

class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result


class AccountDetailsView(DetailView):
    model = User
    slug_field = 'username'
    context_object_name = 'user'
    slug_url_kwarg = 'username'
    query_pk_and_slug = True
    template_name = 'accounts/manage/user_index.html'

class AccountLikesView(View):
    """
        Displays all shots that the user liked. 
    """
    model = User
    template_name = "accounts/manage/account_likes.html"

    def get(self, request, username, pk, *args, **kwargs):
        # filter shots
        try:
            user = self.model.objects.prefetch_related("likes").get(username=username, pk=pk)
            return render(request, self.template_name, {"user": user})
        except self.model.DoesNotExist:
            pass

class EditProfileView(LoginRequiredMixin, View):
    model = None
    form_class = AccountUpdateForm
    template_name = "accounts/manage/edit_profile.html"

    def get_user(self, username, pk):
        user = get_object_or_404(User, username=username, pk=pk)
        return user

    def dispatch(self, request, username, pk, *args, **kwargs):
        self.model = self.get_user(username, pk)
        if request.user != self.model:
            pass
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.model)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            self.model.photo = cd["photo"]
            self.model.location = cd["location"]
            self.model.first_name = cd["first_name"]
            self.model.last_name = cd["last_name"]
            self.model.website = cd["website"]
            self.model.biography = cd["biography"]
            self.model.save(update_fields=["first_name", "last_name", "website", "biography", "location", "photo"])
            
            return redirect("accounts:account_update", username=self.model.username, pk=self.model.pk)
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})
    
class GeneralView(LoginRequiredMixin, View):
    model = None
    form_class = GeneralEditForm
    template_name = "accounts/manage/general.html"

    def get_user(self, username, pk):
        user = get_object_or_404(User, username=username, pk=pk)
        return user

    def dispatch(self, request, username, pk, *args, **kwargs):
        self.model = self.get_user(username, pk)
        if request.user != self.model:
            pass
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.model)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            self.model.username = cd["username"]
            self.model.email = cd["email"]
            self.model.save(update_fields=["username", "email"])
            
            return redirect("accounts:general_edit", username=self.model.username, pk=self.model.pk)
        else:
            
            return render(request, self.template_name, {"form": form})

class UpdatePasswordView(LoginRequiredMixin, View):

    form_class = PasswordChangeForm
    template_name = "accounts/password/manage/change_password.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class(request.user)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect("accounts:password_change")
        else:
            return render(request, self.template_name, {"form": form})

class PwdResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password/pwd__reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_class=PwdResetConfirmForm