from ajax_views.decorators import ajax_view
from django.http import JsonResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import resolve_url
from django.template import loader
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from libs.email import send_template

from .forms import ContactForm, DefaultForm
from .models import ContactsConfig, NotificationReceiver


@ajax_view('contacts.form_ajax')
class ContactPopup(FormView):
    form_class = ContactForm
    template_name = 'contacts/popups/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'config': ContactsConfig.get_solo(),
            'csrf_token': get_token(self.request),
        })
        return context

    def form_valid(self, form):
        captcha_response = form.cleaned_data['captcha']
        if captcha_response:
            message = form.save(commit=False)
            referer = self.request.POST.get('referer')
            message.save()
            message.referer = escape(referer)

            receivers = NotificationReceiver.objects.all().values_list('email', flat=True)
            send_template(self.request, receivers,
                          subject=_('Message from {domain}'),
                          template='contacts/mails/full_message.html',
                          context={
                              'message': message,
                          }
                          )

            return JsonResponse({
                'url': resolve_url('contacts:thank_you'),
                'message': loader.render_to_string(
                    'contacts/popups/success.html',
                    self.get_context_data(),
                    request=self.request
                )
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': 'Error verifying reCAPTCHA, please try again.'
            })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.error_dict_full
        })


@ajax_view('contacts.default_form_ajax')
class ContactDefaultForm(FormView):
    form_class = DefaultForm

    def get(self, request, *args, **kwargs):
        raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'config': ContactsConfig.get_solo(),
            'csrf_token': get_token(self.request),
        })
        return context

    def form_valid(self, form):
        captcha_response = form.cleaned_data['captcha']
        if captcha_response:
            message = form.save(commit=False)
            referer = self.request.POST.get('referer')
            message.referer = escape(referer)
            message.save()

            receivers = NotificationReceiver.objects.all().values_list('email', flat=True)
            send_template(self.request, receivers,
                          subject=_('Message from {domain}'),
                          template='contacts/mails/message.html',
                          context={
                              'message': message,
                          }
                          )

            return JsonResponse({
                'url': resolve_url('contacts:thank_you'),
                'message': loader.render_to_string(
                    'contacts/popups/success.html',
                    self.get_context_data(),
                    request=self.request
                )
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': 'Error verifying reCAPTCHA, please try again.'
            })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.error_dict_full
        })
