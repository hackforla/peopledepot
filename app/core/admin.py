from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', )}
        ),
        (_('Important_dates'), {'fields': ('created_at', 'updated_at', )}),
    )
    readonly_fields = ('created_at', 'updated_at')
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'email', 'password', 'password2', ),
        }),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('username', 'is_staff', 'is_active')
