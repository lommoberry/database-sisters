from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# from .forms import YourForm

# Create your views here.
def add_journal_request(request):
    return render(request, "editingdatabase/adding.html")


def add_data(request):
    if request.method == 'POST':
    #     form = YourForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('success')  # Redirect to a success page
    # else:
    #     form = YourForm()
        journalTitle = request.POST.get('journalTitle')
        auth_fname = request.POST.get('auth_fname')
        countryorigin = request.POST.get('auth_lname')
        countrytravel = request.POST.get('auth_lname')
        century = request.POST.get('auth_lname')
        file = request.POST.get('auth_lname')

#parse journal txt create num entries and journal entries and site etc
    with connection.cursor() as cursor:
        sql = "INSERT INTO journal (journalTitle, auth_fname, countryorigin, century) VALUES (%s, %s)"
        cursor.execute(sql, [journalTitle, auth_fname])
    return redirect('editingdatabase/success.html')
    return render(request, 'adding.html', {'form': form})
