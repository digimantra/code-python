from django import forms
from django.utils.translation import ugettext_lazy as _
from libs.form_helper.forms import FormHelperMixin
from libs.widgets import PhoneWidget
from .models import Message, DefaultMessage
from contacts import conf
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

class ContactForm(FormHelperMixin, forms.ModelForm):
    DATE_INPUT_FORMATS = ['%m/%d/%Y']
    default_field_template = 'form_helper/field.html'
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(
            attrs={
                'required_score': 0.85,
            }
        ))
    field_templates = {
        # 'time': 'form_helper/choice_field.html',
        'marital_status': 'form_helper/choice_field_2.html',
        'bussines_owner': 'form_helper/choice_field_2.html',
        'household_income': 'form_helper/field.html',
        'investeble_assets': 'form_helper/field.html',
        'additional_information': 'form_helper/unlabeled_field.html',
        'occupation': 'form_helper/unlabeled_field.html',
        'spouse_occupation': 'form_helper/unlabeled_field.html',
        'real_estate_question': 'form_helper/choice_field_2.html',
        'number_of_children': 'form_helper/field.html',
        'social_media': 'form_helper/field.html',

        'spouse_retirement': 'form_helper/field.html',
        'retirement': 'form_helper/field.html',
        'stock_options': 'form_helper/choice_field_2.html',
        'professional_guidance': 'form_helper/unlabeled_field.html',
        'read_fee_structure': 'form_helper/choice_field_2.html',
        'how_did_you_hear_about_us': 'form_helper/multiple_choice_field.html',
        'basic_goals1': 'form_helper/multiple_choice_field.html',
        'agree': 'form_helper/multiple_choice_field.html',

    }


    marital_status = forms.ChoiceField(
        initial=conf.MARITAL_STATUS[0][0],
        choices=conf.MARITAL_STATUS,
        widget=forms.RadioSelect,
    ),
    bussines_owner = forms.ChoiceField(
        initial=conf.YES_NO[0][0],
        choices=conf.YES_NO,
        widget=forms.RadioSelect,
    ),
    household_income = forms.ChoiceField(

        initial=conf.HOUSEHOLD_INCOME[0][0],
        choices=conf.HOUSEHOLD_INCOME,
        widget=forms.RadioSelect,
    ),
    investeble_assets = forms.ChoiceField(
        label='Investeble assets*',
        initial=conf.HOUSEHOLD_INCOME[0][0],
        choices=conf.HOUSEHOLD_INCOME,
        widget=forms.RadioSelect,
    ),
    real_estate_question = forms.ChoiceField(
        initial=conf.YES_NO[0][0],
        choices=conf.YES_NO,
        widget=forms.RadioSelect,
    ),

    number_of_children = forms.ChoiceField(
        initial=conf.NUMBER_CHILDREN[0][0],
        choices=conf.NUMBER_CHILDREN,
        widget=forms.RadioSelect,
    ),
    spouse_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form__input ',
        }),
    )

    date_of_birth = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        label='Date of birth*',
        widget=forms.DateInput(attrs={
            'class': 'form__input form__input_date--birth',
            'placeholder': 'mm/dd/yyyy',
        }),
    )
    spouse_date_birth = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        required=False,
        label='',
        widget=forms.DateInput(attrs={
            'class': 'form__input form__input_date--birth',
            'placeholder': 'mm/dd/yyyy'
        }),
    )

    phone = forms.CharField(
        required=True,
        label='Phone*',
        widget=PhoneWidget(attrs={
            'class': 'form__input form__input_phone',
            'type': 'tel',
            'placeholder': 'Phone*',
        }),
    )
    email = forms.CharField(
        required=True,
        label='Email*',
        widget=forms.EmailInput(attrs={
            'class': 'form__input',
            'type': 'email',
            'placeholder': 'Email*',
        }),
    )

    spouse_retirement = forms.ChoiceField(
        label='',
        required=False,
        initial=conf.RETIREMENT[0][0],
        choices=conf.RETIREMENT,
        widget=forms.RadioSelect
    ),
    retirement = forms.ChoiceField(

        label='',
        initial=conf.RETIREMENT[0][0],
        choices=conf.RETIREMENT,
        widget=forms.RadioSelect
    ),
    social_media = forms.ChoiceField(
        label='',
        initial=conf.SOCIAL_MEDIA[0][0],
        choices=conf.SOCIAL_MEDIA,
        widget=forms.RadioSelect,
    ),
    read_fee_structure = forms.ChoiceField(
        initial=conf.YES_NO[0][0],
        choices=conf.YES_NO,
        widget=forms.RadioSelect,
    ),

    basic_goals1 = forms.MultipleChoiceField(
        choices=conf.BASIC_GOALS,
        widget=forms.CheckboxSelectMultiple,
    ),

    how_did_you_hear_about_us = forms.MultipleChoiceField(
        choices=conf.HOW_DID_YOU_HEAR_ABOUT_US,
        widget=forms.CheckboxSelectMultiple,
    ),

    agree = forms.MultipleChoiceField(
        required=True,
        choices=conf.AGREE,
        widget=forms.CheckboxSelectMultiple,
        help_text='Please Check to submit the form',
    ),

    class Meta:
        model = Message
        fields = ('date_of_birth', 'spouse_date_birth', 'name','social_media',
                  'phone', 'email', 'marital_status', 'occupation', 'bussines_owner',
                  'household_income', 'investeble_assets', 'real_estate_question', 'number_of_children',
                  'additional_information', 'how_did_you_hear_about_us', 'spouse_name', 'spouse_retirement',
                  'retirement', 'stock_options', 'professional_guidance', 'read_fee_structure', 'basic_goals1', 'agree',
                  'spouse_occupation')
        widgets = {
            'bussines_owner': forms.RadioSelect(
                choices=conf.YES_NO,
            ),
            'real_estate_question': forms.RadioSelect(
                choices=conf.YES_NO,
            ),
            'number_of_children': forms.Select(
                choices=conf.NUMBER_CHILDREN,
                attrs={
                    'class': 'form__input form__select',
                    'placeholder': 'Number Of Children*',
                },
            ),
            'marital_status': forms.RadioSelect(
                choices=conf.MARITAL_STATUS,
            ),
            'household_income': forms.Select(
                choices=conf.HOUSEHOLD_INCOME,
                attrs={
                    'class': 'form__input form__select',
                    'placeholder': 'Household Income*',
                },
            ),
            'investeble_assets': forms.Select(
                choices=conf.HOUSEHOLD_INCOME,
                attrs={
                    'class': 'form__input form__select',
                    'placeholder': 'Investable Assets*',
                },
            ),

            'additional_information': forms.Textarea(attrs={
                'class': 'form__textarea',
                'rows': 1,

            }),
            'occupation': forms.Textarea(attrs={
                'class': 'form__textarea',
                'rows': 1,
            }),
            'spouse_occupation': forms.Textarea(attrs={
                'class': 'form__textarea',
                'rows': 1,
            }),

            'name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': 'Full name*',
            }),

            'spouse_retirement': forms.Select(
                choices=conf.RETIREMENT,
                attrs={
                    'class': 'form__input form__select',
                },
            ),

            'retirement': forms.Select(
                choices=conf.RETIREMENT,
                attrs={
                    'class': 'form__input form__select',
                },
            ),
            'social_media': forms.Select(
                choices=conf.SOCIAL_MEDIA,
                attrs={
                    'class': 'form__input form__select',
                },
            ),
            'stock_options': forms.RadioSelect(
                choices=conf.YES_NO,
            ),
            'professional_guidance': forms.Textarea(attrs={
                'class': 'form__textarea',
                'rows': 1,
            }),
            'read_fee_structure': forms.RadioSelect(
                choices=conf.YES_NO,
            ),

        }
        error_messages = {
            'name': {
                'required': _('Please enter your name'),
                'max_length': _('Name should not be longer than %(limit_value)d characters'),
            },
            'phone': {
                'required': _('Please enter your e-mail or phone so we can contact you'),
                'max_length': _('Phone number should not be longer than %(limit_value)d characters'),
            },
            'email': {
                'required': _('Please enter your e-mail or phone so we can contact you'),
                'max_length': _('E-mail should not be longer than %(limit_value)d characters'),
            },
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['investeble_assets'].label = "Investable Assets*"
        self.fields['household_income'].label = "Household Income*"
        self.fields['retirement'].label = ""
        self.fields['spouse_retirement'].label = ""
        self.fields['social_media'].label = ""
        self.fields['spouse_name'].label = ""
        self.fields['captcha'].label = ""

    def clean(self):
        """ Требуем указать email ИЛИ телефон """
        if 'phone' in self.cleaned_data and 'email' in self.cleaned_data:
            phone = self.cleaned_data.get('phone')
            email = self.cleaned_data.get('email')

            if not phone and not email:
                self.add_field_error('phone', 'required')
                self.add_field_error('email', 'required')

        return super().clean()


class DefaultForm(FormHelperMixin, forms.ModelForm):
    default_field_template = 'form_helper/field.html'
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(
            attrs={
                'required_score': 0.85,
            }
        ))
    name = forms.CharField(
        required=True,
        label='Full Name*',
        widget=forms.TextInput(attrs={
            'class': 'form__input',
            'placeholder': 'Full Name*'
        }),
    )
    email = forms.CharField(
        required=True,
        label='Email*',
        widget=
        forms.EmailInput(attrs={
            'class': 'form__input',
            'type': 'email',
            'placeholder': 'Email*',
        }),
    )
    message = forms.CharField(
        required=True,
        label='Message*',
        widget=forms.Textarea(attrs={
            'rows': 1,
            # 'wrap': "off",
            'class': 'form__input',
            'placeholder': 'Message*',
        }),
    )

    class Meta:
        model = DefaultMessage
        fields = ('name', 'phone', 'email', 'message', 'additional_information',)
        widgets = {
            'phone': PhoneWidget(attrs={
                'class': 'form__input',
                'type': 'tel',
                'placeholder': 'Phone',
            }),
            'additional_information': forms.Textarea(attrs={
                'class': 'form__input',
                'rows': 1,
                'placeholder': 'Additional Information'
                # 'wrap': "off",
            }),
        }
        error_messages = {
            'name': {
                'required': _('Please enter your name'),
                'max_length': _('Name should not be longer than %(limit_value)d characters'),
            },
            'phone': {
                'required': _('Please enter your e-mail or phone so we can contact you'),
                'max_length': _('Phone number should not be longer than %(limit_value)d characters'),
            },
            'email': {
                'required': _('Please enter your e-mail or phone so we can contact you'),
                'max_length': _('E-mail should not be longer than %(limit_value)d characters'),
            },
            'message': {
                'required': _('Please enter your message'),
                'max_length': _('Message should not be longer than %(limit_value)d characters'),
            },
        }

    def clean(self):
        """ Требуем указать email ИЛИ телефон """
        if 'phone' in self.cleaned_data and 'email' in self.cleaned_data:
            phone = self.cleaned_data.get('phone')
            email = self.cleaned_data.get('email')

            if not phone and not email:
                self.add_field_error('phone', 'required')
                self.add_field_error('email', 'required')

        return super().clean()

    def __init__(self, *args, **kwargs):
        super(DefaultForm, self).__init__(*args, **kwargs)
        self.fields['captcha'].label = ""
