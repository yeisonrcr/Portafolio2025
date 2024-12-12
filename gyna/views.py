from django.shortcuts import render, HttpResponse
# Create your views here.
def gyna(request):
    return HttpResponse("<p>hola</p>")

def ginaLogin(request):
    return render (request, "vehicle/adminlogin.html", {"mensajeMio": "Nada que momstrar"})
