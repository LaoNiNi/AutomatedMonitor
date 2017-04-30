#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/9 21:08"

import xadmin

from django import forms
from xadmin import views
from  monitor import models
# Register your models here.

# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email','name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = models.UserProfile
        fields = ('email','password','is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(object):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email','is_admin','is_active')
    list_filter = ('is_admin',)
    list_editable = ['is_admin']

    fieldsets = (
        (None, {'fields': ('email','name', 'password')}),
        ('Personal info', {'fields': ('phone','weixin','memo',)}),

        ('用户权限', {'fields': ('is_active','is_staff','is_admin','user_permissions','groups')}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2','is_active','is_admin')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('user_permissions','groups')






class HostAdmin(object):
    list_display =  ('id','name','ip_addr','status')
    filter_horizontal = ('host_groups','templates')


class HostGroupAdmin(object):
    style_fields = {'templates': 'm2m_transfer'}


class TemplateAdmin(object):
    filter_horizontal = ('services','triggers')
    style_fields = {'services':'m2m_transfer','triggers':'m2m_transfer'}

class ServiceAdmin(object):
    filter_horizontal = ('items',)
    list_display = ('name','interval','plugin_name')
    style_fields = {'items': 'm2m_transfer'}
    #list_select_related = ('items',)


class TriggerExpressionInline(object):
    model = models.TriggerExpression
    #exclude = ('memo',)
    #readonly_fields = ['create_date']


class TriggerAdmin(object):
    list_display = ('name','severity','enabled')
    inlines = [TriggerExpressionInline,]
    #filter_horizontal = ('expressions',)


class TriggerExpressionAdmin(object):
    list_display = ('trigger','service','service_index','specified_index_key','operator_type','data_calc_func','threshold','logic_type')


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "大倪的自动化监控系统"
    site_footer = "如有雷同，纯属巧合"
    menu_style = "accordion"


# class ServiceIndexAdmin(object):
#     style_fields = {'idc': 'm2m_transfer'}


xadmin.site.register(models.Host,HostAdmin)
xadmin.site.register(models.HostGroup,HostGroupAdmin)
xadmin.site.register(models.Template,TemplateAdmin)
xadmin.site.register(models.Service,ServiceAdmin)
xadmin.site.register(models.Trigger,TriggerAdmin)
xadmin.site.register(models.TriggerExpression,TriggerExpressionAdmin)
xadmin.site.register(models.ServiceIndex)
xadmin.site.register(models.Action)
xadmin.site.register(models.ActionOperation)
#admin.site.register(models.ActionCondtion,ActionConditionAdmin)
xadmin.site.register(models.Maintenance)
xadmin.site.register(models.UserProfile,UserProfileAdmin)
xadmin.site.register(models.EventLog)

xadmin.site.register(views.BaseAdminView,BaseSettings)
xadmin.site.register(views.CommAdminView,GlobalSettings)