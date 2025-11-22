from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .forms import Registration
from .models import RegistrationForm

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()  
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('signin')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = Registration()

    return render(request, 'register.html', {'form': form})

def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            User = RegistrationForm.objects.get(email=email)
            print(f"User found: {User.email}")
            print(f"Stored Password Hash: {User.password}")
            user = authenticate(request, email=email, password=password)

            
            if check_password(password, User.password):
                print("Password check successful")
                request.session['email'] = User.email
                return redirect('profile')
            else:
                print("Password check failed")
                messages.error(request, "Invalid email or Password")
        except RegistrationForm.DoesNotExist:
            print(f"No User found with email: {email}")
            messages.error(request, "User does not exist")
            
            

    return render(request, "login.html")

def user_logout(request):
    request.session.flush() 
    return redirect('signin')


def profile(request):
    email = request.session.get('email')
    
    if not email:
        messages.error(request, "Please log in first")
        return redirect('signin')

    try:
        User = RegistrationForm.objects.get(email=email)
    except RegistrationForm.DoesNotExist:
        messages.error(request, "User does not exist")
        return redirect('signin')
    
    return render(request, 'profile.html', {'User': User})

