import os
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm

from dashboard.models import User, Image, ImageAlbum, SiteContent, EventData, EventPhoto


class RegisterForm(forms.ModelForm):
    """Registration form for new users
    """
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password", "bloodgroup", "contact", "emergency_contact_no", "photo", "About"]

    def clean_confirm_password(self):
        """Check for password and confirm_password matching
        """
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords doesn't match")
        return confirm_password


class LoginForm(AuthenticationForm):
    """Login Form with email and password
    """
    pass


class ProfileForm(forms.ModelForm):
    """User Profile edit form
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "date_of_birth"]


class PasswordResetEmailForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("Error: There is no user registered with the specified email address!")
        return email

class UserEditForm(forms.ModelForm):
    """Staff Profile Edit Form """

    class Meta:
        model = User 
        fields = ["first_name", "last_name", "email", "date_of_birth", "is_active", 
                    "is_staff", "bloodgroup", "contact", "emergency_contact_no", "photo", "About"]


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ["title", "photos"]

class ImageAlbumForm(forms.ModelForm):

    class Meta:
        model = ImageAlbum
        fields = ["name", "description", "created_by", "created_on", "active", "images", "event_link"]


class SiteContentForm(forms.ModelForm):

    class Meta:
        model = SiteContent
        fields = ["name", "content", "active", "link"]


class EventDataForm(forms.ModelForm):

    class Meta:
        model = EventData
        fields = ["created", "name", "created_id", "event_datetime", "status", "updated", "venue_name",
                 "venue_address", "venue_city", "venue_country", "link", "Contact_Us", "description",
                 ]


class EventPhotoForm(forms.ModelForm):

    class Meta:
        model = EventPhoto
        fields = ["event", "highres_link", "photo_link", "thumb_link", "photo_id"]