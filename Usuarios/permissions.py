from django.contrib.auth.models import Permission

permission = Permission.objects.create(
    codename='can_view_users_list',
    name='Can view users list'
)