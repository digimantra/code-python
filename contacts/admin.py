from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils import dateformat
from django.utils.timezone import localtime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from suit.admin import SortableModelAdmin, SortableTabularInline
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from attachable_blocks.admin import AttachableBlockAdmin, AttachedBlocksStackedInline
from seo.admin import SeoModelAdminMixin
from libs.description import description
from webpage.admin import WebPageSingletonAdmin
from .models import ContactsConfig, NotificationReceiver, ContactBlock, Message, DefaultMessage, SubscribePage, SampleSubscribePage


class ContactsConfigBlocksInline(AttachedBlocksStackedInline):
    suit_classes = 'suit-tab suit-tab-blocks'


class NotificationReceiverAdmin(ModelAdminInlineMixin, admin.TabularInline):
    model = NotificationReceiver
    extra = 0
    suit_classes = 'suit-tab suit-tab-notify'


@admin.register(ContactsConfig)
class ContactsConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    fieldsets = WebPageSingletonAdmin.fieldsets + (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                
            ),
        }),
        ('Address', {
            'classes': ('suit-tab', 'suit-tab-address'),
            'fields': (
                'address', 'city', 'email', 'region', 'zip', 'coords', 'number',
            ),
        }),
        ('Form Block', {
            'classes': ('suit-tab', 'suit-tab-form'),
            'fields': (
                'form_block_header', 'form_block_description',
            ),
        }),
    )
    inlines = (NotificationReceiverAdmin, ContactsConfigBlocksInline)
    suit_form_tabs = (
        ('general', _('General')),
        ('form', _('Form')),
        ('notify', _('Notifications')),
        ('address', _('Address')),
        ('blocks', _('Blocks')),
    )

    class Media:
        js = (
            'contacts/admin/js/coords.js',
        )



@admin.register(Message)
class MessageAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'name', 'phone', 'date_of_birth','spouse_name','spouse_date_birth', 'email',
            ),
        }),
        (_('Text'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'marital_status', 'spouse_date_birth','spouse_name','spouse_retirement','occupation','spouse_occupation','retirement', 'stock_options','professional_guidance','read_fee_structure','bussines_owner',
                'household_income', 'investeble_assets', 'real_estate_question', 'number_of_children',
                'basic_goals1', 'additional_information', 'how_did_you_hear_about_us','social_media',
            ),
        }),
        (_('Info'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'date_fmt', 'referer',
            ),
        }),
    )
    readonly_fields = ('name', 'phone', 'date_of_birth', 'how_did_you_hear_about_us', 'spouse_date_birth','spouse_name','spouse_occupation','spouse_retirement','occupation','retirement', 'stock_options','professional_guidance','read_fee_structure', 'email', 'marital_status', 'occupation','bussines_owner','retirement',
                'household_income','retirement','investeble_assets', 'real_estate_question', 'number_of_children',
                'additional_information', 'date_fmt', 'referer','basic_goals1','social_media')
    list_display = ('name', 'message_fmt', 'date_fmt')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True



    def message_fmt(self, obj):
        return description(obj.additional_information, 60, 80)
    message_fmt.short_description = _('Message')
    message_fmt.admin_order_field = 'additional_information'

    def date_fmt(self, obj):
        return dateformat.format(localtime(obj.date), settings.DATETIME_FORMAT)
    date_fmt.short_description = _('Date')
    date_fmt.admin_order_field = 'date'


@admin.register(DefaultMessage)
class DefaultMessageAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'name', 'phone', 'email',
            ),
        }),
        (_('Text'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'message', 'additional_information',
            ),
        }),
        (_('Info'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'date_fmt', 'referer',
            ),
        }),
    )
    readonly_fields = ('name', 'phone', 'email', 'message', 'date_fmt', 'additional_information', 'referer')
    list_display = ('name', 'message_fmt', 'date_fmt')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def message_fmt(self, obj):
        return description(obj.message, 60, 80)
    message_fmt.short_description = _('Message')
    message_fmt.admin_order_field = 'message'

    def date_fmt(self, obj):
        return dateformat.format(localtime(obj.date), settings.DATETIME_FORMAT)
    date_fmt.short_description = _('Date')
    date_fmt.admin_order_field = 'date'


@admin.register(ContactBlock)
class ContactBlockAdmin(AttachableBlockAdmin):
    fieldsets = AttachableBlockAdmin.fieldsets + (
        (_('Customization'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header', 'description',
            ),
        }),
    )
@admin.register(SubscribePage)
class SubscribePageConfigAdmin(WebPageSingletonAdmin):
    pass

@admin.register(SampleSubscribePage)
class SubscribePageConfigAdmin(WebPageSingletonAdmin):
    pass