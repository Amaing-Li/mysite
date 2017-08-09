from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
#from django.template import loader
#from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question,Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html' # override the default, polls/question_list.html
    context_object_name = 'latest_question_list' # override the default, question_list

    def get_queryset(self):
#        """Return the last five published questions."""
#        return Question.objects.order_by('-pub_date')[:5]
        """
        Return the last five published questions (not including those set to be 
        published in the future)>
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question # corresponding to the pg table
    template_name = 'polls/detail.html' # override the default, polls/question_detail.html```
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'




#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([q.question_text for q in latest_question_list])
#    return HttpResponse("Hello, world. You're at the polls index.")
#    return HttpResponse(output)
#    template = loader.get_template('polls/index.html')
#    context = {
#        'latest_question_list':latest_question_list,
#    }
#    return HttpResponse(template.render(context,request))
#    return render(request, 'polls/index.html', context) #shortcut

#def detail(request,question_id):
#    return HttpResponse("You're looking at question %s." % question_id)
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    return render(request,'polls/detail.html',{'question':question})
#    question = get_object_or_404(Question,pk=question_id)  #shortcut #decouple
#    return render(request,'polls/detail.html',{'question':question})

#def results(request,question_id):
#    response = "You're looking at the results of question %s."
#    return HttpResponse(request % question_id)
#    question = get_object_or_404(Question,pk=question_id)
#    return render(request,'polls/results.html',{'question':question})
 
def vote(request,question_id):
#    return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
