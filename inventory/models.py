
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy
from django.utils import timezone
import misaka
import os
import uuid



# Choices for language
ENG = 1
FRE = 2
LANGUAGE_CHOICES = (
    (ENG,'English'),
    (FRE,'French'),
)

# Create your models here.

class Location(models.Model):
    # Choices for surface_type
    CAN = 'Canada'
    US = 'United States'
    COUNTRY_CHOICES = (
        (CAN,'Canada'),
        (US,'United States'),
    )
    location_eng = models.CharField(max_length=1000, blank=True, null=True)
    location_fre = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField( max_length=25, choices=COUNTRY_CHOICES)
    abbrev_eng = models.CharField(max_length=25, blank=True, null=True)
    abbrev_fre = models.CharField(max_length=25, blank=True, null=True)
    uuid_gcmd = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} {}".format(location_eng)


class Organization(models.Model):
    name_eng = models.CharField(max_length=1000, blank=True, null=True)
    name_fre = models.CharField(max_length=1000, blank=True, null=True)
    abbrev = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=7, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name_eng)

    class Meta:
        ordering = ['name_eng']

class PersonRole(models.Model):
    role = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.role

    class Meta:
        ordering = ['id']

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="person")
    full_name = models.CharField(max_length=255, blank=True, null=True)
    position_eng = models.CharField(max_length=255, blank=True, null=True)
    position_fre = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(self.user.last_name, self.user.first_name)

    class Meta:
        ordering = ['user']

    def save(self,*args,**kwargs):
        self.full_name = "{} {}".format(self.user.first_name, self.user.last_name)

        super().save(*args,**kwargs)

class Section(models.Model):
    section = models.CharField(max_length=255)
    abbrev  = models.CharField(max_length=25, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(max_length=255, blank=True, null=True)
    unit_head = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="section_heads")
    manager = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="section_manangers")

    def __str__(self):
        return "{} ({})".format(self.section, self.division)

    class Meta:
        ordering = ['section']


class Status(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label

class SpatialRepresentationType(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label

class SpatialReferenceSystem(models.Model):
    label = models.CharField(max_length=255)
    code = models.CharField(max_length=25, blank=True, null=True)
    codespace = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label

class SecurityClassification(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.label

class ResourceType(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'inventory_resource_type'


class Maintenance(models.Model):
    frequency = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.frequency

class CharacterSet(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label

class KeywordDomain(models.Model):
    name_eng = models.CharField(max_length=255, blank=True, null=True)
    name_fre = models.CharField(max_length=255, blank=True, null=True)
    abbrev = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    web_services = models.BooleanField()
    xml_block = models.TextField(blank=True, null = True)

    def __str__(self):
        return self.name_eng

class Keyword(models.Model):
    text_value_eng = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Keyword value (English)")
    text_value_fre = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Keyword value (French)")
    uid = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Unique Identifier")
    concept_scheme = models.CharField(max_length=1000, blank=True, null=True)
    details = models.TextField(blank=True, null = True)
    keyword_domain = models.ForeignKey(KeywordDomain, on_delete=models.DO_NOTHING, blank=True, null = True)
    xml_block = models.TextField(blank=True, null = True)
    is_taxonomic = models.BooleanField(default=False)

    def __str__(self):
        return self.text_value_eng

    class Meta:
        ordering = ["keyword_domain","text_value_eng"]

    def save(self,*args,**kwargs):
        if self.keyword_domain.id == 2 or self.keyword_domain.id == 5:
            self.is_taxonomic = True
        super().save(*args,**kwargs)

    # def get_absolute_url(self):
    #     return reverse('resources:keyword_detail', kwargs={'pk':self.id})


class Publication(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Citation(models.Model):
    title_eng = models.TextField(blank=True, null=True, verbose_name="Title (English)")
    title_fre = models.TextField(blank=True, null=True, verbose_name="Title (French)")
    authors = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    publication = models.ForeignKey(Publication, on_delete=models.DO_NOTHING, blank=True, null = True)
    pub_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Publication Number")
    url_eng = models.TextField(blank=True, null = True, verbose_name="URL (English)")
    url_fre = models.TextField(blank=True, null = True, verbose_name="URL (French)")
    abstract_eng = models.TextField(blank=True, null = True, verbose_name="Abstrast (English)")
    abstract_fre = models.TextField(blank=True, null = True, verbose_name="Abstrast (French)")
    series = models.CharField(max_length=1000, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title_eng

    @property
    def short_citation(self):
        if self.title_eng != None:
            title = self.title_eng
        else:
            title = self.title_fre

        my_str = "{authors}. {year}. {title}. {publication} {pub_number}.".format(
            authors=self.authors,
            year = self.year,
            title = title,
            publication = self.publication,
            pub_number = self.pub_number,
        )

        return my_str


    @property
    def short_citation_html(self):
        if self.title_eng != None:
            title = self.title_eng
        else:
            title = self.title_fre

        if self.url_eng == None:
            my_str = "{authors}. {year}. {title}. {publication} {pub_number}.".format(
                authors=self.authors,
                year = self.year,
                title = title,
                publication = self.publication,
                pub_number = self.pub_number,
            )
        else:
            my_str = "{authors}. {year}. <a href=""{url_eng}""> {title}</a>. {publication} {pub_number}.".format(
                authors=self.authors,
                year = self.year,
                title = title,
                publication = self.publication,
                pub_number = self.pub_number,
                url_eng = self.url_eng,
            )
        return my_str

    @property
    def citation_br(self):
        if self.title_eng != None:
            title = self.title_eng
        else:
            title = self.title_fre

        my_str = "<b>Title:</b> {title}<br><b>Authors:</b> {authors}<br><b>Year:</b> {year}<br><b>Publication:</b> {publication}. {pub_number}".format(
            authors=self.authors,
            year = self.year,
            title = title,
            publication = self.publication,
            pub_number = self.pub_number,
        )
        return my_str


    @property
    def title(self):
        if self.title_eng != None:
            title = self.title_eng
        else:
            title = self.title_fre

        return title


class Resource(models.Model):
    uuid = models.UUIDField(blank=True, null=True, verbose_name="UUID")
    resource_type = models.ForeignKey(ResourceType, on_delete=models.DO_NOTHING, blank=True, null = True)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, blank=True, null = True)
    title_eng = models.TextField(verbose_name="Title (English)")
    title_fre = models.TextField(blank=True, null = True, verbose_name="Title (French)")
    purpose_eng = models.TextField(blank=True, null = True, verbose_name="Purpose (English)")
    purpose_fre = models.TextField(blank=True, null = True, verbose_name="Purpose (French)")
    descr_eng = models.TextField(blank=True, null = True, verbose_name="Description (English)")
    descr_fre = models.TextField(blank=True, null = True, verbose_name="Description (French)")
    physical_sample_descr_eng = models.TextField(blank=True, null = True, verbose_name="Description of physical samples (English)")
    physical_sample_descr_fre = models.TextField(blank=True, null = True, verbose_name="Description of physical samples (French)")
    time_start_day = models.IntegerField(blank=True, null = True, verbose_name="Start day")
    time_start_month = models.IntegerField(blank=True, null = True, verbose_name="Start month")
    time_start_year = models.IntegerField(blank=True, null = True, verbose_name="Start year")
    time_end_day = models.IntegerField(blank=True, null = True, verbose_name="End day")
    time_end_month = models.IntegerField(blank=True, null = True, verbose_name="End month")
    time_end_year = models.IntegerField(blank=True, null = True, verbose_name="End year")
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null = True)
    maintenance = models.ForeignKey(Maintenance, on_delete=models.DO_NOTHING, blank=True, null = True, verbose_name="Maintenance frequency")
    sampling_method_eng = models.TextField(blank=True, null = True, verbose_name="Sampling method (English)")
    sampling_method_fre = models.TextField(blank=True, null = True, verbose_name="Sampling method (French)")
    resource_constraint_eng = models.TextField(blank=True, null = True, verbose_name="Resource constraint (English)")
    resource_constraint_fre = models.TextField(blank=True, null = True, verbose_name="Resource constraint (French)")
    qc_process_descr_eng = models.TextField(blank=True, null = True, verbose_name="QC process description (English)")
    qc_process_descr_fre = models.TextField(blank=True, null = True, verbose_name="QC process description (French)")
    security_use_limitation_eng = models.CharField(max_length=255, blank=True, null = True, verbose_name="Security use limitation (English)")
    security_use_limitation_fre = models.CharField(max_length=255, blank=True, null = True, verbose_name="Security use limitation (French)")
    security_classification = models.ForeignKey(SecurityClassification, on_delete=models.DO_NOTHING, blank=True, null = True)
    storage_envr_notes = models.TextField(blank=True, null=True, verbose_name="Storage notes (internal)")
    distribution_format = models.CharField(max_length=255,blank=True, null=True)
    open_data_notes = models.CharField(max_length=255,blank=True, null=True, verbose_name="Open data notes (internal only)")
    public_url = models.CharField(max_length=1000,blank=True, null=True, verbose_name="Public URL")
    geo_descr_eng = models.CharField(max_length=255,blank=True, null=True, verbose_name="Geographic description (English)")
    geo_descr_fre = models.CharField(max_length=255,blank=True, null=True, verbose_name="Geographic description (French)")
    spat_ref_system = models.ForeignKey(SpatialReferenceSystem, on_delete=models.DO_NOTHING, blank=True, null = True, verbose_name="Spatial reference system")
    spat_representation = models.ForeignKey(SpatialRepresentationType, on_delete=models.DO_NOTHING, blank=True, null = True, verbose_name="Spatial representation type")
    data_char_set = models.ForeignKey(CharacterSet, on_delete=models.DO_NOTHING, blank=True, null = True, verbose_name="Data character set")
    west_bounding = models.FloatField(blank=True, null=True, verbose_name="West bounding coordinate")
    south_bounding = models.FloatField(blank=True, null=True, verbose_name="South bounding coordinate")
    east_bounding = models.FloatField(blank=True, null=True, verbose_name="East bounding coordinate")
    north_bounding = models.FloatField(blank=True, null=True, verbose_name="North bounding coordinate")
    parameters_collected_eng = models.TextField(blank=True, null = True, verbose_name="Parameters collected (English)")
    parameters_collected_fre = models.TextField(blank=True, null = True, verbose_name="Parameters collected (French)")
    additional_credit = models.TextField(blank=True, null = True)
    analytic_software = models.TextField(blank=True, null = True, verbose_name="Analytic software notes (internal)")
    date_verified = models.DateTimeField(blank=True, null=True)
    fgp_publication_date = models.DateTimeField(blank=True, null=True, verbose_name="Date published to FGP")
    notes = models.TextField(blank=True, null = True, verbose_name="General notes (internal)")
    citations = models.ManyToManyField(Citation, related_name='resources')
    keywords = models.ManyToManyField(Keyword, related_name='resources')
    people = models.ManyToManyField(Person, through='ResourcePerson')
    parent = models.ForeignKey("self", on_delete=models.DO_NOTHING, blank=True, null=True, related_name='children', verbose_name="Parent resource")
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now)
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)


    def get_absolute_url(self):
        return reverse('inventory:resource_detail', kwargs={'pk':self.pk})

    class Meta:
        ordering = ['id',]

    def __str__(self):
        return "({}) {}".format(self.id,self.title_eng)

    def truncated_title(self):
        if self.title_eng:
            if self.title_eng.__len__() > 50:
                my_str = self.title_eng[:50]+" ..."
            else:
                my_str = self.title_eng
        else:
            my_str = "no title"

        return my_str

    def save(self,*args,**kwargs):
        if self.uuid == None:
            self.uuid = uuid.uuid1()

        super().save(*args,**kwargs)



class ResourcePerson(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING, related_name="resource_people")
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="resource_people")
    role = models.ForeignKey(PersonRole, on_delete=models.DO_NOTHING)
    notes = models.TextField(blank=True, null = True)

    class Meta:
        unique_together = (('resource', 'person', 'role'),)
        db_table = 'inventory_resource_people'
        ordering = ['role']

    def get_absolute_url(self):
        return reverse('inventory:resource_detail', kwargs={'pk':self.resource.id})


class BoundingBox(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    west_bounding = models.FloatField(blank=True, null=True)
    south_bounding = models.FloatField(blank=True, null=True)
    east_bounding = models.FloatField(blank=True, null=True)
    north_bounding = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

class ResourceCertification(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING, related_name="certification_history")
    certifying_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    certification_date = models.DateTimeField(blank=True, null=True, verbose_name="Date published to FGP")
    notes = models.TextField(blank=True, null = True)

    class Meta:
        ordering = ['-certification_date']
        db_table = 'inventory_resource_certification'


class Correspondence(models.Model):
    custodian = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="correspondences")
    subject = models.CharField(max_length=255)
    date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        ordering = ['-date']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     Person.profile.save()