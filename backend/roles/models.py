from django.db import models
from django.apps import apps


class Role(models.Model):
    """Role model to represent different user roles in the system"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    # Using a ManyToManyField to Django's built-in Permission model for flexibility
    permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='roles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'roles_role'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    def __str__(self):
        return self.name

    def __bool__(self):
        return self.is_active

    def get_permissions_codenames(self):
        """Return a list of permission codenames for this role"""
        return list(self.permissions.values_list('codename', flat=True))

    def has_permission(self, codename):
        """Check if role has a specific permission"""
        return self.permissions.filter(codename=codename).exists()

    def add_permission(self, permission_codename):
        """Add a permission to the role by codename"""
        Permission = apps.get_model('auth', 'Permission')
        try:
            permission = Permission.objects.get(codename=permission_codename)
            self.permissions.add(permission)
            return True
        except Permission.DoesNotExist:
            return False

    def remove_permission(self, permission_codename):
        """Remove a permission from the role by codename"""
        Permission = apps.get_model('auth', 'Permission')
        try:
            permission = Permission.objects.get(codename=permission_codename)
            self.permissions.remove(permission)
            return True
        except Permission.DoesNotExist:
            return False