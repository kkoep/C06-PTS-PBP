from .forms import ExpForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from faq_recommendations.models import FreqAskedQuestions
from django.core import serializers
from faq_recommendations.models import Experiences
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def show_faq(request):
    data_faq = FreqAskedQuestions.objects.all()    
    context = {
        'faq' : data_faq,
    }
    return render(request, 'freqaskedquestions.html', context)

def show_json(request):
    data = FreqAskedQuestions.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def add_exp(request):
    form = ExpForm(request.POST)
    if(request.method == 'POST'):
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        nomorHP = request.POST.get('nomorHP')
        message = request.POST.get('message')
        new_task = Experiences(nama = nama, email = email, nomorHP = nomorHP, message = message)
        new_task.save()
        return JsonResponse({
            'nama' : nama,
            'email' : email,
            'nomorHP' : nomorHP,
            'message' : message,
        }, status = 200)
    return JsonResponse({
      "status": False,
      "message": form.errors,
      # Insert any extra data if you want to pass data to Flutter
    }, status=401)