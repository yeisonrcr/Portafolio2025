from django.shortcuts import render, HttpResponse

def blog(request):
    if request.method == 'POST':
        # Manejo del caso POST
        return render(request, 'blog/blog.html')
    elif request.method == 'GET':
        # Manejo del caso GET
        return render(request, 'blog/blog.html')
    else:
        # Si el método de solicitud no es GET o POST
        return HttpResponse(status=405)
