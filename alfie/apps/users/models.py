from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.localflavor.us.models import USStateField

from userena.models import UserenaBaseProfile

import datetime

# https://docs.djangoproject.com/en/dev/topics/auth/

class UserProfile(UserenaBaseProfile):
    """
    Creates a UserProfile object keyed to a User object that defines user profile information.

    """

    # Keyed to User object
    # fields=email, password, firstname, lastname
    user = models.OneToOneField(User, unique=True, verbose_name=_('user'), related_name='my_profile')

    # shipping address
    ship_address_1 = models.CharField(_("Address"), max_length=128, blank=True, null=True)
    ship_address_2 = models.CharField(_("Address cont'd"), max_length=128, blank=True, null=True)
    ship_city = models.CharField(_("City"), max_length=64, blank=True, null=True)
    ship_state = USStateField(_("State"), blank=True, null=True)
    ship_zip_code = models.CharField(_("Zip code"), max_length=5, blank=True, null=True)
	
    # Plan choice
    choice = models.CharField(_("plan level"), max_length=255, blank=True, null=True)

    # Preferences
    # spice = models.CharField(_("spice level"), max_length=255, blank=True, null=True)
    # allergy = models.CharField(_("allergy"), max_length=255, blank=True, null=True)

    # Housekeeping
    subscribed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cancelled = models.DateTimeField(blank=True, null=True, editable=False)
    killed = models.DateTimeField(blank=True, null=True, editable=False) # keep for 90 days

	# Payment info
    last_4_digits = models.CharField(max_length=4, blank=True, null=True)
    stripe_id = models.CharField(max_length=255, blank=True, null=True)