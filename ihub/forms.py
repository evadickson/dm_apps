from django import forms
from django.forms import modelformset_factory

from . import models
from django.contrib.auth.models import User


class EntryCreateForm(forms.ModelForm):
    class Meta:
        model = models.Entry
        exclude = [
            'date_last_modified',
            'date_created',
        ]
        widgets = {
            'initial_date': forms.DateInput(attrs={"type": "date"}),
            'last_modified_by': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),
        }


class EntryForm(forms.ModelForm):
    class Meta:
        model = models.Entry
        exclude = [
            'date_last_modified',
            'date_created',
            'created_by',
        ]
        widgets = {
            'initial_date': forms.DateInput(attrs={"type": "date"}),
            'last_modified_by': forms.HiddenInput(),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = models.EntryNote
        fields = "__all__"
        widgets = {
            'entry': forms.HiddenInput(),
            'author': forms.HiddenInput(),
        }


class ReportSearchForm(forms.Form):
    # FY_CHOICES = [
    #     ("{}".format(y["fiscal_year"]), "{}".format(y["fiscal_year"])) for y in
    #     models.Entry.objects.all().values("fiscal_year").order_by("fiscal_year").distinct() if y is not None]
    # FY_CHOICES.insert(0, (None, "all years"))
    # ORG_CHOICES = [(obj.id, obj) for obj in models.Organization.objects.all()]
    # # ORG_CHOICES = [(None, "---"), ]
    # REPORT_CHOICES = (
    #     (None, "------"),
    #     (1, "Capacity Report (Excel Spreadsheet)"),
    #     (2, "Organizational Report / Cue Card (PDF)"),
    # )
    #
    # report = forms.ChoiceField(required=True, choices=REPORT_CHOICES)
    # fiscal_year = forms.ChoiceField(required=False, choices=FY_CHOICES, label='Fiscal year')
    # organizations = forms.MultipleChoiceField(required=False, choices=ORG_CHOICES,
    #                                           label='Organizations (Leave blank for all)')
    # single_org = forms.ChoiceField(required=False, choices=ORG_CHOICES,
    #                                           label='Organization')
    pass

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = "__all__"


class PersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = "__all__"


class EntryPersonForm(forms.ModelForm):
    # save_then_go_OT = forms.CharField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = models.EntryPerson
        fields = "__all__"
        labels = {
            "user": "DFO employee",
        }
        widgets = {
            'entry': forms.HiddenInput(),
            # 'overtime_description': forms.Textarea(attrs={"rows": 5}),
            # 'user': forms.Select(choices=USER_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        USER_CHOICES = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        User.objects.all().order_by("last_name", "first_name")]
        USER_CHOICES.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all().order_by("last_name", "first_name")
        self.fields['user'].choices = USER_CHOICES


class MemberForm(forms.ModelForm):
    # save_then_go_OT = forms.CharField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = models.OrganizationMember
        fields = "__all__"
        widgets = {
            'organization': forms.HiddenInput(),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        fields = "__all__"
        widgets = {
            'entry': forms.HiddenInput(),
            'date_uploaded': forms.HiddenInput(),
        }


class SectorForm(forms.ModelForm):
    class Meta:
        model = models.Sector
        fields = "__all__"


SectorFormSet = modelformset_factory(
    model=models.Sector,
    form=SectorForm,
    extra=1,
)


class MemberRoleForm(forms.ModelForm):
    class Meta:
        model = models.MemberRole
        fields = "__all__"


MemberRoleFormSet = modelformset_factory(
    model=models.MemberRole,
    form=MemberRoleForm,
    extra=1,
)


class OrganizationFormShort(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = [
            'name_eng',
            'name_fre',
            'name_ind',
            'abbrev',
            'address',
            'city',
            'postal_code',
            'province',
            'phone',
            'fax',
            'next_election',
            'election_term',
            'population_on_reserve',
            'population_off_reserve',
            'population_other_reserve',
            'fin',
            'notes',
            'grouping',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={"rows": 2}),
        }


OrganizationFormSet = modelformset_factory(
    model=models.Organization,
    form=OrganizationFormShort,
    extra=1,
)


class StatusForm(forms.ModelForm):
    class Meta:
        model = models.Status
        fields = "__all__"


StatusFormSet = modelformset_factory(
    model=models.Status,
    form=StatusForm,
    extra=1,
)


class EntryTypeForm(forms.ModelForm):
    class Meta:
        model = models.EntryType
        fields = "__all__"


EntryTypeFormSet = modelformset_factory(
    model=models.EntryType,
    form=EntryTypeForm,
    extra=1,
)


class FundingPurposeForm(forms.ModelForm):
    class Meta:
        model = models.FundingPurpose
        fields = "__all__"


FundingPurposeFormSet = modelformset_factory(
    model=models.FundingPurpose,
    form=FundingPurposeForm,
    extra=1,
)


class RegionForm(forms.ModelForm):
    class Meta:
        model = models.Region
        fields = "__all__"


RegionFormSet = modelformset_factory(
    model=models.Region,
    form=RegionForm,
    extra=1,
)


class GroupingForm(forms.ModelForm):
    class Meta:
        model = models.Grouping
        fields = "__all__"


GroupingFormSet = modelformset_factory(
    model=models.Grouping,
    form=GroupingForm,
    extra=1,
)
