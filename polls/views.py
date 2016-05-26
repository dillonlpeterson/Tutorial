from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.

from .models import Question

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
		'latest_question_list':latest_question_list,
	}
	return render(request, 'polls/index.html', context)

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', { 'question':question })

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("You are voting on question %s." % question_id)

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_query_set(self):
		""" Return the last 5 submitted questions """
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]






