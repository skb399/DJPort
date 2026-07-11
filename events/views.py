from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Display the homepage.
    """

    return render(request, "events/home.html")