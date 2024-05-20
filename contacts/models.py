from django.db import models
from django.utils.timezone import now
from django.utils.dates import WEEKDAYS
from django.shortcuts import resolve_url
from django.utils.formats import time_format
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from libs.multiselect_field.fields import MultiSelectField
from attachable_blocks.models import AttachableBlock
from google_maps.fields import GoogleCoordsField
from webpage.models import WebPageSingleton
from .conf import *
from multiselectfield import MultiSelectField

class ContactsConfig(WebPageSingleton):
    address = models.CharField(_('address'), max_length=255)
    city = models.CharField(_('city'), max_length=255)
    email = models.EmailField(_('e-mail'))
    region = models.CharField(_('region'), max_length=64, blank=True)
    number = models.CharField(_('number'), max_length=255, blank=True)
    zip = models.CharField(_('zip'), max_length=32, blank=True)
    coords = GoogleCoordsField(_('coords'), blank=True)
    form_block_header = models.CharField(_('form block header'), blank=True, max_length=256)
    form_block_description = models.TextField(_('form block description'), blank=True)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('contacts:index')


class SubscribePage(WebPageSingleton):
    class Meta:
        verbose_name = _('Subscribe for Smart Strategies')

    def get_absolute_url(self):
        return resolve_url('contacts:subscribe_for_smart_strategies')


class SampleSubscribePage(WebPageSingleton):
    class Meta:
        verbose_name = _('Subscribe')

    def get_absolute_url(self):
        return resolve_url('contacts:subscribe')


class ThankYouPage(SingletonModel):
    header = models.CharField(_('header'), max_length=255)
    text = models.TextField(_('text'), blank=True)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('Thank You page')

    def get_absolute_url(self):
        return resolve_url('contacts:thank_you')


class NotificationReceiver(models.Model):
    config = models.ForeignKey(ContactsConfig, related_name='receivers')
    email = models.EmailField(_('e-mail'))

    class Meta:
        verbose_name = _('notification receiver')
        verbose_name_plural = _('notification receivers')

    def __str__(self):
        return self.email


class Message(models.Model):
    # Date / Time
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    spouse_date_birth = models.DateField(_('spouse date birth'), blank=True, null=True)
    date = models.DateTimeField(_('date sent'), default=now, editable=False)
    spouse_name = models.CharField(_('spouse_name'), blank=True, max_length=255)
    spouse_retirement = models.CharField(_('spouse_retirement'), choices=RETIREMENT, default=RETIREMENT[0][0],
                                         max_length=255,blank=True,null=True)
    retirement = models.CharField(_('retirement'), choices=RETIREMENT, default=RETIREMENT[0][0], max_length=255)
    stock_options = models.CharField(_('stock_options'), choices=YES_NO, default=YES_NO[0][0], max_length=255)
    professional_guidance = models.CharField(_('professional_guidance'), blank=True, max_length=1024)
    read_fee_structure = models.CharField(_('read_fee_structure'), choices=YES_NO, default=YES_NO[0][0], max_length=255)

    # another
    name = models.CharField(_('Full name*'), max_length=128)
    phone = models.CharField(_('phone'), max_length=32, blank=True)
    email = models.EmailField(_('e-mail'), blank=True)
    message = models.TextField(_('message'), max_length=2048)
    marital_status = models.CharField(_('marital status'), choices=MARITAL_STATUS, default=MARITAL_STATUS[0][0],
                                      max_length=255)
    occupation = models.CharField(_('occupation*'), blank=True, max_length=255)
    spouse_occupation = models.CharField(_('spouse_occupation*'), blank=True,null=True, max_length=255)
    bussines_owner = models.CharField(_('business owner'), choices=YES_NO, default=YES_NO[0][0], max_length=255)
    household_income = models.CharField(_('household income'), choices=HOUSEHOLD_INCOME, default=HOUSEHOLD_INCOME[0][0],
                                        max_length=255)
    investeble_assets = models.CharField(_('investable assets'), choices=HOUSEHOLD_INCOME,
                                         default=HOUSEHOLD_INCOME[0][0], max_length=255)
    real_estate_question = models.CharField(_('real estate question'), choices=YES_NO, default=YES_NO[0][0],
                                            max_length=255)
    number_of_children = models.CharField(_('number of children*'), choices=NUMBER_CHILDREN,
                                          default=NUMBER_CHILDREN[0][0], max_length=255)
    social_media = models.CharField(_('social media question*'), choices=SOCIAL_MEDIA,
                                    default=SOCIAL_MEDIA[0][0], max_length=255)
    additional_information = models.CharField(_('additional information*'), max_length=1024, blank=True)
    referer = models.CharField(_('from page'), max_length=512, blank=True, editable=False)
    how_did_you_hear_about_us = MultiSelectField(choices=HOW_DID_YOU_HEAR_ABOUT_US, default='', max_length=1024)
    basic_goals1 = MultiSelectField(choices=BASIC_GOALS, default='', max_length=1024)
    agree = models.BooleanField(choices=AGREE,default=False)

    class Meta:
        default_permissions = ('delete',)
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ('-date',)

    def __str__(self):
        return self.name

class DefaultMessage(models.Model):
    name = models.CharField(_('Full name*'), max_length=128)
    phone = models.CharField(_('phone'), max_length=32, blank=True)
    email = models.EmailField(_('e-mail'), blank=True)
    message = models.TextField(_('message'), max_length=2048)
    additional_information = models.CharField(_('additional information'), max_length=1024, blank=True)
    referer = models.CharField(_('from page'), max_length=512, blank=True, editable=False)
    date = models.DateTimeField(_('date sent'), default=now, editable=False)

    class Meta:
        default_permissions = ('delete',)
        verbose_name = _('Defaul message')
        verbose_name_plural = _('Default messages')
        ordering = ('-date',)

    def __str__(self):
        return self.name


class ContactBlock(AttachableBlock):
    BLOCK_VIEW = 'contacts.views.contact_block_render'

    header = models.CharField(_('header'), max_length=128, blank=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        default_permissions = ()
        verbose_name = _('Contact block')
        verbose_name_plural = _('Contact blocks')