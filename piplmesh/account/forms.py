import datetime

from django import forms
from django.forms import widgets
from django.forms.extras import widgets as extras_widgets
from django.utils import encoding, safestring
from django.utils.translation import ugettext_lazy as _

from piplmesh.account import fields, form_fields, models

class RadioFieldRenderer(widgets.RadioFieldRenderer):
    """
    RadioSelect renderer which adds ``first`` and ``last`` style classes
    to first and last radio widgets.
    """

    def _render_widgets(self):
        for i, w in enumerate(self):
            classes = []
            if i == 0:
                classes.append('first')
            if i == len(self.choices) - 1:
                classes.append('last')

            cls = ''
            if classes:
                cls = u' class="%s"' % (u' '.join(classes),)

            yield u'<li%s>%s</li>' % (cls, encoding.force_unicode(w))

    def render(self):
        return safestring.mark_safe(u'<ul>\n%s\n</ul>' % (u'\n'.join(self._render_widgets())),)

class UserUsernameForm(forms.Form):
    """
    Class with username form.
    """

    username = forms.RegexField(
        label=_("Username"),
        max_length=30,
        min_length=4,
        regex='^' + models.USERNAME_REGEX + '$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters."),
        }
    )

    def clean_username(self):
        """
        This method checks whether the username exists in a case-insensitive manner.
        """

        username = self.cleaned_data['username']
        if models.User.objects(username__iexact=username).count():
            raise forms.ValidationError(_("A user with that username already exists."), code='username_exists')
        return username

class UserPasswordForm(forms.Form):
    """
    Class with user password form.
    """

    password1 = forms.CharField(
        label=_("Password"),
        min_length=6,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password (repeat)"),
        min_length=6,
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )

    def clean_password2(self):
        """
        This method checks whether the passwords match.
        """

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError(_("The two password fields did not match."), code='password_mismatch')
        return password2


class UserCurrentPasswordForm(forms.Form):
    """
    Class with user current password form.
    """

    current_password = forms.CharField(
        label=_("Current password"),
        widget=forms.PasswordInput,
        help_text=_("Enter your current password, for verification."),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserCurrentPasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        """
        This method checks if user password is correct.
        """

        password = self.cleaned_data['current_password']
        if self.user.check_password(password):
            return password
        raise forms.ValidationError(_("Your old password was entered incorrectly."), code='password_incorrect')

class UserBasicInfoForm(forms.Form):
    """
    Class with user basic information form.
    """

    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    email = forms.EmailField(label=_("E-mail"))
    gender = forms.ChoiceField(
        label=_("Gender"),
        choices=fields.GENDER_CHOICES,
        widget=forms.RadioSelect(renderer=RadioFieldRenderer),
    )
    birthdate = form_fields.LimitedDateTimeField(
        upper_limit=models.upper_birthdate_limit,
        lower_limit=models.lower_birthdate_limit,
        label=_("Birth date"),
        required=False,
        widget=extras_widgets.SelectDateWidget(
            years=[
                y for y in range(
                    models.upper_birthdate_limit().year,
                    models.lower_birthdate_limit().year,
                    -1,
                )
            ],
        ),
    )

class UserAdditionalInfoForm(forms.Form):
    """
    Class with user additional information form.
    """

class RegistrationForm(UserUsernameForm, UserPasswordForm, UserBasicInfoForm):
    """
    Class with registration form.
    """

class AccountChangeForm(UserBasicInfoForm, UserAdditionalInfoForm, UserCurrentPasswordForm):
    """
    Class with form for changing your account settings.
    """

class PasswordChangeForm(UserCurrentPasswordForm, UserPasswordForm):
    """
    Class with form for changing password.
    """
