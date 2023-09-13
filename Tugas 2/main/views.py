from django.shortcuts import render


# Create your views here.
def show_main(request):
    context = {
        'name': 'Daffa Al Fathan Zaki',
        'class': 'PBP A',
        'amount': 1,
        'description': "Test",
    }

    return render(request, "main.html", context)