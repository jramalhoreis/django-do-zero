import csv
import json
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from django.http import HttpRequest, HttpResponse

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView, FormView

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

from polls.models import Question, Choice
from polls.forms import QuestionForm, QuestionImportForm
from webapp.decorators import class_view_decorator,check_editor_access



#def index (request):
#    aviso = 'AVISO: Esta página não exige login'
#    messages.warning(request, aviso)

#    #return HttpResponse ('Dango Index')
#    return render(request, 'index.html', {'titulo': 'Ultimas Enquetes'})


def index (request, categoria=None):
    aviso = 'AVISO: Esta página não exige login'
    messages.warning(request, aviso)

    #questions=Question.objects.all()
    if categoria is not None:
        questions=Question.objects.filter(categoria=categoria)
    else:
        questions=Question.objects.all()

    categorias = Question.objects.all().values_list(
        'categoria',
        flat=True,
    ).exclude(
        categoria=None
    ).distinct

    context={}
    context['all_questions'] = questions
    context['titulo'] = 'Últimas Enquetes'
    context['categoria'] = categoria
    context['all_categorias'] = categorias

    return render(request, 'polls/questions.html', context)

@login_required
def olax(request):

    return HttpResponse( 'django ola')

@login_required
def ola(request):
    questions=Question.objects.all()
    context={}
    context['all_questions'] = questions
    #print(f'\nquestions {questions.values()}')

    return render( request, 'polls/questions.html', context)


# -------------------------------------------------------------------------------

@class_view_decorator(staff_member_required)
class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    template_name = "polls/question_form.html"
    fields=('question_text', 'pub_date', 'categoria', 'end_date')
    success_url = reverse_lazy('index')
    success_message = 'Pergunta Criada com Sucesso'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, self.success_message)
        return super(QuestionCreateView, self).form_valid(form)
    
    #def form_valid(self, form):
    #    try:
    #        form.instance.question = self.question
    #        response = super(QuestionCreateView, self).form_valid(form)
    #    except (ValidationError) as error:
    #        messages.error(self.request, self.error.message)
    #        return self.form_invalid(form)
    #    else:
    #        messages.success(self.request, self.success_message)
    #        return response
    
    def get_context_data(self, **kwargs) :
        context =  super(QuestionCreateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Criando Pergunta'
        return context



@login_required
def question_create(request):
    context = {}
    form = QuestionForm(request.POST or None, request.FILES or None)
    context['form'] = form
    context['form_title'] = 'Criando Pergunta'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Pergunta Criada com Sucesso')
            return redirect('index')
        
    return render(request, 'polls/question_form.html', context)    

# -------------------------------------------------------------------------------


@class_view_decorator(check_editor_access)
class QuestionUpdateView(LoginRequiredMixin,UpdateView):
    model = Question
    template_name = "polls/question_form.html"
    #fields=('question_text', 'pub_date')
    form_class = QuestionForm
    success_url = reverse_lazy('index')
    success_message = 'Pergunta Atualizada com Sucesso'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(QuestionUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs) :
        context =  super(QuestionUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando Pergunta'
        return context
    

@login_required
def question_update(request, question_id):
    context = {}
    question = get_object_or_404(Question, id=question_id)

    form = QuestionForm(request.POST or None, instance=question)

    context['form'] = form
    context['form_title'] = 'Editando Pergunta'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Pergunta Atualizada com Sucesso')
            return redirect('index')
        
    return render(request, 'polls/question_form.html', context)    




# -------------------------------------------------------------------------------



class QuestionDeleteView(LoginRequiredMixin,DeleteView):
    model = Question
    template_name = "polls/question_confirm_delete_form.html"
    #fields=('question_text', 'pub_date')
    #form_class = QuestionForm
    success_url = reverse_lazy('index')
    success_message = 'Pergunta Excluida com Sucesso'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(QuestionDeleteView, self).form_valid(form)
    
    def get_context_data(self, **kwargs) :
        context =  super(QuestionDeleteView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando Pergunta'
        return context
    

@login_required
def question_delete(request, question_id):
    context = {}
    question = get_object_or_404(Question, id=question_id)

    #form = QuestionForm(request.POST or None, instance=question)

    #context['form'] = form
    #context['form_title'] = 'Editando Pergunta'
    context['object'] = question

    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Pergunta Excluida com Sucesso')
        return redirect('index')
        
    return render(request, 'polls/question_confirm_delete_form.html', context)    




# -------------------------------------------------------------------------------

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'polls/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        question = kwargs.get('object')

        expired = False
        if question.end_date is not None and question.end_date < timezone.now():
            expired = True

        context['total_votes'] = question.get_total_votes()
        context['expired'] = expired

        return context

# -------------------------------------------------------------------------------

# foi refatorado para permitir apenas 1 voto por usuario
#def vote(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    if request.method == 'POST':
#        try:
#            selected_choice = question.choice_set.get(pk=request.POST.get('choice'))
#        except(KeyError, Choice.DoesNotExist):
#            messages.error(request, 'Selectione uma alternativa para votar')
#        else:
#            selected_choice.votes += 1
#            selected_choice.save()
#            messages.success(request, 'Seu voto foi registrado com sucesso')
#            #return redirect(reverse_lazy("question_detail", args=(question_id,)))
#            return redirect(reverse_lazy("polls_results", args=(question_id,)))
#        
#    context = {'question': question}    
#
#    return render(request, 'polls/question_detail.html', context)

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        try:
            selected_choice = question.choice_set.get(pk=request.POST.get('choice'))
            session_user=get_object_or_404(User, id=request.user.id)
            selected_choice.votes += 1
            selected_choice.save(user=session_user)

        except(KeyError, Choice.DoesNotExist):
            messages.error(request, 'Selectione uma alternativa para votar')
        except (ValidationError) as error:
            messages.error(request, error.message)
        else:
            #selected_choice.votes += 1
            #selected_choice.save()
            messages.success(request, 'Seu voto foi registrado com sucesso')
            ##return redirect(reverse_lazy("question_detail", args=(question_id,)))
            return redirect(reverse_lazy("polls_results", args=(question_id,)))
        
    context = {'question': question}    

    return render(request, 'polls/question_detail.html', context)



#-------------------------------------------------------------------------------

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {}
    context['question'] = question
    context['votes'] = question.get_results()

    return render(request, 'polls/results.html', context)



# -------------------------------------------------------------------------------

class QuestionListView(ListView):
    model = Question
    template_name = 'polls/question_list.html'
    context_object_name = 'questions'
    paginate_by = 5
    ordering = ['-pub_date']

# -------------------------------------------------------------------------------



class SobreTemplateView(TemplateView):
    model = Question
    template_name = 'polls/sobre.html'
    
# -------------------------------------------------------------------------------

class ChoiceCreateView(LoginRequiredMixin,CreateView):
    model = Choice
    template_name = "polls/choice_form.html"
    fields=('choice_text', )
    #success_url = reverse_lazy('index')
    success_message = 'Alternativa Criada com Sucesso'

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        return super(ChoiceCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) :
        context =  super(ChoiceCreateView, self).get_context_data(**kwargs)
        context['form_title'] = f'Alternativa para: {self.question.question_text}'
        return context

    #def form_valid(self, form):
    #    form.instance.question = self.question
    #    messages.success(self.request, self.success_message)
    #    return super(ChoiceCreateView, self).form_valid(form)
    
    def form_valid(self, form):
        try:
            form.instance.question = self.question
            #messages.success(self.request, self.success_message)
            response =super(ChoiceCreateView, self).form_valid(form)
        except (ValidationError) as error:
            messages.error(self.request, error.message)
            return self.form_invalid(form)
        else:
            messages.success(self.request, self.success_message)
            return response

    
    def get_success_url(self, *args, **kwargs):
        question_id = self.kwargs.get('pk')
        return reverse_lazy('question_detail', kwargs={'pk': question_id})
    
# -------------------------------------------------------------------------------

class ChoiceUpdateView(LoginRequiredMixin,UpdateView):
    model = Choice
    template_name = "polls/question_form.html"
    fields=('choice_text', )
    #success_url = reverse_lazy('index')
    success_message = 'Alternativa Atualizada com Sucesso'

    #def dispatch(self, request, *args, **kwargs):
    #    self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
    #    return super(ChoiceCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) :
        context =  super(ChoiceUpdateView, self).get_context_data(**kwargs)
        #context['form_title'] = f'Editando Alternativa: {self.question.question_text}'
        context['form_title'] = f'Editando Alternativa: '
        return context

    def form_valid(self, form):
        #form.instance.question = self.question
        messages.success(self.request, self.success_message)
        return super(ChoiceUpdateView, self).form_valid(form)
    
    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id
        return reverse_lazy('question_detail', kwargs={'pk': question_id})
           
# -------------------------------------------------------------------------------

class ChoiceDeleteView(LoginRequiredMixin,DeleteView):
    model = Choice
    template_name = "polls/choice_confirm_delete_form.html"
    #fields=('choice_text', )
    #success_url = reverse_lazy('index')
    success_message = 'Alternativa Excluida com Sucesso'

    #def dispatch(self, request, *args, **kwargs):
    #    self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
    #    return super(ChoiceCreateView, self).dispatch(request, *args, **kwargs)

    #def get_context_data(self, **kwargs) :
    #    context =  super(ChoiceDeleteView, self).get_context_data(**kwargs)
    #    context['form_title'] = f'Excluindo Alternativa: {self.question.question_text}'
    #    return context

    def form_valid(self, form):
        #form.instance.question = self.question
        messages.success(self.request, self.success_message)
        return super(ChoiceDeleteView, self).form_valid(form)
    
    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id
        return reverse_lazy('question_detail', kwargs={'pk': question_id})
           
# -------------------------------------------------------------------------------


class QuestionImportView(LoginRequiredMixin, FormView):
    template_name = 'polls/question_import_form.html'
    parent_class = FormView
    form_class = QuestionImportForm
    success_url = reverse_lazy('index')
    error_message = 'Ocorreu algum erro inesperado'

    def form_valid(self, form):
        if self.request.method == 'POST':
            tmp_file_name = form.cleaned_data.get('tmp_file_name')

            csv_file = open(tmp_file_name)
            csv_reader = csv.DictReader(csv_file)
            question_count = 0

            for row in csv_reader:
                print(f'\nrow {row}')
                print(f'question_text: { row.get("question_text")}')
                print(f'pub_date.....: { row.get("pub_date")}')
                pub_date = datetime.fromisoformat(row.get('pub_date'))
                #pub_date = datetime.fromisoformat(row['pub_date'])
                question = Question (
                    question_text = row.get('question_text'),
                    pub_date = pub_date
                )

                question.save()
                question_count += 1

            success_message= f'{question_count} perguntas importadas com sucesso'
            messages.success(self.request, success_message)

        return super(QuestionImportView, self).form_valid(form)


def poll_send(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question_url = reverse_lazy('question_detail', args=[question_id])

    try:
        email = request.POST.get('email')
        print(f'email {email}')
        if len(email) < 5:
            raise ValueError('E-mail Invalido')
        print(f'Estou aqui')
        link = f'{request._current_scheme_host}{question_url}'
        print(f'link {link}')
        template='polls/question_send'
        text_message= render_to_string(f'{template}.txt', {'question_link': link })
        html_message= render_to_string(f'{template}.html', {'question_link': link })

        #send_mail(
        #subject = 'Encontrei esta enquete e acredito que possa te interessar',
        #message = text_message,
        #from_email = settings.EMAIL_HOST_USER,
        #recipient_list=[email],
        #html_message=html_message
        #)
        #print(f'subject {subject}')
        #print(f'message {message}')
        #print(f'from_email {from_email}')
        #print(f'recipient_list {recipient_list}')
        #print(f'html_message {html_message}')
        #print(f'link {link}')
        #print(f'email {email}')
        #print(f'text_message {text_message}')

        send_mail(
            subject = 'Encontrei esta enquete e acredito que possa te interessar',
            message = text_message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        #send_mail(subject='Assunto', message='Este é o meu primeiro email', from_email='jramalho.reis@gmail.com', recipient_list=['ramalhoreis@uol.com.br'])

        messages.success('Enquete compartilhada com sucesso')

    except ValueError as error:
        messages.error(request, error)

    except Exception as error:
        messages.error(request, 'Erro ao enviar mensagem')
        messages.error(request, error)
        
    return redirect(question_url)



@login_required
def questions_export_csv(request):
    response=HttpResponse(
        content_type = "text/csv",
        headers={'Content-Disposition': 'attachment; filename="questions.csv'}
    )

    questions = Question.objects.all()

    writer = csv.writer(response)
    writer.writerow(['question_text', 'pub_date'])

    for line in questions:
        writer.writerow([line.question_text, f'{line.pub_date:%Y-%m-%d}'])

    return response



def get_all_questions(request):
    questions = list(Question.objects.values('pk', 'question_text', 'pub_date', 'categoria'))
    data = {'success': True, 'questions': questions}
    json_data = json.dumps(data, indent=1, cls=DjangoJSONEncoder)
    response = HttpResponse(json_data, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'

    return response




