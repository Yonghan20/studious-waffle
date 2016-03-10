from django import forms
from models import *
from messagekey import *
from functions import *
from mongoengine.queryset import DoesNotExist

import re

reg_key = RegisterFormMsg
main_key = MainMsg
log_key = LoginFormMsg
act_key = ActivateFormMsg
res_key = ResetPasswordFormMsg
set_key = SettingsFormMsg

class RegisterForm(forms.Form):
    username = forms.CharField(error_messages={main_key.REQUIRED: reg_key.REQUIRED_USERNAME_MSG},max_length= 10, min_length= 5,
                               widget=forms.TextInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                           main_key.PLACEHOLDER: reg_key.ENTER_USERNAME_MSG,
                                                           main_key.AUTOFOCUS: True,
                                                           main_key.ONFOCUS : main_key.CURSORTOEND}))
    display_name = forms.CharField(error_messages={main_key.REQUIRED: reg_key.REQUIRED_DISPLAY_NAME_MSG},max_length=10, min_length=1,
                             widget=forms.TextInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                        main_key.PLACEHOLDER: reg_key.ENTER_DISPLAYNAME_MSG}))
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=reg_key.GENDER_CHOICES, initial=reg_key.GENDER_CHOICES[0][0])
    email = forms.EmailField(error_messages={main_key.REQUIRED: reg_key.REQUIRED_EMAIL_MSG},max_length=100,
                             widget=forms.TextInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                        main_key.PLACEHOLDER: reg_key.ENTER_EMAIL_MSG}))
    password = forms.CharField(error_messages={main_key.REQUIRED: reg_key.REQUIRED_PASSWORD_MSG},min_length=6, max_length=12,
                               widget=forms.PasswordInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                               main_key.PLACEHOLDER: reg_key.ENTER_PASSWORD_MSG}))
    confirm_password = forms.CharField(error_messages={main_key.REQUIRED: reg_key.REQUIRED_CONFIRM_PASSWORD_MSG},min_length=6, max_length=12,
                                       widget=forms.PasswordInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                                        main_key.PLACEHOLDER: reg_key.ENTER_CONFIRM_PASSWORD_MSG }))
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get(reg_key.USERNAME)
        email = cleaned_data.get(reg_key.EMAIL)
        password = cleaned_data.get(reg_key.PASSWORD)
        confirm_password = cleaned_data.get(reg_key.CONFIRM_PASSWORD)

        #email space validation have to do here, no idea why
        data = self.data
        fields = self.fields
        errors = self.add_error
        input = reg_key.EMAIL # cant do with data[reg_key.EMAIL], no idea why
        data[input] = data[input].strip()

    def clean_email(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        input = reg_key.EMAIL # cant do with data[reg_key.EMAIL], no idea why

        data[input] = data[input].strip()
        user = GetUserByUsernameOrEmail(data[input])
        if user is not False:
            errors(input, reg_key.EMAIL_EXISTS % data[input])

    def clean_display_name(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        input = reg_key.DISPLAY_NAME

        strip_value = data[input] = data[input].strip()
        if len(strip_value) == 0:
            errors(input, reg_key.REQUIRED_DISPLAY_NAME_MSG)
        elif not re.match("^[A-Za-z0-9_-]*$", strip_value):
            errors(input, reg_key.DISPLAY_NAME_INVALID)

    def clean_username(self):
        data = self.data
        errors = self.add_error
        input = reg_key.USERNAME
        strip_value = data[input] = data[input].strip()
        if len(strip_value) == 0:
            errors(input, reg_key.REQUIRED_USERNAME_MSG)
        elif not re.match("^[A-Za-z0-9\s_-]*$", strip_value):
            errors(input, reg_key.USER_NAME_INVALID)
        else:
            user = GetUserByUsernameOrEmail(data[input])
            if user is not False:
                errors(input, reg_key.USERNAME_EXISTS % data[input])

    def clean_password(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        input = reg_key.PASSWORD
        input2 = reg_key.CONFIRM_PASSWORD

        if data[input] != data[input2]:
            errors(input, reg_key.PASSWORD_NOT_MATCH_MSG)

    def clean_confirm_password(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        input = reg_key.PASSWORD
        input2 = reg_key.CONFIRM_PASSWORD

        if data[input] != data[input2]:
            errors(input2, reg_key.CONFIRM_PASSWORD_NOT_MATCH_MSG)

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({main_key.STYLE: main_key.BORDER_RED})
        return ret

class ActivationForm(forms.Form):
    account = forms.CharField(error_messages={main_key.REQUIRED: act_key.REQUIRED_ACCOUNT_MSG},max_length=100,
                             widget=forms.TextInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                        main_key.PLACEHOLDER: act_key.ENTER_ACCOUNT_MSG}))
    def clean(self):
        cleaned_data = super(ActivationForm, self).clean()
        account = cleaned_data.get(log_key.ACCOUNT)

    def clean_account(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        input = act_key.ACCOUNT

        strip_value = data[input] = data[input].strip()
        if len(strip_value) == 0:
            errors(input, act_key.REQUIRED_ACCOUNT_MSG)
        else:
            user = GetUserByUsernameOrEmail(data[input])
            if user is False:
                errors(input, act_key.USERNAME_OR_EMAIL_NOT_EXIST)
            elif user.is_active == True:
                errors(input, act_key.IS_ACTIVATED_MSG)

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({main_key.STYLE: main_key.BORDER_RED})
        return ret

class LoginForm(forms.Form):
    account = forms.CharField(error_messages={main_key.REQUIRED: log_key.REQUIRED_ACCOUNT_MSG},max_length=100,
                               widget=forms.TextInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                           main_key.PLACEHOLDER: log_key.ENTER_ACCOUNT_MSG,
                                                           main_key.AUTOFOCUS: True,
                                                           main_key.ONFOCUS : main_key.CURSORTOEND}))
    password = forms.CharField(error_messages={main_key.REQUIRED: log_key.REQUIRED_PASSWORD_MSG}, max_length=12,
                               widget=forms.PasswordInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                               main_key.PLACEHOLDER: log_key.ENTER_PASSWORD_MSG}))
    remember_me = forms.BooleanField(required=False)
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        account = cleaned_data.get(log_key.ACCOUNT)
        password = cleaned_data.get(log_key.PASSWORD)

    def clean_account(self):
        data = self.data
        errors = self.add_error
        input = log_key.ACCOUNT
        input2 = log_key.PASSWORD
        strip_value = data[input] = data[input].strip()
        if len(strip_value) == 0:
            errors(input, log_key.REQUIRED_ACCOUNT_MSG)
        else:
            user = GetUserByUsernameOrEmail(data[input])
            if user is False:
                errors(input, log_key.INVALID_ERROR_MSG)
            elif user.check_password(data[input2]) is False:
                errors(input, log_key.INVALID_ERROR_MSG)

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({main_key.STYLE: main_key.BORDER_RED})
        return ret

class ResetPasswordForm(forms.Form):
    account = forms.CharField(error_messages={main_key.REQUIRED: act_key.REQUIRED_ACCOUNT_MSG},max_length=100,
                             widget=forms.TextInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                        main_key.PLACEHOLDER: act_key.ENTER_ACCOUNT_MSG}))
    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        account = cleaned_data.get(log_key.ACCOUNT)

    def clean_account(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        input = act_key.ACCOUNT

        strip_value = data[input] = data[input].strip()
        if len(strip_value) == 0:
            errors(input, act_key.REQUIRED_ACCOUNT_MSG)
        else:
            user = GetUserByUsernameOrEmail(data[input])
            if user is False:
                errors(input, act_key.USERNAME_OR_EMAIL_NOT_EXIST)

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({main_key.STYLE: main_key.BORDER_RED})
        return ret

class SettingsForm(forms.Form):
    username = forms.CharField(error_messages={main_key.REQUIRED: reg_key.REQUIRED_USERNAME_MSG},max_length= 10, min_length= 5,
                               widget=forms.HiddenInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                           main_key.PLACEHOLDER: reg_key.ENTER_USERNAME_MSG}))
    display_name = forms.CharField(error_messages={main_key.REQUIRED: reg_key.REQUIRED_DISPLAY_NAME_MSG},max_length=10, min_length=1,
                             widget=forms.TextInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                        main_key.PLACEHOLDER: reg_key.ENTER_DISPLAYNAME_MSG}))
    privacy = forms.ChoiceField(error_messages={main_key.REQUIRED: set_key.REQUIRED_PRIVACY_MSG},
                                widget=forms.RadioSelect, choices=set_key.PRIVACY_CHOICES)

    old_password = forms.CharField(min_length=6, max_length=12, required=False,
                               widget=forms.PasswordInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                               main_key.PLACEHOLDER: set_key.ENTER_OLD_PASSWORD_MSG}))
    password = forms.CharField(min_length=6, max_length=12, required=False,
                               widget=forms.PasswordInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                               main_key.PLACEHOLDER: set_key.ENTER_PASSWORD_MSG}))
    confirm_password = forms.CharField(min_length=6, max_length=12, required=False,
                                       widget=forms.PasswordInput(attrs={main_key.CLASS: main_key.FORM_CONTROL_CLASS,
                                                                        main_key.PLACEHOLDER: set_key.ENTER_CONFIRM_PASSWORD_MSG }))

    def clean(self):
        cleaned_data = super(SettingsForm, self).clean()
        old_password = cleaned_data.get(set_key.OLD_PASSWORD)
        password = cleaned_data.get(set_key.PASSWORD)
        confirm_password = cleaned_data.get(set_key.CONFIRM_PASSWORD)
        privacy = cleaned_data.get(set_key.PRIVACY)

    def clean_username(self):
        data = self.data
        errors = self.add_error
        input = reg_key.USERNAME
        strip_value = data[input] = data[input].strip()
        if len(strip_value) == 0:
            errors(input, reg_key.REQUIRED_USERNAME_MSG)
        elif not re.match("^[A-Za-z0-9_-]*$", strip_value):
            errors(input, reg_key.USER_NAME_INVALID)

    def clean_display_name(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        input = reg_key.DISPLAY_NAME

        strip_value = data[input] = data[input].strip()
        if len(strip_value) == 0:
            errors(input, reg_key.REQUIRED_DISPLAY_NAME_MSG)
        elif not re.match("^[A-Za-z0-9\s_-]*$", strip_value):
            errors(input, reg_key.DISPLAY_NAME_INVALID)

    def clean_old_password(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        input = reg_key.USERNAME
        old = set_key.OLD_PASSWORD
        new = set_key.PASSWORD
        confirm = set_key.CONFIRM_PASSWORD

        if len(data[old]) > 0 or len(data[new]) > 0 or len(data[confirm]) > 0:
            if len(data[old]) <= 0:
                errors(old, set_key.REQUIRED_OLD_PASSWORD_MSG)
            else:
                user = GetUserByUsernameOrEmail(data[input])
                if user.check_password(data[old]) is False:
                    errors(old, set_key.OLD_PASSWORD_INVALID_MSG)

    def clean_password(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        old = set_key.OLD_PASSWORD
        new = set_key.PASSWORD
        confirm = set_key.CONFIRM_PASSWORD
        if len(data[old]) > 0 or len(data[new]) > 0 or len(data[confirm]) > 0:
            if len(data[new]) <= 0:
                errors(new, set_key.REQUIRED_PASSWORD_MSG)
            elif data[new] != data[confirm]:
                errors(new, set_key.PASSWORD_NOT_MATCH_MSG)

    def clean_confirm_password(self):
        data = self.data
        fields = self.fields
        errors = self.add_error
        old = set_key.OLD_PASSWORD
        new = set_key.PASSWORD
        confirm = set_key.CONFIRM_PASSWORD
        if len(data[old]) > 0 or len(data[new]) > 0 or len(data[confirm]) > 0:
            if len(data[confirm]) <= 0:
                errors(confirm, set_key.REQUIRED_CONFIRM_PASSWORD_MSG)
            elif data[confirm] != data[new]:
                errors(confirm, set_key.CONFIRM_PASSWORD_NOT_MATCH_MSG)

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update({main_key.STYLE: main_key.BORDER_RED})
        return ret

