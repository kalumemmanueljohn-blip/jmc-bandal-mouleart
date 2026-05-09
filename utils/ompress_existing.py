# compress_existing.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jeunesse_eglise.settings')
django.setup()

from events.models import Event
from gallery.models import GalleryImage, GalleryVideo
from blog.models import BlogPost
from teachings.models import Teaching  # ← AJOUTÉ

def compress_all():
    print("=" * 50)
    print("🚀 COMPRESSION DE TOUS LES FICHIERS EXISTANTS")
    print("=" * 50)
    
    # 1. Images des événements
    print("\n📅 1. Compression des images d'événements...")
    event_count = 0
    for event in Event.objects.filter(image__isnull=False):
        try:
            old_size = event.image.size
            if old_size > 500 * 1024:  # > 500KB
                event.save()
                new_size = event.image.size
                print(f"   ✅ {event.title}: {old_size//1024}KB → {new_size//1024}KB (gagné { (old_size - new_size)//1024 }KB)")
                event_count += 1
            else:
                print(f"   ⏭️ {event.title}: déjà optimisée ({old_size//1024}KB)")
        except Exception as e:
            print(f"   ❌ Erreur {event.title}: {e}")
    
    # 2. Images de la galerie
    print("\n🖼️ 2. Compression des images de la galerie...")
    img_count = 0
    for img in GalleryImage.objects.all():
        try:
            old_size = img.image.size
            if old_size > 500 * 1024:  # > 500KB
                img.save()
                new_size = img.image.size
                print(f"   ✅ {img.title}: {old_size//1024}KB → {new_size//1024}KB")
                img_count += 1
            else:
                print(f"   ⏭️ {img.title}: déjà optimisée ({old_size//1024}KB)")
        except Exception as e:
            print(f"   ❌ Erreur {img.title}: {e}")
    
    # 3. Vidéos de la galerie
    print("\n🎬 3. Compression des vidéos de la galerie...")
    video_count = 0
    for video in GalleryVideo.objects.filter(video_file__isnull=False):
        try:
            old_size = video.video_file.size
            if old_size > 10 * 1024 * 1024:  # > 10MB
                video.save()
                new_size = video.video_file.size
                print(f"   ✅ {video.title}: {old_size//1024//1024}MB → {new_size//1024//1024}MB")
                video_count += 1
            else:
                print(f"   ⏭️ {video.title}: déjà optimisée ({old_size//1024//1024}MB)")
        except Exception as e:
            print(f"   ❌ Erreur {video.title}: {e}")
    
    # 4. Images du blog
    print("\n📝 4. Compression des images du blog...")
    blog_count = 0
    for post in BlogPost.objects.filter(featured_image__isnull=False):
        try:
            old_size = post.featured_image.size
            if old_size > 300 * 1024:  # > 300KB
                post.save()
                new_size = post.featured_image.size
                print(f"   ✅ {post.title}: {old_size//1024}KB → {new_size//1024}KB")
                blog_count += 1
            else:
                print(f"   ⏭️ {post.title}: déjà optimisée ({old_size//1024}KB)")
        except Exception as e:
            print(f"   ❌ Erreur {post.title}: {e}")
    
    # 5. Audios et vidéos des enseignements
    print("\n🎧 5. Compression des fichiers d'enseignements...")
    teaching_count = 0
    for teaching in Teaching.objects.filter(file__isnull=False):
        try:
            old_size = teaching.file.size
            
            # Audio
            if teaching.content_type == 'audio' and old_size > 5 * 1024 * 1024:  # > 5MB
                teaching.save()
                new_size = teaching.file.size
                print(f"   ✅ AUDIO {teaching.title}: {old_size//1024//1024}MB → {new_size//1024//1024}MB")
                teaching_count += 1
            # Vidéo
            elif teaching.content_type == 'video' and old_size > 10 * 1024 * 1024:  # > 10MB
                teaching.save()
                new_size = teaching.file.size
                print(f"   ✅ VIDEO {teaching.title}: {old_size//1024//1024}MB → {new_size//1024//1024}MB")
                teaching_count += 1
            # PDF ou déjà petit
            else:
                if teaching.content_type == 'audio':
                    print(f"   ⏭️ {teaching.title}: audio déjà optimisé ({old_size//1024//1024}MB)")
                elif teaching.content_type == 'video':
                    print(f"   ⏭️ {teaching.title}: vidéo déjà optimisée ({old_size//1024//1024}MB)")
                else:
                    print(f"   ⏭️ {teaching.title}: {teaching.content_type} non compressé ({old_size//1024}KB)")
        except Exception as e:
            print(f"   ❌ Erreur {teaching.title}: {e}")
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE LA COMPRESSION")
    print("=" * 50)
    print(f"   🖼️ Événements compressés: {event_count}")
    print(f"   🖼️ Galerie compressées: {img_count}")
    print(f"   🎬 Vidéos compressées: {video_count}")
    print(f"   📝 Blog compressés: {blog_count}")
    print(f"   🎧 Enseignements compressés: {teaching_count}")
    print("=" * 50)
    print("\n✅ Compression terminée!")

def compress_by_type(choice):
    """Compresse un type spécifique"""
    if choice == 'events':
        print("Compression des événements...")
        for event in Event.objects.filter(image__isnull=False):
            if event.image.size > 500 * 1024:
                event.save()
                print(f"   ✅ {event.title}")
    
    elif choice == 'gallery':
        print("Compression de la galerie...")
        for img in GalleryImage.objects.all():
            if img.image.size > 500 * 1024:
                img.save()
                print(f"   ✅ {img.title}")
        for video in GalleryVideo.objects.filter(video_file__isnull=False):
            if video.video_file.size > 10 * 1024 * 1024:
                video.save()
                print(f"   ✅ {video.title}")
    
    elif choice == 'blog':
        print("Compression du blog...")
        for post in BlogPost.objects.filter(featured_image__isnull=False):
            if post.featured_image.size > 300 * 1024:
                post.save()
                print(f"   ✅ {post.title}")
    
    elif choice == 'teachings':
        print("Compression des enseignements...")
        for teaching in Teaching.objects.filter(file__isnull=False):
            if teaching.content_type == 'audio' and teaching.file.size > 5 * 1024 * 1024:
                teaching.save()
                print(f"   ✅ AUDIO {teaching.title}")
            elif teaching.content_type == 'video' and teaching.file.size > 10 * 1024 * 1024:
                teaching.save()
                print(f"   ✅ VIDEO {teaching.title}")
    
    else:
        print("Choix invalide. Options: events, gallery, blog, teachings")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Compression par type
        compress_by_type(sys.argv[1])
    else:
        # Compression de tout
        compress_all()