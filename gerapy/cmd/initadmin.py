import django
import os

from gerapy import settings


def initadmin():
    """
    create super user
    :return:
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gerapy.server.server.settings")
    django.setup()
    from django.contrib.auth.models import User
    
    admins = User.objects.filter(is_superuser=True)
    if admins:
        print('Admin user already exists, you can use them to login:')
        for admin in admins:
            print('- %s(%s)' % (admin.username, admin.email))
    else:
        print('No Admin user exists, create temp admin user')
        for user in settings.ADMINS:
            username = user
            email = '%s@gerapy.com' % username
            password = username
            admin, created = User.objects.update_or_create(email=email, username=username)
            admin.set_password(password)
            admin.is_active = True
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
            print('%s admin account: %s(%s), initial password: %s, just use it temporarily '
                  'and change the password for safety' % \
                  ('Created' if created else 'Reset', username, email, password))
