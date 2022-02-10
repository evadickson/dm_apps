from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from shared_models.models import SimpleLookup, UnilingualSimpleLookup, MetadataFields

YES_NO_CHOICES = (
    (1, "Yes"),
    (0, "No"),
)


class LengthsUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lengths_user", verbose_name=_("DM Apps user"))
    is_admin = models.BooleanField(default=False, verbose_name=_("app administrator?"), choices=YES_NO_CHOICES)
    is_crud_user = models.BooleanField(default=False, verbose_name=_("CRUD permissions?"), choices=YES_NO_CHOICES)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        ordering = ["-is_admin", "user__first_name", ]


class Sampler(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        if not self.first_name:
            return "{}".format(self.last_name)
        else:
            return "{}, {}".format(self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name', 'first_name']


class Species(models.Model):
    aphia_id = models.IntegerField(blank=True, null=True, unique=True, verbose_name="WoRMS AphiaID")
    common_name_en = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("English common name"))
    common_name_fr = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French common name"))
    scientific_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Scientific name"))

    def __str__(self):
        return self.tname

    @property
    def tname(self):
        # check to see if a french value is given
        if getattr(self, str(_("common_name_en"))):
            return "{}".format(getattr(self, str(_("common_name_en"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.common_name_en)

    def get_absolute_url(self):
        return reverse('shared_models:species_detail', kwargs={'pk': self.id})

    @property
    def formatted_scientific_name(self):
        return mark_safe("<em>{}</em>".format(self.scientific_name))


class Port(models.Model):
    ''' Model is shared between Port app and Herring app'''
    PROVINCE_CHOICES = (
        ("1", _('NS')),
        ("2", _('NB')),
        ("3", _('PE')),
        ("4", _('QC')),
        ("5", _('NL')),
    )

    province_code = models.CharField(max_length=1, choices=PROVINCE_CHOICES, verbose_name=_("Province"))
    district_code = models.CharField(max_length=2)
    port_code = models.CharField(max_length=2)
    port_name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    herring_fishing_area_code = models.CharField(max_length=100, blank=True, null=True)
    nafo_unit_area_code = models.CharField(max_length=100, blank=True, null=True)

    # These two fields are just temporary. they are being created to help bridge the data from the hlog format into oracle.
    # They should be deleted once the new herring database is being used.
    alias_wharf_id = models.IntegerField(blank=True, null=True)
    alias_wharf_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{}, {} ({}{}-{})".format(self.port_name, self.get_province_code_display(), self.province_code, self.district_code,
                                         self.port_code)

    @property
    def full_district(self):
        return "{}{}".format(self.province_code, self.district_code, )

    @property
    def full_code(self):
        return "{}{}{}".format(self.province_code, self.district_code, self.port_code)

    class Meta:
        ordering = ['port_name', 'province_code', 'district_code', 'port_code']
        unique_together = ['province_code', 'district_code', 'port_code']

    def get_absolute_url(self):
        return reverse('port:port_list')


class FishingArea(UnilingualSimpleLookup):
    type_choices = (
        (1, "herring"),
        (2, "groundfish"),
        (3, "lobster"),
        (4, "NAFO"),
    )
    type = models.IntegerField(verbose_name=_("type"), choices=type_choices)

    class Meta:
        ordering = ['type', 'name']


class Gear(models.Model):
    gear = models.CharField(max_length=255)
    gear_code = models.CharField(max_length=255)
    nafo_code = models.IntegerField(null=True, blank=True)
    uses_bait = models.BooleanField(default=False, verbose_name=_("is bait used with this gear?"))

    def __str__(self):
        return "{} - {}".format(self.gear_code, self.gear)

    class Meta:
        ordering = ['gear_code']

    def get_absolute_url(self):
        return reverse('port:gear_list')


class MeshSize(models.Model):
    size_mm = models.IntegerField(null=True, verbose_name=_("size in mm"))
    size_inches = models.CharField(max_length=55, null=True, blank=True, verbose_name=_("size in inches"))
    size_inches_decimal = models.FloatField(null=True, blank=True, verbose_name=_("size in inches (decimal)"))

    def __str__(self):
        return "{} / {} mm".format(self.size_inches, self.size_mm)

    class Meta:
        ordering = ['size_mm']

    def get_absolute_url(self):
        return reverse('port:meshsize_list')


class Bait(SimpleLookup):
    pass


class Sample(MetadataFields):
    date = models.DateTimeField()
    species = models.ForeignKey(Species, related_name="samples", on_delete=models.DO_NOTHING, blank=True, null=True)
    sampler = models.ForeignKey(Sampler, related_name="samples", on_delete=models.DO_NOTHING, blank=True, null=True)
    ref_number = models.IntegerField(verbose_name="reference number", unique=True, null=True)
    port = models.ForeignKey(Port, related_name="samples", on_delete=models.DO_NOTHING, null=True, blank=True, )
    fishing_area = models.ForeignKey(FishingArea, related_name="samples", on_delete=models.DO_NOTHING, null=True, blank=True, )
    gear = models.ForeignKey(Gear, related_name="samples", on_delete=models.DO_NOTHING, null=True, blank=True, )
    mesh_size = models.ForeignKey(MeshSize, related_name="samples", on_delete=models.DO_NOTHING, null=True, blank=True)
    bait = models.ForeignKey(Bait, related_name="samples", on_delete=models.DO_NOTHING, null=True, blank=True)
    experimental_net_used = models.IntegerField(choices=YES_NO_CHOICES, null=True, blank=True)
    cfvn = models.IntegerField(null=True, blank=True, verbose_name=_("commercial fishing vessel number (CFVN)"))
    license_number = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("license number"))
    catch_weight_lbs = models.FloatField(null=True, blank=True, verbose_name="catch weight (lbs)")
    sample_weight_lbs = models.FloatField(null=True, blank=True, verbose_name="sample weight (lbs)")
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, editable=False, related_name='lengths_samples_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, editable=False, related_name='lengths_samples_updated_by')

    class Meta:
        ordering = ['-date', ]

    def get_absolute_url(self):
        return reverse('port:sample_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.species:
            return f"{self.species} (#{self.ref_number})"
        return f"#{self.ref_number}"

    @property
    def fish_measured(self):
        return self.fishies.count()

    @property
    def fish_kept(self):
        return self.fishies.filter(kept=True).count()


class Fish(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='fishies')
    length_bin_cm = models.FloatField()
    kept = models.BooleanField(default=False)

    class Meta:
        ordering = ('sample', 'length_bin_cm')
