from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls.base import reverse_lazy
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.edit import FormView


#AUTH VIEWS




class LoginView(FormView):
    template_name = "account_login.html"
    form_class = AuthenticationForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse_lazy('home_page'))
        return super().form_valid(form)


class ConfirmLogoutView(TemplateView):
    template_name = "account_logout_yes_no_confirmation.html"

class LogoutView(RedirectView):
    url = reverse_lazy("home_page")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

