# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

LANGUAGES = ["java", "php", "node"]

class InvalidLanguage(Exception):
    pass

class Language(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_language(cls):
        return cls.__name__.lower()

class JAVA(Language):
    jdk_version = models.CharField(max_length=32, blank=True)

    class Meta:
        db_table = "java"

    @staticmethod
    def get_form_class():
        from .forms import JAVAForm
        return JAVAForm

class PHP(Language):
    php_version = models.CharField(max_length=32, blank=True)

    class Meta:
        db_table = "php"

    @staticmethod
    def get_form_class():
        from .forms import PHPForm
        return PHPForm


class NODE(Language):
    node_version = models.CharField(max_length=32, blank=True)

    class Meta:
        db_table = "node"

    @staticmethod
    def get_form_class():
        from .forms import NODEForm
        return NODEForm

class Setting(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def language(self):
        if self.content_type:
            return self.content_type.model
        else:
            return "N/A"

    @language.setter
    def language(self, value):
        if self.language != value:
            self.content_type = ContentType.objects.get(model=value)
            self.object_id = self.content_type.model_class().objects.create().id
            self.save()

class Application(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=50)
    repository = models.CharField(max_length=50)

    owner = models.ForeignKey(User)
    date_added = models.DateTimeField(default=timezone.now)
    setting = models.OneToOneField(Setting, null=True, blank=True)

    @staticmethod
    def get_all_languages():
        return LANGUAGES

    def get_language(self):
        if self.setting:
            return self.setting.language
        else:
            return "N/A"

    def set_language(self, lang):
        LANGS = self.get_all_languages()
        if lang in LANGS:
            if self.setting:
                self.setting.language = lang
            else:
                content_type = ContentType.objects.get(model=lang)
                object_id = content_type.model_class().objects.create().id
                self.setting = Setting.objects.create(content_type=content_type, object_id=object_id)
            self.save()
        else:
            raise InvalidLanguage("Language {0} is invalid, please select from {1}.".format(lang, '/'.join(LANGS)))
    language = property(get_language, set_language)

    def get_setting_instance(self):
        return self.setting.content_object

class Environment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    jenkins_job_url = models.URLField()

    max_unavailable_number = models.PositiveIntegerField()
    concurrency = models.PositiveIntegerField()

    application = models.ForeignKey(Application)

class Version(models.Model):
    STATUS = (
        ('SUCCESS', 'SUCCESS'),
        ('FAILURE', 'FAILURE')
    )

    name = models.CharField(max_length=10)
    branch = models.CharField(max_length=30)
    is_build_successful = models.BooleanField()
    jenkins_build_status = models.CharField(max_length=10, choices=STATUS)
    artifact_url = models.CharField(max_length=50)

    environment = models.ForeignKey(Environment, related_name="versions")

# class Node(models.Model):
#     hostname = models.CharField(max_length=30)
#     ip_address = models.GenericIPAddressField()
#     environment = models.ForeignKey(Environment, related_name="nodes")

class Depoloyment(models.Model):
    STATUS = (
        ('CREATED', 'CREATED'),
        ('PENGING', 'PENDING'),
        ('EXECUTING', 'EXECUTING'),
        ('DONE', 'DONE'),
        ('FAILED', 'FAILED')
    )
    environment = models.ForeignKey(Environment, related_name="deployments")
    # nodes = models.ManyToManyField(Node)
    version = models.ForeignKey(Version)
    status = models.CharField(max_length=10, choices=STATUS)

class Task(models.Model):
    STATUS = (
        ('UNREACHABLE', 'UNREACHABLE'),
        ('PENDING', 'PENDING'),
        ('PROGRESS', 'PROGRESS'),
        ('SKIPPED', 'SKIPPED'),
        ('FAILED', 'FAILED'),
        ('COMPLETED', 'COMPLETED')
    )
    deployment = models.ForeignKey(Depoloyment, related_name="tasks")
    name = models.CharField(max_length=50)
    stdout = models.TextField()
    stderr = models.TextField()
    # status = models.CharField(max_length=20, choices=STATUS)


class Foo(models.Model):
    bar = models.CharField(max_length=10)

from bitfield import BitField
class MyModel(models.Model):
    flags = BitField(flags=(
        'awesome_flag',
        'flaggy_foo',
        'baz_bar',
    ))

from django.contrib.postgres.fields import ArrayField
class Post(models.Model):
    name = models.CharField(max_length=200)
    tags = ArrayField(models.CharField(max_length=200), blank=True)

    def __str__(self):
        return self.name

from django.contrib.postgres.fields import JSONField
class Dog(models.Model):
    name = models.CharField(max_length=200)
    # data = JSONField()

    # def __str__(self):
    #     return self.name

from picklefield.fields import PickledObjectField
class SomeObject(models.Model):
    args = PickledObjectField()
