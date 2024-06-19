from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
import google.generativeai as genai
import os
from .models import Chat
from django.utils import timezone
from dotenv import load_dotenv
load_dotenv()

# Create your views here.

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def ask_geminiai(message):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
        )
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I am unable to respond at the moment."

def chatapp(request):
    # chats = Chat.objects.filter(user=request.user)
    user_id = request.user.id if request.user.is_authenticated else None
    chats = Chat.objects.filter(user_id=user_id)
    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_geminiai(message)
        print(response)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chat2.html",{'chats': chats})
  


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('chatapp')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                login(request, user)
                return redirect('chatapp')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')