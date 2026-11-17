from django.shortcuts import render

def csrf_failure(request,reacon=""):
    return render(request, 'core/404csrf.html',status=404)

def csrf_failure(request,reacon=""):
    return render(request, 'core/403csrf.html',status=403)