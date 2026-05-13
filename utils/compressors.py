# utils/compressors.py
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import tempfile
import os

# ============ COMPRESSION IMAGES ============
def compress_image(image_file, max_size=1200, quality=75):
    """
    Compresse une image
    - max_size: largeur maximale en pixels
    - quality: qualité JPEG (1-100)
    """
    try:
        img = Image.open(image_file)
        
        # Conversion en RGB si nécessaire
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        # Redimensionnement
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Compression
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        # Nouveau nom
        name = image_file.name
        if '.' in name:
            name = name.rsplit('.', 1)[0] + '.jpg'
        else:
            name = name + '.jpg'
        
        return ContentFile(output.read(), name=name)
    
    except Exception as e:
        print(f"Erreur compression image: {e}")
        return image_file


def compress_image_webp(image_file, max_size=1200, quality=75):
    """Compresse une image en format WebP (plus petit)"""
    try:
        img = Image.open(image_file)
        
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        output = BytesIO()
        img.save(output, format='WEBP', quality=quality, optimize=True)
        output.seek(0)
        
        name = image_file.name
        if '.' in name:
            name = name.rsplit('.', 1)[0] + '.webp'
        else:
            name = name + '.webp'
        
        return ContentFile(output.read(), name=name)
    
    except Exception as e:
        print(f"Erreur compression image WebP: {e}")
        return image_file


# ============ COMPRESSION VIDEOS (DÉSACTIVÉE POUR RENDER) ============
def compress_video(video_file, max_width=854, bitrate='800k', fps=24):
    """
    ⚠️ Compression vidéo désactivée sur Render (trop gourmande en mémoire)
    Retourne le fichier original sans modification
    """
    print(f"ℹ️ Vidéo non compressée (désactivé sur Render): {video_file.name}")
    print(f"   💡 Pour réduire la taille, compressez la vidéo avant de l'uploader")
    print(f"   📊 Taille actuelle: {video_file.size // 1024 // 1024} MB")
    return video_file


def compress_video_high_quality(video_file):
    """Compression haute qualité - désactivée"""
    print(f"ℹ️ Compression vidéo désactivée: {video_file.name}")
    return video_file


def compress_video_medium_quality(video_file):
    """Compression qualité moyenne - désactivée"""
    print(f"ℹ️ Compression vidéo désactivée: {video_file.name}")
    return video_file


def compress_video_low_quality(video_file):
    """Compression basse qualité - désactivée"""
    print(f"ℹ️ Compression vidéo désactivée: {video_file.name}")
    return video_file


# ============ COMPRESSION AUDIO (DÉSACTIVÉE) ============
def compress_audio(audio_file, bitrate='64k', format='mp3'):
    """
    Fonction factice - la compression audio n'est pas disponible.
    Retourne le fichier sans modification.
    """
    print(f"ℹ️ Audio non compressé automatiquement: {audio_file.name}")
    print(f"   Compressez-le manuellement avant upload (Audacity, Online Converter, etc.)")
    return audio_file


def compress_audio_high_quality(audio_file):
    """Fonction factice"""
    return compress_audio(audio_file)


def compress_audio_medium_quality(audio_file):
    """Fonction factice"""
    return compress_audio(audio_file)


def compress_audio_low_quality(audio_file):
    """Fonction factice"""
    return compress_audio(audio_file)
