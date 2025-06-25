from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Puppy, CustomUser, Message, Reunion
from .forms import (
    LostPuppyForm, 
    FoundPuppyForm, 
    UserProfileForm, 
    MessageForm, 
    SearchForm,
    ReunionForm
)
from django_tables2 import RequestConfig
from .tables import PuppyTable

def index(request):
    recent_puppies = Puppy.objects.filter(status='LOST').order_by('-created_at')[:4]
    success_stories = Reunion.objects.all().order_by('-reunion_date')[:3]
    return render(request, 'index.html', {
        'recent_puppies': recent_puppies,
        'success_stories': success_stories
    })

@login_required
def dashboard(request):
    user_puppies = Puppy.objects.filter(created_by=request.user).order_by('-created_at')
    messages_received = Message.objects.filter(receiver=request.user).order_by('-sent_at')[:5]
    
    table = PuppyTable(user_puppies)
    RequestConfig(request).configure(table)
    
    return render(request, 'dashboard.html', {
        'puppy_table': table,
        'messages': messages_received
    })

@login_required
def report_lost(request):
    if request.method == 'POST':
        form = LostPuppyForm(request.POST, request.FILES)
        if form.is_valid():
            puppy = form.save(commit=False)
            puppy.created_by = request.user
            puppy.status = 'LOST'
            puppy.save()
            messages.success(request, 'Lost puppy report submitted successfully!')
            return redirect('search_puppies')
    else:
        form = LostPuppyForm()
    return render(request, 'report_lost.html', {'form': form})

@login_required
def report_found(request):
    if request.method == 'POST':
        form = FoundPuppyForm(request.POST, request.FILES)
        if form.is_valid():
            puppy = form.save(commit=False)
            puppy.created_by = request.user
            puppy.status = 'FOUND'
            puppy.save()
            messages.success(request, 'Found puppy report submitted successfully!')
            return redirect('search_puppies')
    else:
        form = FoundPuppyForm()
    
    return render(request, 'report_found.html', {'form': form})

def search_puppies(request):
    form = SearchForm(request.GET or None)
    puppies = Puppy.objects.all()
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        breed = form.cleaned_data.get('breed')
        color = form.cleaned_data.get('color')
        status = form.cleaned_data.get('status')
        location = form.cleaned_data.get('location')
        
        if search_query:
            puppies = puppies.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if breed:
            puppies = puppies.filter(breed__iexact=breed)
            
        if color:
            puppies = puppies.filter(color__iexact=color)
            
        if status and status != 'all':
            puppies = puppies.filter(status__iexact=status)
            
        if location:
            puppies = puppies.filter(last_seen_location__icontains=location)
    
    table = PuppyTable(puppies)
    RequestConfig(request).configure(table)
    
    return render(request, 'search.html', {
        'form': form,
        'puppy_table': table
    })

def puppy_detail(request, puppy_id):
    puppy = get_object_or_404(Puppy, id=puppy_id)
    message_form = MessageForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = request.user
            message.receiver = puppy.created_by
            message.puppy = puppy
            message.save()
            messages.success(request, 'Your message has been sent!')
            return redirect('puppy_detail', puppy_id=puppy.id)
    
    return render(request, 'puppy_detail.html', {
        'puppy': puppy,
        'message_form': message_form,
        'has_3d_model': bool(puppy.model_3d)
    })

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})

@login_required
def mark_as_reunited(request, puppy_id):
    puppy = get_object_or_404(Puppy, id=puppy_id, created_by=request.user)
    
    if request.method == 'POST':
        form = ReunionForm(request.POST)
        if form.is_valid():
            reunion = form.save(commit=False)
            reunion.puppy = puppy
            reunion.owner = request.user
            reunion.save()
            
            puppy.status = 'REUNITED'
            puppy.save()
            
            messages.success(request, f'{puppy.name} has been marked as reunited!')
            return redirect('dashboard')
    else:
        form = ReunionForm()
    
    return render(request, 'mark_reunited.html', {
        'puppy': puppy,
        'form': form
    })