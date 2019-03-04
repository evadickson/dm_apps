from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Sector(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Province(models.Model):
    # Choices for surface_type
    CAN = 'Canada'
    US = 'United States'
    COUNTRY_CHOICES = (
        (CAN, 'Canada'),
        (US, 'United States'),
    )
    name_eng = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("Name (English)"))
    name_fre = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("Name (French)"))
    country = models.CharField(max_length=25, choices=COUNTRY_CHOICES, verbose_name=_("country"))
    abbrev_eng = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("abbreviation (English)"))
    abbrev_fre = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("abbreviation (French)"))

    def __str__(self):
        return "{}".format(getattr(self, str(_("name_eng"))))


class Grouping(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name (English)"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Name (French)"))
    is_indigenous = models.BooleanField(default=False, verbose_name=_("indigenous?"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):
            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Person(models.Model):
    # Choices for language
    ENG = 1
    FRE = 2
    BI = 3
    LANGUAGE_CHOICES = (
        (ENG, _("English")),
        (FRE, _("French")),
        (BI, _("Bilingual")),
    )
    designation = models.CharField(max_length=25, verbose_name=_("designation"), blank=True, null=True)
    first_name = models.CharField(max_length=100, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, verbose_name=_("last name"), blank=True, null=True)
    phone_1 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("phone 1"))
    phone_2 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("phone 2"))
    email_1 = models.EmailField(blank=True, null=True, verbose_name=_("email 1"))
    email_2 = models.EmailField(blank=True, null=True, verbose_name=_("email 2"))
    cell = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("phone 2"))
    fax = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("fax"))
    language = models.IntegerField(choices=LANGUAGE_CHOICES, blank=True, null=True, verbose_name=_("language preference"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("notes"))

    # metadata
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"),
                                         related_name="masterlist_person_last_modified_by")

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('masterlist:person_detail', kwargs={'pk': self.pk})

    @property
    def contact_card(self):
        my_str = "<b>{first} {last}</b>".format(first=self.first_name, last=self.last_name)
        if self.phone_1:
            my_str += "<br>{}: {}".format(_("Phone 1"), self.phone_1)
        if self.phone_2:
            my_str += "<br>{}: {}".format(_("Phone 2"), self.phone_2)
        if self.fax:
            my_str += "<br>{}: {}".format(_("Fax"), self.fax)
        if self.email_1:
            my_str += "<br>{}: {}".format(_("E-mail 1"), self.email_1)
        if self.email_2:
            my_str += "<br>{}: {}".format(_("E-mail 2"), self.email_2)
        return my_str

    @property
    def contact_card_no_name(self):
        my_str = ""
        if self.phone_1:
            my_str += "<br>{}: {}".format(_("Phone 1"), self.phone_1)
        if self.phone_2:
            my_str += "<br>{}: {}".format(_("Phone 2"), self.phone_2)
        if self.fax:
            my_str += "<br>{}: {}".format(_("Fax"), self.fax)
        if self.email_1:
            my_str += "<br>{}: {}".format(_("E-mail 1"), self.email_1)
        if self.email_2:
            my_str += "<br>{}: {}".format(_("E-mail 2"), self.email_2)
        return my_str


class Organization(models.Model):
    name_eng = models.CharField(max_length=1000, verbose_name=_("english Name"))
    name_fre = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("french Name"))
    name_ind = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("indigenous Name"))
    abbrev = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("abbreviation"))
    address = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("address"))
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("city"))
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("postal code"))
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("province"))
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("phone"))
    fax = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("fax"))
    dfo_contact_instructions = models.TextField(blank=True, null=True, verbose_name=_("dfo contact instructions"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("notes"))
    key_species = models.TextField(blank=True, null=True, verbose_name=_("key species"))
    grouping = models.ManyToManyField(Grouping, verbose_name=_("grouping"), blank=True)
    regions = models.ManyToManyField(Region, verbose_name=_("region"), blank=True)
    sectors = models.ManyToManyField(Sector, verbose_name=_("DFO sector"), blank=True)

    # ihub only
    next_election = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("next election"))
    election_term = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("election term"))
    population_on_reserve = models.IntegerField(blank=True, null=True, verbose_name=_("population on reserve"))
    population_off_reserve = models.IntegerField(blank=True, null=True, verbose_name=_("population off reserve"))
    population_other_reserve = models.IntegerField(blank=True, null=True, verbose_name=_("population on other reserve"))
    fin = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("FIN"))

    # metadata
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name_eng"))):
            return "{}".format(getattr(self, str(_("name_eng"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name_eng)

    class Meta:
        ordering = ['name_eng']

    @property
    def full_address(self):
        # initial my_str with either address or None
        if self.address:
            my_str = self.address
        else:
            my_str = ""
        # add city
        if self.city:
            if my_str:
                my_str += ", "
            my_str += self.city
        # add province abbrev.
        if self.province:
            if my_str:
                my_str += ", "
            my_str += self.province.abbrev_eng
        # add postal code
        if self.postal_code:
            if my_str:
                my_str += ", "
            my_str += self.postal_code
        return my_str

    def get_absolute_url(self):
        return reverse('masterlist:org_detail', kwargs={'pk': self.pk})


class OrganizationMember(models.Model):
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("role"))
    notes = models.TextField(blank=True, null=True)

    # metadata
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["organization", "person"]
        unique_together = ["organization", "person"]

    def __str__(self):

        if self.person.first_name:
            first_name = self.person.first_name + " "
        else:
            first_name = ""

        if self.person.last_name:
            last_name = self.person.last_name
        else:
            last_name = ""


        return "{} {}, {} ({})".format(first_name, last_name, self.role, self.organization)


class ConsultationInstruction(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name="consultation_instructions")
    letter_to = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("address letter to:"))
    letter_cc = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("include on cc (letter)"))
    paper_copy = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("paper copy to"))
    notes = models.TextField(blank=True, null=True)
    # metadata
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def get_absolute_url(self):
        return reverse('masterlist:org_detail', kwargs={'pk': self.organization.pk})

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["organization", ]

    def __str__(self):
        return "Consultation Instructions for {}".format(self.organization)


class ConsultationInstructionRecipient(models.Model):
    TO = 1
    CC = 2
    TO_CC_CHOICES = (
        (TO, _("TO")),
        (CC, _("CC")),
    )
    consultation_instruction = models.ForeignKey(ConsultationInstruction, on_delete=models.CASCADE, related_name="recipients")
    member = models.ForeignKey(OrganizationMember, on_delete=models.DO_NOTHING, related_name="consultation_instructions")
    to_cc = models.IntegerField(choices=TO_CC_CHOICES, verbose_name=_("TO / CC"))
    # metadata
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name=_("date last modified"))
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("last modified by"))

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["to_cc", "member"]
        unique_together = ["consultation_instruction", "member"]

    def __str__(self):
        if self.member.person.designation:
            designation = self.member.person.designation + " "
        else:
            designation = ""

        if self.member.person.first_name:
            first_name = self.member.person.first_name + " "
        else:
            first_name = ""

        if self.member.person.last_name:
            last_name = self.member.person.last_name
        else:
            last_name = ""

        if self.member.person.email_1:
            email = self.member.person.email_1
        else:
            email = _("EMAIL MISSING")

        if self.member.role:
            role = self.member.role
        else:
            role = _("MISSING ROLE")

        return "{}: {}{}{} - {} [{}]".format(self.get_to_cc_display(), designation, first_name, last_name, role, email)