from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView 

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()


from accounts.forms import AccountSignupForm
from polls.models import QuestionUser


class AccountCreateView(CreateView):
    model = User
    template_name = 'registration/signup_form.html'
    form_class = AccountSignupForm
    success_url = reverse_lazy('login')
    success_message = 'Usuario Cadastrado com Sucesso'

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        form.save()
        messages.success(self.request, self.success_message) 

        return super(AccountCreateView, self).form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView ):
    model = User
    template_name = 'accounts/user_form.html'
    #form_class = AccountSignupForm
    fields=('first_name', 'email', 'imagem')
    success_url = reverse_lazy('index')
    success_message = 'Perfil Atualizado com Sucesso'

    # editar o proprio perfil
    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        user = self.request.user
        if user is None or not user.is_authenticated or user_id != user.id:
            return User.objects.none()
        
        return User.objects.filter(id=user.id)

    def form_valid(self, form):
        messages.success(self.request, self.success_message) 
        return super(AccountUpdateView, self).form_valid(form)


class AccountTemplateView(TemplateView):
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(AccountTemplateView, self).get_context_data(**kwargs)
        voted = QuestionUser.objects.filter(user=self.request.user)
        context['questions_voted'] = voted
        return context


