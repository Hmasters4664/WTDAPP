import sys

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
import uuid


class Event(models.Model):
    title = models.TextField(max_length=100, blank=True, )
    info_link = models.CharField(max_length=150, blank=True, )
    image_link = models.CharField(max_length=150, blank=True, )
    date_string = models.TextField(max_length=100, blank=True, )
    dates = models.DateField(_('Date of Birth'), null=True, blank=True, )
    long_position = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True,)
    lat_position = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True,)
    location = models.TextField(blank=True, null=True,)
    province = models.TextField(blank=True, null=True, )
    category = models.CharField(max_length=30, blank=True, null=True, )
    slug = models.SlugField(blank=True, unique=True)

    def save(self, **kwargs):
        if not self.title:
            self.title = "Unkown"

        slug_str = "%s %s" % (self.title, uuid.uuid4())
        self.slug = slugify(slug_str)
        super(Event, self).save(**kwargs)
