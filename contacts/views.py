from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Contact
from django.urls import path
from . import views
from django.shortcuts import render
from .forms import ContactForm
from django.shortcuts import get_object_or_404, redirect
# Create your views here.


def home(request):
    return render(request, "home.html")


def contacts(request):
    mycontact = Contact.objects.all().values()
    template = loader.get_template('allcontacts.html')
    context = {
        'ycontact': mycontact,
    }
    return HttpResponse(template.render(context, request))
# HttpResponse just returns raw text. It does not know how to render a template file


def formcont(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Firstname = form.cleaned_data['firstname']
            Lastname = form.cleaned_data['lastname']
            Phone = form.cleaned_data['phone']
            Email = form.cleaned_data['email']
            print('Name:', Firstname, Lastname)
            print('Phone:', Phone)
            print('Email:', Email)
            # to print form in database
            Contact.objects.create(
                firstname=Firstname,
                lastname=Lastname,
                phone=Phone,
                email=Email
            )
            form = ContactForm()
            return render(request, "formcontact.html", {'form': form, 'success': True})
    else:
        form = ContactForm()
    return render(request, "formcontact.html", {'form': form})


def delete(request, x_id):
    # to fetch context for editing or deleting
    mycontact = get_object_or_404(Contact, id=x_id)
    mycontact.delete()
    return redirect('contacts')


def edit(request, x_id):
    mycontact = get_object_or_404(Contact, id=x_id)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Firstname = form.cleaned_data['firstname']
            Lastname = form.cleaned_data['lastname']
            Phone = form.cleaned_data['phone']
            Email = form.cleaned_data['email']

            # update the existing contact
            mycontact.firstname = Firstname
            mycontact.lastname = Lastname
            mycontact.phone = Phone
            mycontact.email = Email
            mycontact.save()  # save the updates

            return redirect('contacts')  # returns to contact list
    else:
        form = ContactForm(initial={
            'firstname': mycontact.firstname,
            'lastname': mycontact.lastname,
            'phone': mycontact.phone,
            'email': mycontact.email
        })
    return render(request, 'editcontact.html', {'form': form})
