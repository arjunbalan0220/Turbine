
from django.shortcuts import render, redirect
from .forms import  ContactForm
from django.contrib import messages

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect("Home")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})