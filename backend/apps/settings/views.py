from typing import Any

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name: str = "settings/settings.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if isinstance(user, (AbstractBaseUser, User)):
            context["password_change_form"] = PasswordChangeForm(user=user)
        return context

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if not isinstance(request.user, (AbstractBaseUser, User)):
            return redirect("login")

        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            messages.success(
                request, "Your password was successfully updated!"
            )
            return redirect(reverse_lazy("settings"))
        else:
            context = self.get_context_data(**kwargs)
            context["password_change_form"] = password_change_form
            return self.render_to_response(context)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm

    def form_valid(self, form: Any) -> HttpResponse:
        form.save()
        return JsonResponse({"success": True})

    def form_invalid(self, form: Any) -> HttpResponse:
        return JsonResponse({"success": False, "errors": form.errors})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["password_change_form"] = self.get_form()
        return context
