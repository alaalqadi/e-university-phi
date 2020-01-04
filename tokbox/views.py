from django.shortcuts import render


def session_view(request):
    context = {
    }
    return render(request, 'sessionScreen.html', context)
