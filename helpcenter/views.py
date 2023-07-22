'''Generic module doc-string.'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import UpdateView
from .models import Ticket
from .forms import EditTicketForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def home(request):
    '''This is our homepage!'''
    return render(request, 'helpcenter/home.html', {})

def tickets(request):
    # Check if the user is authenticated (logged in)
    if request.user.is_authenticated:
        # Get all posts by the currently logged-in user
        user_tickets = request.user.posts.all()
    else:
        user_tickets = []  # Return an empty list if the user is not logged in

    return render(request, 'helpcenter/tickets.html', {'user_tickets': user_tickets})


def create(request):
    if request.method == "POST":
        
        ticket_title = request.POST['title']
        subject = request.POST['subject']

        if request.user.is_authenticated:
            new_ticket = Ticket(title=ticket_title, subject=subject, author=request.user)
            new_ticket.save()
        else:
            messages.error(request, "Log in to create a ticket.")

        return redirect("home")
    else:
        return render(request, 'helpcenter/create.html', {})

def list(request):

    return render(request, 'helpcenter/list.html', {})

def about(request):

    return render(request, 'helpcenter/about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.success(request, ("there was an error"))
            return redirect("login")
    else:
        return render(request, 'helpcenter/login.html', {})


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
        else:
            form = UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, "helpcenter/register_user.html", {'form' :form,})

def redirect_home(request):
     return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out.."))
    return redirect("home")

def edit_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.user != ticket.author:
        messages.error(request, "No Permission")
        return HttpResponseRedirect(reverse('tickets'))

    if request.method == "POST":
        form = EditTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket updated")
            return HttpResponseRedirect(reverse('tickets'))
    else:
        form = EditTicketForm(instance=ticket)

    return render(request, 'helpcenter/edit_ticket.html', {'form': form, 'ticket': ticket})

def delete_ticket(request, ticket_id):
    del_ticket = Ticket.objects.get(pk=ticket_id)
    del_ticket.delete()
    return redirect('tickets')