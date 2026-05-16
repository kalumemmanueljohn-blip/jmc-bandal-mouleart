from django.db import models
# from utils.compressors import compress_image, compress_video  # ← COMMENTÉ TEMPORAIREMENT

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='gallery/', verbose_name="Image")
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True)
    taken_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de l'événement")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['-uploaded_at']
    
    def save(self, *args, **kwargs):
        # Compression DÉSACTIVÉE
        # try:
        #     if self.image and hasattr(self.image, 'file'):
        #         if self.image.size > 500 * 1024:
        #             self.image = compress_image(self.image, max_size=1200, quality=75)
        # except Exception as e:
        #     print(f"Erreur compression: {e}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class GalleryVideo(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    video_url = models.URLField(blank=True, null=True, verbose_name="Lien YouTube/Vimeo")
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True, verbose_name="Fichier vidéo (MP4)")
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True, verbose_name="Miniature")
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    
    class Meta:
        verbose_name = "Vidéo"
        verbose_name_plural = "Vidéos"
        ordering = ['-uploaded_at']
    
    def save(self, *args, **kwargs):
        # Compression DÉSACTIVÉE
        # if self.video_file and hasattr(self.video_file, 'file'):
        #     if self.video_file.size > 10 * 1024 * 1024:
        #         try:
        #             self.video_file = compress_video(self.video_file, max_width=854, bitrate='800k', fps=24)
        #         except Exception as e:
        #             print(f"Erreur compression vidéo: {e}")
        # 
        # if self.thumbnail and hasattr(self.thumbnail, 'file'):
        #     if self.thumbnail.size > 200 * 1024:
        #         self.thumbnail = compress_image(self.thumbnail, max_size=640, quality=70)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_video_id(self):
        """Extrait l'ID d'une vidéo YouTube"""
        if self.video_url:
            if 'youtu.be' in self.video_url:
                return self.video_url.split('/')[-1]
            elif 'youtube.com' in self.video_url:
                return self.video_url.split('v=')[-1].split('&')[0]
        return None
    
    def get_embed_url(self):
        """Retourne l'URL embed pour YouTube"""
        video_id = self.get_video_id()
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None
