# create_admin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jeunesse_eglise.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    """Crée un superutilisateur avec TOUS les droits pour gérer le site"""
    
    # Configuration
    USERNAME = 'admin'
    EMAIL = 'admin@exemple.com'
    PASSWORD = 'Admin123!'
    
    print("=" * 60)
    print("👑 ADMINISTRATEUR - CITE BETHEL BANDAL MOULEART")
    print("=" * 60)
    print("Cet administrateur pourra :")
    print("  ✅ Gérer les événements (ajout, modification, suppression)")
    print("  ✅ Gérer la galerie (photos et vidéos)")
    print("  ✅ Gérer le blog (articles)")
    print("  ✅ Gérer les enseignements audio/vidéo/PDF")
    print("  ✅ Gérer les abonnés WhatsApp")
    print("  ✅ Gérer les membres")
    print("  ✅ Accéder à l'interface d'administration Django")
    print("=" * 60)
    
    try:
        user, created = User.objects.get_or_create(
            username=USERNAME,
            defaults={
                'email': EMAIL,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        if not created:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.email = EMAIL
        
        user.set_password(PASSWORD)
        user.save()
        
        print(f"\n✅ Administrateur {'créé' if created else 'mis à jour'} avec succès !")
        print("-" * 40)
        print(f"📧 Identifiant: {USERNAME}")
        print(f"🔒 Mot de passe: {PASSWORD}")
        print("-" * 40)
        print(f"👑 Superuser (is_superuser): {user.is_superuser}")
        print(f"⭐ Staff (is_staff): {user.is_staff}")
        print(f"✅ Actif (is_active): {user.is_active}")
        print("-" * 40)
        
        print("\n📋 ÉTAT DES CONDITIONS DANS VOS TEMPLATES :")
        print("   {% if user.is_superuser %}  → ✅ VRAI (boutons admin visibles)")
        print("   {% if user.is_staff %}      → ✅ VRAI")
        print("   {% if user.is_authenticated %} → ✅ VRAI (après connexion)")
        
        print("\n🌐 LIENS D'ADMINISTRATION :")
        print(f"   - Interface Django: /admin/")
        print(f"   - Événements: /admin/events/event/")
        print(f"   - Galerie: /admin/gallery/galleryimage/")
        print(f"   - Blog: /admin/blog/blogpost/")
        print(f"   - Enseignements: /admin/teachings/teaching/")
        
        print("\n" + "=" * 60)
        print("🎉 ADMINISTRATEUR PRÊT À UTILISER !")
        print("=" * 60)
        print("💡 Changez votre mot de passe après la première connexion")
        
        return user
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return None

if __name__ == '__main__':
    print("\n🚀 DÉPLOIEMENT DE L'ADMINISTRATEUR\n")
    create_admin()
    print("\n✨ Configuration terminée !")