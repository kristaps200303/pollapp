from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import CustomSignupForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Question, Choice, Response

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mainpage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})
    
from django.contrib.auth.decorators import login_required

@login_required
def mainpage(request):
    polls = Question.objects.prefetch_related('choices').order_by('-created_at').all()
    user_responses = {}
    if request.user.is_authenticated:
        responses = Response.objects.filter(user=request.user).select_related('choice', 'question')
        user_responses = {response.question_id: response.choice_id for response in responses}
    print(user_responses)
    return render(request, 'mainpage.html', {'polls': polls, 'user_responses': user_responses})






def create_poll(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        if question_text:
            question = Question.objects.create(question_text=question_text)
            choices = [(key, value) for key, value in request.POST.items() if key.startswith('choice_')]
            for count, (key, choice_text) in enumerate(choices, start=1):
                if choice_text: 
                    Choice.objects.create(question=question, choice_text=choice_text, order=count)
            return redirect('mainpage')
        else:
            messages.error(request, 'Lūdzu aizpildiet visus lauciņus.')
    return render(request, 'create_poll.html')

import logging
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

logger = logging.getLogger(__name__)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Question, Choice, Response
from django.contrib.auth.decorators import login_required

@login_required
def submit_answer(request, poll_id):
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        
        # Printing to the console (suitable for development)
        print(f"Submitting answer for Question ID: {poll_id}, Choice ID: {choice_id}")
        
        # For production, consider using logging instead
        logger.info(f"Submitting answer for Question ID: {poll_id}, Choice ID: {choice_id}")

        question = get_object_or_404(Question, pk=poll_id)
        choice = get_object_or_404(Choice, pk=choice_id)
        user = request.user
        response, created = Response.objects.update_or_create(
            user=user, question=question,
            defaults={'choice': choice}
        )
        return redirect('mainpage')

    
from django.contrib.auth.decorators import login_required
from .models import Response

@login_required
def view_responses(request):
    responses = Response.objects.all().select_related('user', 'question', 'choice')
    return render(request, 'responses.html', {'responses': responses})


@login_required
def view_question_responses(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    responses = Response.objects.filter(question=question).select_related('user', 'choice')
    return render(request, 'question_responses.html', {'question': question, 'responses': responses})