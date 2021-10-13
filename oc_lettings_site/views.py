from django.shortcuts import render


def index(request):
    return render(request, 'oc_lettings_site/index.html')
