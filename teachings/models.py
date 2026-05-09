from django.db import models
# Compression audio désactivée sur Render (pydub incompatible)
from utils.compressors import compress_image, compress_video
# compress_audio n'est plus importé

class TeachingCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, help_text="Icône Bootstrap (ex: bi-mic)", verbose_name="Icône")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.name


class Teaching(models.Model):
    TYPE_CHOICES = [
        ('audio', '🎵 Audio'),
        ('video', '🎥 Vidéo'),
        ('pdf', '📄 PDF'),
        ('text', '📝 Texte'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    category = models.ForeignKey(TeachingCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachings', verbose_name="Catégorie")
    speaker = models.CharField(max_length=100, verbose_name="Prédicateur/Enseignant")
    description = models.TextField(verbose_name="Description")
    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Type de contenu")
    file = models.FileField(upload_to='teachings/', blank=True, null=True, verbose_name="Fichier")
    video_url = models.URLField(blank=True, null=True, verbose_name="Lien YouTube/Vimeo")
    external_link = models.URLField(blank=True, null=True, verbose_name="Lien externe")
    duration = models.CharField(max_length=20, blank=True, help_text="ex: 34min", verbose_name="Durée")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0, verbose_name="Vues")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Enseignement"
        verbose_name_plural = "Enseignements"
    
    def save(self, *args, **kwargs):
        # Compression selon le type de contenu
        if self.file and hasattr(self.file, 'file'):
            # Pour les fichiers audio (MP3) - Compression manuelle seulement
            if self.content_type == 'audio' and self.file.size > 5 * 1024 * 1024:  # > 5MB
                print(f"ℹ️ Audio {self.title} fait {self.file.size//1024//1024}MB")
                print(f"   💡 Pour accélérer l'upload, compressez l'audio avant de l'envoyer")
                print(f"   📊 Taille recommandée: < 2MB")
            
            # Pour les fichiers vidéo (MP4)
            elif self.content_type == 'video' and self.file.size > 10 * 1024 * 1024:  # > 10MB
                try:
                    self.file = compress_video(self.file, max_width=854, bitrate='800k', fps=24)
                    print(f"✅ Vidéo compressée: {self.title}")
                except Exception as e:
                    print(f"❌ Erreur compression vidéo {self.title}: {e}")
            
            # Pour les fichiers PDF (ne pas compresser)
            elif self.content_type == 'pdf':
                # Les PDF ne sont pas compressés
                pass
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_icon(self):
        """Retourne l'icône Bootstrap selon le type"""
        icons = {
            'audio': 'bi-mic-fill',
            'video': 'bi-camera-reels-fill',
            'pdf': 'bi-file-pdf-fill',
            'text': 'bi-file-text-fill',
        }
        return icons.get(self.content_type, 'bi-file-earmark')
    
    def get_type_display_icon(self):
        """Retourne l'affichage du type avec icône"""
        types = {
            'audio': '🎵 Audio',
            'video': '🎥 Vidéo',
            'pdf': '📄 PDF',
            'text': '📝 Texte',
        }
        return types.get(self.content_type, self.content_type)
