from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import datetime

#from django.template import RequestContext , loader

from polls.models import Question, Choice
from polls.forms import UserForm, UserProfileForm

#class IndexView(generic.ListView):
#	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#output = ', '.join([p.question for p in latest_question_list])
	#template = loader.get_template('polls/index.html')
#	context = {	'latest_question_list' : latest_question_list }
	#return HttpResponse(template.render(context))
#	return render(request, 'polls/index.html', context)

def register(request):
	registered=False

	if(request.method) == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password) 
			user.save()
			profile = profile_form.save(commit=False)
			profile.user=user

			if 'picture' in request.FILES:
				profile.picture = request.Files[ 'picture']

			profile.save()
			registered = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,'polls/register.html' , 
		{ 'user_form': user_form, 'profile_form':profile_form, 'registered':registered})

def user_login(request):
	if request.method == 'POST': 
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				print "abc"
				return HttpResponseRedirect('/polls/')
			else:
				return HttpResponse("Your account is disabled")
		else:
			print "Invalid Login details : {0} , {1} ".format(username, password)
			return HttpResponse(" Invalid login details supplied")
	else:
		return render(request, 'polls/login.html', {})


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/polls/')


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'


	def get_queryset(self):
		a=[]
		for q in Question.objects.all():
			c=q.choice_set.all()
			if c :
				if q.pub_date<=timezone.now():
					a.append(q)
		#Q=Question.objects.create(question="How are you?", pub_date=timezone.now()-datetime.timedelta(days=2)) 
		#a.append(Q)

		return a

		#return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())
#@login_required
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
	p=get_object_or_404(Question,pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question' : p,
			'error_message' : "You did'nt select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results' , args=(p.id,)))

