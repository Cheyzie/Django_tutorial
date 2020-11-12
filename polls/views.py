from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F, Sum, Subquery
import datetime

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list':latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)
# def detail(request, question_id):
#     question = get_object_or_404(Question ,pk=question_id)
#     return render(request, 'polls/detail.html', {'question':question})
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id )
#     return render(request, 'polls/results.html', {'question':question})

class Custom404View(generic.TemplateView):
    template_name = 'polls/404.html'


def created(request):

    question_text = request.POST['question'] 
    choices = []
    for i in range(0, int(request.POST['choice_counter'])):
        value = request.POST['choice' + str(i+1)]
        if not value == '':
            choices.append(value)
    try:
        if len(choices) < 2 or question_text == '':
            raise Exception
        question = Question.objects.create(question_text=question_text, pub_date=timezone.now())
        for choice in choices:
            question.choice_set.create(choice_text=choice, votes=0)
    except:
         return render(request, 'polls/create.html', {
            'error_message': "Так не пойдет! Введи название и минимум 2 варианта ответа."
        })
    else:
        return HttpResponseRedirect(reverse('polls:index'))
    


class CreateView(generic.TemplateView):
    template_name = 'polls/create.html'



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """
        Возвращает 3 последних опросов
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:3]
class PageView(generic.ListView):
    template_name = 'polls/page.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Возвращает 3 опроса на страницу
        """
        begin_q = 3*self.kwargs['page']
        end_q = begin_q + 3
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[begin_q:end_q]
    
    def get_context_data(self):
        context = super().get_context_data()
        context['page'] = int(self.kwargs['page']) + 1 
        context['next_page'] = int(self.kwargs['page']) + 1 if self.kwargs['page'] + 1 < Question.objects.count()/3 else self.kwargs['page']
        context['prev_page'] = self.kwargs['page'] - 1 if self.kwargs['page'] > 0 else 0
        return context

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    def get(self, request, pk):
        self.object = self.get_object()
        if self.object.is_active():
            return super().get(request, pk)
        else:
            url = reverse('polls:results', args=(pk,))
            return redirect(url)

    



        

class ResultsView(generic.DetailView):

    model = Question
    template_name = 'polls/results.html'
    
        
    
    

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Так не пойдет! Сначала проголосуйте"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))