# build.sh
#!/bin/bash

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Migrations
python manage.py migrate

# Créer l'admin
python manage.py shell << EOF
from django.contrib.auth.models import User
User.objects.filter(username='admin', is_superuser=False).delete()
user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@exemple.com',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True
    }
)
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.set_password('Admin123!')
user.save()
print('='*50)
print('✅ Admin OK - superuser:', user.is_superuser)
print('='*50)
EOF
