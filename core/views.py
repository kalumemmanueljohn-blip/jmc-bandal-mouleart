from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.http import HttpResponse
from django.utils import timezone
import csv

from events.models import Event
# from core.models import VerseOfTheDay  # ❌ COMMENTÉ - Modèle inexistant
from .models import Subscriber


def home(request):
    upcoming_events = Event.objects.filter(
        status='upcoming', 
        date__gte=timezone.now()
    )[:3]
    # verse_of_day = VerseOfTheDay.objects.filter(is_active=True).first()  # ❌ COMMENTÉ
    
    context = {
        'upcoming_events': upcoming_events,
        # 'verse_of_day': verse_of_day,  # ❌ COMMENTÉ
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def save_phone(request):
    """Sauvegarder le numéro de téléphone"""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        name = request.POST.get('name', '')
        
        if not phone:
            messages.error(request, "❌ Veuillez saisir un numéro de téléphone.")
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        
        phone = phone.strip()
        
        obj, created = Subscriber.objects.get_or_create(
            phone_number=phone,
            defaults={'name': name}
        )
        
        if created:
            messages.success(request, "✅ Merci ! Vous recevrez nos actualités par WhatsApp.")
        else:
            messages.info(request, "📱 Ce numéro est déjà enregistré dans notre liste.")
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@staff_member_required
def subscribers_list(request):
    """Page personnalisée pour voir les abonnés WhatsApp"""
    subscribers = Subscriber.objects.all().order_by('-created_at')
    
    search = request.GET.get('search', '')
    if search:
        subscribers = subscribers.filter(
            models.Q(phone_number__icontains=search) |
            models.Q(name__icontains=search)
        )
    
    status = request.GET.get('status', '')
    if status == 'active':
        subscribers = subscribers.filter(is_active=True)
    elif status == 'inactive':
        subscribers = subscribers.filter(is_active=False)
    
    context = {
        'subscribers': subscribers,
        'search': search,
        'status': status,
        'total_count': Subscriber.objects.count(),
        'active_count': Subscriber.objects.filter(is_active=True).count(),
    }
    return render(request, 'core/subscribers.html', context)


@staff_member_required
def subscriber_toggle(request, id):
    """Activer/Désactiver un abonné"""
    subscriber = get_object_or_404(Subscriber, id=id)
    subscriber.is_active = not subscriber.is_active
    subscriber.save()
    messages.success(request, f'✅ Abonné {subscriber.phone_number} {"activé" if subscriber.is_active else "désactivé"}')
    return redirect('subscribers_list')


@staff_member_required
def subscriber_delete(request, id):
    """Supprimer un abonné"""
    subscriber = get_object_or_404(Subscriber, id=id)
    phone = subscriber.phone_number
    subscriber.delete()
    messages.success(request, f'✅ Abonné {phone} supprimé avec succès !')
    return redirect('subscribers_list')


@staff_member_required
def export_subscribers_csv(request):
    """Exporter les abonnés WhatsApp en CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="abonnes_whatsapp.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Numéro de téléphone', 'Nom', "Date d'inscription", 'Actif'])
    
    subscribers = Subscriber.objects.all().order_by('-created_at')
    
    for subscriber in subscribers:
        writer.writerow([
            subscriber.phone_number,
            subscriber.name if subscriber.name else '',
            subscriber.created_at.strftime('%d/%m/%Y à %H:%M'),
            'Oui' if subscriber.is_active else 'Non'
        ])
    
    return response
