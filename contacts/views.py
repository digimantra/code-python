from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from seo.seo import Seo
from .models import ContactsConfig, NotificationReceiver, ThankYouPage, DefaultMessage
from .forms import ContactForm, DefaultForm
from libs.email import send_template
from django.utils.translation import ugettext_lazy as _

from webpage.views import WebPageSingletonView
from .models import *
from django.template import loader


class IndexView(DetailView):
    model = ContactsConfig
    context_object_name = 'page'
    template_name = 'contacts/index.html'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get_context_data(self, **kwargs):
        seo = Seo()
        seo.set_data(self.object, defaults={
            'title': self.object.header,
        })
        seo.save(self.request)

        self.request.breadcrumbs.add(self.object.title)
        
        context = super().get_context_data(**kwargs)
        context.update({
            'is_contact': True,
            'form': DefaultForm(),
        })

        return context


class SubscribePageView(WebPageSingletonView):
    model = SubscribePage
    template_name = 'contacts/index.html'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get_context_data(self, **kwargs):
        self.get_seo().set_data(self.object, defaults={
            'title': self.object.title,
            'og_title': self.object.title,
        })
        self.get_seo().save(self.request)
        self.request.breadcrumbs.add(self.object.title)

        context = super().get_context_data(**kwargs)
        context.update({
            'config': self.model.get_solo(),
            'subscribe_page': True,
        })
        return context


class SubscribeEmailPageView(WebPageSingletonView):
    model = SampleSubscribePage
    template_name = 'contacts/index.html'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get_context_data(self, **kwargs):
        self.get_seo().set_data(self.object, defaults={
            'title': self.object.title,
            'og_title': self.object.title,
        })
        self.get_seo().save(self.request)
        self.request.breadcrumbs.add(self.object.title)

        context = super().get_context_data(**kwargs)
        context.update({
            'config': self.model.get_solo(),
            'sample_subscribe_page': True,
        })
        return context



class ThankYouView(DetailView):
    model = ThankYouPage
    context_object_name = 'page'
    template_name = 'contacts/thank_you.html'

    def get_object(self, queryset=None):
        return self.model.get_solo()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'address': ContactsConfig.get_solo(),
            'header': self.object.header,
            'text': self.object.text
        })
        return context




def contact_block_render(context, block, **kwargs):

    if 'is_contact' in context:
        is_contact = True
    else:
        is_contact = False


    return loader.render_to_string('contacts/block.html', {
        'block': block,
        'form': ContactForm(),
        'is_contact': is_contact,
        'address': ContactsConfig.get_solo(),
    }, request=context.get('request'))
