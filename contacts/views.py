from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contact
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contacts = Contact.objects.order_by('-id')
    paginator = Paginator(contacts, 20)

    page = request.GET.get('p')
    contacts = paginator.get_page(page)

    return render(request, 'contacts/index.html', {
        'contacts': contacts
    })


def view_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if not contact.display:
        raise Http404()
    return render(request, 'contacts/view_contact.html', {
        'contact': contact
    })


def search(request):
    term = request.GET.get('term')
    if term is None or not term:
        messages.add_message(request, messages.ERROR, 'empty')
        return redirect('index')
    camps = Concat('name', Value(' '), 'surname')
    contacts = Contact.objects.annotate(
        full_name=camps
    ).filter(
        Q(full_name__icontains=term) | Q(phone__icontains=term)
    )
    paginator = Paginator(contacts, 20)
    page = request.GET.get('p')
    contacts = paginator.get_page(page)

    return render(request, 'contacts/search.html', {
        'contacts': contacts
    })
