from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from utils.compressors import compress_image

class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', '⏰ À venir'),
        ('ongoing', '🔴 En cours'),
        ('past', '✅ Passé'),
        ('cancelled', '❌ Annulé'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    date = models.DateTimeField(verbose_name="Date et heure")
    location = models.CharField(max_length=300, verbose_name="Lieu")
    location_link = models.URLField(blank=True, null=True, verbose_name="Lien Google Maps/Zoom")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Image")
    max_participants = models.IntegerField(default=0, verbose_name="Max participants (0 = illimité)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming', verbose_name="Statut")
    is_featured = models.BooleanField(default=False, verbose_name="⭐ À la une")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        ordering = ['date']
        verbose_name = "Événement"
        verbose_name_plural = "📅 Événements"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Compression auto de l'image avant sauvegarde
        try:
            if self.image and hasattr(self.image, 'file') and self.image.size:
                if self.image.size > 500 * 1024:  # 500KB
                    self.image = compress_image(self.image, max_size=1200, quality=75)
        except Exception as e:
            print(f"Erreur compression image: {e}")
            # On continue sans compression en cas d'erreur
        
        super().save(*args, **kwargs)
    
    def is_full(self):
        try:
            if self.max_participants == 0:
                return False
            return self.participants.count() >= self.max_participants
        except:
            return False
    
    def remaining_places(self):
        try:
            if self.max_participants == 0:
                return "Illimité"
            places = self.max_participants - self.participants.count()
            return max(0, places)
        except:
            return "Illimité"
    
    def participants_count(self):
        try:
            return self.participants.count()
        except:
            return 0
    participants_count.short_description = "Participants"

class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants', verbose_name="Événement")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participations', verbose_name="Utilisateur")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Inscrit le")
    attended = models.BooleanField(default=False, verbose_name="Présent")
    
    class Meta:
        unique_together = ['event', 'user']
        verbose_name = "Participant"
        verbose_name_plural = "👥 Participants"
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
