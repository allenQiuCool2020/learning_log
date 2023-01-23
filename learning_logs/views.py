from django.shortcuts import render, HttpResponseRedirect, reverse, Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
	return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
	topics = Topic.objects.filter(owner=request.user).order_by('data_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	topic = Topic.objects.get(id=topic_id)
	if topic.owner != request.user:
		raise Http404
	entries = topic.entry_set.order_by('-data_added')
	context = {'topic':topic, 'entries':entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	if request.method != 'POST':
		form = TopicForm()
	else:
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			
			return HttpResponseRedirect(reverse('topics'))
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	topic = Topic.objects.get(id=topic_id)


	form = EntryForm()
	if request.method == 'POST':
		form = EntryForm(request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			#print(new_entry.topic)
			new_entry.save()
			return HttpResponseRedirect(reverse('topic', args=[topic_id]))
	context = {'form': form, 'topic': topic }
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic

	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('topic', args=[topic.id]))
	context = {'entry': entry, 'topic': topic, 'form':form}
	return render(request, 'learning_logs/edit_entry.html', context)


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def register(request):
	if request.method != 'POST':
		form = UserCreationForm()
	else:
		form = UserCreationForm(data = request.POST)
		if form.is_valid():
			new_user = form.save()
			authenticated_user = authenticate(username=new_user.username, 
				password=request.POST['password1'])
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse('index'))
	context = {'form': form}
	return render(request, 'learning_logs/register.html', context)








