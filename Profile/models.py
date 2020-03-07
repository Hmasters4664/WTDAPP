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
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from io import StringIO, BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .validators import validate_characters, check_negative_number, check_zero_number
import os


RELATIONSHIP_FOLLOWING = 0
RELATIONSHIP_BLOCKED = 1
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Friends'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.TextField(max_length=50, blank=False, validators=[validate_characters], )
    country = models.CharField(max_length=30, blank=True, validators=[validate_characters], )
    profile_picture = models.ImageField(upload_to='profile', blank=True, null=True,)
    profile_small = models.ImageField(upload_to='profile', blank=True, null=True, )
    profile_medium = models.ImageField(upload_to='profile', blank=True, null=True, )
    city = models.CharField(max_length=30, blank=True, validators=[validate_characters], )
    province = models.CharField(_('provice/state'), max_length=30, blank=True, validators=[validate_characters], )
    birth_date = models.DateField(null=True, blank=True, )
    relationships = models.ManyToManyField('self', through='Relationship',
                                           symmetrical=False, related_name='related_to')
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        ordering = ['-id']

    def save(self, **kwargs):
        if not self.name:
            self.name = "Unkown"
        if not self.slug:
            slug_str = "%s %s" % (self.name, uuid.uuid4())
            self.slug = slugify(slug_str)

        slr = self.slug
        self.profile_picture.name =slr+".png"
        image = Image.open(self.profile_picture)
        image.thumbnail((54, 54), Image.ANTIALIAS)
        output = BytesIO()
        image=image.convert("RGBA")
        image.save(output, format='PNG', quality=85)
        output.seek(0)
        name = slr
        name += "-54.png"
        self.profile_small = InMemoryUploadedFile(output, 'ImageField', name,
                                                      'image/png',
                                                      sys.getsizeof(output), None)
        image = Image.open(self.profile_picture)
        image.thumbnail((160, 155), Image.ANTIALIAS)
        output = BytesIO()
        image=image.convert("RGBA")
        image.save(output, format='PNG', quality=85)
        output.seek(0)
        name = slr
        name += "-160.png"
        self.profile_medium = InMemoryUploadedFile(output, 'ImageField', name,
                                                      'image/png',
                                                      sys.getsizeof(output), None)
        super(Profile, self).save(**kwargs)

    def __unicode__(self):
        return self.name

    def add_relationship(self, person, status, uuids=uuid.uuid4(), symm=True):

        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status,
            uuid=uuids)
        if symm:
            # avoid recursion by passing `symm=False`
            person.add_relationship(self, status, uuids, False)
        return relationship

    def friend_relationship(self, person, symm=True):
        try:
            relationship = Relationship.objects.get(from_person=self, to_person=person)
        except Relationship.DoesNotExist:
            relationship = None

        if relationship:
            relationship.status = 0
            relationship.save()
        if symm:
            # avoid recursion by passing `symm=False`
            person.friend_relationship(self, False)
        return relationship

    def block_relationship(self, person, status, symm=True):
        try:
            relationship = Relationship.objects.get(from_person=self, to_person=person)
        except Relationship.DoesNotExist:
            relationship = None

        if relationship:
            relationship.status = 2
        if symm:
            # avoid recursion by passing `symm=False`
            person.block_relationship(self, status, False)
        return relationship

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self)

    def count_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self).count()

    def remove_relationship(self, person, status, symm=True):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        if symm:
            # avoid recursion by passing `symm=False`
            person.remove_relationship(self, status, False)


class Relationship(models.Model):
    from_person = models.ForeignKey(Profile, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Profile, related_name='to_people', on_delete=models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES, default=1)
    uuid = models.UUIDField(editable=False)

    class Meta:
        ordering = ['-id']

