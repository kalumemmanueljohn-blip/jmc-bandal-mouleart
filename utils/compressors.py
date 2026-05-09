# utils/compressors.py
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
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


# ============ COMPRESSION VIDEOS ============
def compress_video(video_file, max_width=854, bitrate='800k', fps=24):
    """
    Compresse une vidéo
    - max_width: largeur maximale en pixels
    - bitrate: débit binaire (ex: '800k', '1M')
    - fps: images par seconde
    """
    temp_input = None
    temp_output = None
    
    try:
        # Créer fichier temporaire d'entrée
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as f:
            for chunk in video_file.chunks():
                f.write(chunk)
            temp_input = f.name
        
        # Charger la vidéo
        clip = VideoFileClip(temp_input)
        
        # Réduire la résolution si trop large
        if clip.w > max_width:
            clip = clip.resize(width=max_width)
        
        # Réduire les FPS si trop élevé
        if clip.fps > fps:
            clip = clip.set_fps(fps)
        
        # Créer fichier temporaire de sortie
        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
        
        # Exporter la vidéo compressée
        clip.write_videofile(
            temp_output,
            codec='libx264',
            audio_codec='aac',
            bitrate=bitrate,
            audio_bitrate='128k',
            preset='fast'
        )
        
        clip.close()
        
        # Lire le fichier compressé
        with open(temp_output, 'rb') as f:
            compressed_content = f.read()
        
        # Nettoyer
        if temp_input and os.path.exists(temp_input):
            os.unlink(temp_input)
        if temp_output and os.path.exists(temp_output):
            os.unlink(temp_output)
        
        return ContentFile(compressed_content, name=video_file.name)
    
    except Exception as e:
        print(f"Erreur compression vidéo: {e}")
        # Nettoyage en cas d'erreur
        if temp_input and os.path.exists(temp_input):
            os.unlink(temp_input)
        if temp_output and os.path.exists(temp_output):
            os.unlink(temp_output)
        return video_file


def compress_video_high_quality(video_file):
    """Compression haute qualité"""
    return compress_video(video_file, max_width=1280, bitrate='1500k', fps=30)


def compress_video_medium_quality(video_file):
    """Compression qualité moyenne"""
    return compress_video(video_file, max_width=854, bitrate='800k', fps=24)


def compress_video_low_quality(video_file):
    """Compression basse qualité (petit fichier)"""
    return compress_video(video_file, max_width=640, bitrate='400k', fps=20)


# ============ COMPRESSION AUDIO ============
def compress_audio(audio_file, bitrate='64k', format='mp3'):
    """
    Compresse un fichier audio
    - bitrate: débit binaire (ex: '64k', '96k', '128k')
    - format: format de sortie ('mp3', 'ogg')
    """
    temp_input = None
    temp_output = None
    
    try:
        # Créer fichier temporaire d'entrée
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
            temp_input = f.name
        
        # Charger l'audio
        audio = AudioSegment.from_mp3(temp_input)
        
        # Réduire le bitrate (compression)
        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format}').name
        
        # Exporter l'audio compressé
        audio.export(
            temp_output,
            format=format,
            bitrate=bitrate
        )
        
        # Lire le fichier compressé
        with open(temp_output, 'rb') as f:
            compressed_content = f.read()
        
        # Nettoyer
        if temp_input and os.path.exists(temp_input):
            os.unlink(temp_input)
        if temp_output and os.path.exists(temp_output):
            os.unlink(temp_output)
        
        return ContentFile(compressed_content, name=audio_file.name)
    
    except Exception as e:
        print(f"Erreur compression audio: {e}")
        # Nettoyage en cas d'erreur
        if temp_input and os.path.exists(temp_input):
            os.unlink(temp_input)
        if temp_output and os.path.exists(temp_output):
            os.unlink(temp_output)
        return audio_file


def compress_audio_high_quality(audio_file):
    """Compression audio haute qualité"""
    return compress_audio(audio_file, bitrate='128k')


def compress_audio_medium_quality(audio_file):
    """Compression audio qualité moyenne"""
    return compress_audio(audio_file, bitrate='96k')


def compress_audio_low_quality(audio_file):
    """Compression audio basse qualité (petit fichier)"""
    return compress_audio(audio_file, bitrate='48k')