from django import forms
from django.forms import modelformset_factory
from django.template.defaultfilters import date
from django.utils.translation import gettext

from . import models

attr_fp_date_time = {"class": "fp-date-time-with-seconds", "placeholder": "Select Date and Time.."}
chosen_js = {"class": "chosen-select-contains"}
YES_NO_CHOICES = (
    (True, "Yes"),
    (False, "No"),
)


class DiverForm(forms.ModelForm):
    class Meta:
        model = models.Diver
        fields = "__all__"


DiverFormset = modelformset_factory(
    model=models.Diver,
    form=DiverForm,
    extra=1,
)


class RegionForm(forms.ModelForm):
    class Meta:
        model = models.Region
        fields = "__all__"


class SiteForm(forms.ModelForm):
    field_order = ["name"]

    class Meta:
        model = models.Site
        fields = "__all__"


class TransectForm(forms.ModelForm):
    field_order = ["name"]

    class Meta:
        model = models.Transect
        fields = "__all__"


class SampleForm(forms.ModelForm):
    class Meta:
        model = models.Sample
        fields = "__all__"
        widgets = {
            "datetime": forms.DateInput(attrs=dict(type="date")),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        site_choices = [(site.id, f"{site.region} - {site}") for site in models.Site.objects.order_by("region", "name")]
        site_choices.insert(0, (None, "---------"))

        self.fields["site"].choices = site_choices


class DiveForm(forms.ModelForm):
    # field_order = ["name"]
    class Meta:
        model = models.Dive
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("instance"):
            self.fields["transect"].queryset = kwargs.get("instance").sample.site.transects.all()
        elif kwargs.get("initial"):
            self.fields["transect"].queryset = models.Sample.objects.get(pk=kwargs.get("initial").get("sample")).site.transects.all()

        self.fields["start_descent"].label += " (yyyy-mm-dd HH:MM:SS)"

    def clean(self):
        if hasattr(self.instance, "sample"):
            sample = self.instance.sample
        else:
            sample = models.Sample.objects.get(pk=self.initial.get("sample"))

        cleaned_data = super().clean()

        start_descent = cleaned_data.get("start_descent")

        if start_descent and (start_descent.year != sample.datetime.year or
                              start_descent.month != sample.datetime.month or
                              start_descent.day != sample.datetime.day):
            msg = gettext(gettext('This must occur on the same day as the sample: {}').format(date(sample.datetime)))
            self.add_error('start_descent', msg)


class SectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        fields = "__all__"
        exclude = ["dive"]
        widgets = {
            "comment": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["interval"].widget.attrs = {"v-model": "sectionToEdit.interval", "ref": "top_of_form", "@change": "unsavedSectionWork=true", ":disabled":"sectionToEdit.id"}
        self.fields["depth_ft"].widget.attrs = {"v-model": "sectionToEdit.depth_ft", "min": 0, "@change": "unsavedSectionWork=true", "step": "0.01"}
        self.fields["percent_sand"].widget.attrs = {"v-model": "sectionToEdit.percent_sand", "max": 1, "min": 0, "@change": "unsavedSectionWork=true", "step": "0.01"}
        self.fields["percent_mud"].widget.attrs = {"v-model": "sectionToEdit.percent_mud", "max": 1, "min": 0, "@change": "unsavedSectionWork=true", "step": "0.01"}
        self.fields["percent_hard"].widget.attrs = {"v-model": "sectionToEdit.percent_hard", "max": 1, "min": 0, "@change": "unsavedSectionWork=true", "step": "0.01"}
        self.fields["percent_algae"].widget.attrs = {"v-model": "sectionToEdit.percent_algae", "max": 1, "min": 0, "@change": "unsavedSectionWork=true", "step": "0.01"}
        self.fields["percent_gravel"].widget.attrs = {"v-model": "sectionToEdit.percent_gravel", "max": 1, "min": 0, "@change": "unsavedSectionWork=true", "step": "0.01"}
        self.fields["percent_cobble"].widget.attrs = {"v-model": "sectionToEdit.percent_cobble", "max": 1, "min": 0, "@change": "unsavedSectionWork=true", "step": "0.01"}
        self.fields["percent_pebble"].widget.attrs = {"v-model": "sectionToEdit.percent_pebble", "max": 1, "min": 0, "@change": "unsavedSectionWork=true", "step": "0.01"}
        self.fields["comment"].widget.attrs = {"v-model": "sectionToEdit.comment", "@change": "unsavedSectionWork=true"}
