from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )

    empty_value_display = 'значение отсутствует'
    list_editable = ('role',)
    list_filter = ('username',)
    search_fields = ('username', 'role')


admin.site.register(User)
