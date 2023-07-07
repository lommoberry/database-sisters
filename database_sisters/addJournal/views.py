from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

# Create your views here.
def add_journal_request(request):
    return render(request, "editingdatabase/adding.html")


def add_data(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = YourForm()

    return render(request, 'add_data.html', {'form': form})
