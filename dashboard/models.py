from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import datetime



class CustomUserManager(BaseUserManager):
    """ Override createuser and createsuperuser to use email as username
    """

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Override django create user
        """
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User Models to manage user related functionaliteis. 
    """
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    
    bloodgroup = models.CharField(max_length=30, blank=True)
    contact = models.CharField(max_length=20,null=True, blank=True)
    emergency_contact_no = models.CharField(max_length=20,null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='media/photos/')
    About = models.CharField(max_length=2000, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def get_username(self):
        return self.email

    def get_full_name(self):
        """Returns the full name of user by combining first_name and last_name
        """
        return "{} {}".format(self.first_name, self.last_name)

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

# Create your models here.


class Image(models.Model):

    title = models.CharField(max_length=20, null=True, blank=True)
    photos = models.ImageField(blank=True, upload_to='media/photos/')
    

    def __str__(self):
        return self.title

    def get_photos(self):
        return self.photos


class ImageAlbum(models.Model):

    name = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateField(_("Date"), default=datetime.date.today)
    active = models.BooleanField(_('active'), default=False)
    images = models.ManyToManyField(Image)
    event_link = models.CharField(max_length=20, null=True, blank=True)


class SiteContent(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    active = models.BooleanField(_('active'), default=False)
    index = models.IntegerField()
    link = models.CharField(max_length=20, null=True, blank=True)


class EventData(models.Model):
    active = models.BooleanField(_('active'), default=False) 
    created =models.CharField(max_length=25)
    name = models.CharField(max_length=255)
    created_id = models.CharField(max_length=255)
    event_datetime = models.DateTimeField()
    status = models.CharField(max_length=55)
    updated = models.CharField(max_length=25)
    updated_date = models.DateTimeField(blank=True, null=True)
    venue_name = models.CharField(max_length=255, null=True, blank=True)
    venue_address = models.CharField(max_length=255, null=True, blank=True)
    venue_city = models.CharField(max_length=255, null=True, blank=True)
    venue_country = models.CharField(max_length=255, null=True, blank=True)
    link = models.CharField(max_length=55)
    Contact_Us = models.CharField(max_length=1000,null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.created_id 

    def get_photos(self):
        return EventPhoto.objects.filter(event=self)


class EventPhoto(models.Model):
    event = models.ForeignKey(EventData,on_delete=models.CASCADE)
    highres_link = models.URLField(max_length=500)
    photo_link = models.URLField(max_length=500)
    thumb_link = models.URLField(max_length=500)
    photo_id = models.CharField(max_length=255)

    def __str__(self):
        return self.photo_id
    

class Press(models.Model):
    title = models.CharField(max_length=255)
    press_description = models.TextField(null=True, blank=True)
    press_photos = models.ImageField(blank=True, upload_to='media/photos/')

    def __str__(self):
        return self.title 
