# from django.db import models

# Create your models here.
from datetime import datetime, timedelta, time
import decimal
import os
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q, Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from shapely.geometry import Point, box, LineString

from bio_diversity import utils, calculation_constants
from bio_diversity.utils import naive_to_aware
from shared_models import models as shared_models
from django.db import models
from django.utils.translation import gettext_lazy as _
YES_NO_CHOICES = (
        (True, _("Yes")),
        (False, _("No")),
    )


class BioModel(models.Model):
    # normal model with created by and created date fields
    class Meta:
        abstract = True

    created_by = models.CharField(max_length=32, verbose_name=_("Created By"))
    created_date = models.DateField(verbose_name=_("Created Date"))

    # to handle unresolved attirbute reference in pycharm
    objects = models.Manager()

    def clean(self, *args, **kwargs):
        # handle null values in uniqueness constraint foreign keys.
        # eg. should only be allowed one instance of a=5, b=null
        super(BioModel, self).clean()
        self.clean_fields()
        if self._meta.unique_together:
            uniqueness_constraints = [constraint for constraint in self._meta.unique_together]
            for constraint in uniqueness_constraints:
                # from stackoverflow
                unique_filter = {}
                unique_fields = []
                null_found = False
                for field_name in constraint:
                    field_value = getattr(self, field_name)
                    if getattr(self, field_name) is None:
                        unique_filter['%s__isnull' % field_name] = True
                        null_found = True
                    else:
                        unique_filter['%s' % field_name] = field_value
                        unique_fields.append(field_name)
                if null_found:
                    unique_queryset = self.__class__.objects.filter(**unique_filter)
                    if self.pk:
                        unique_queryset = unique_queryset.exclude(pk=self.pk)
                    if unique_queryset.exists():
                        msg = self.unique_error_message(self.__class__, tuple(unique_fields))
                        raise ValidationError(msg, code="unique_together")


class BioContainerDet(BioModel):
    class Meta:
        abstract = True

    contdc_id = models.ForeignKey("ContainerDetCode", on_delete=models.CASCADE,
                                  verbose_name=_("Container Detail Code"), db_column="CONT_DET_ID")
    det_value = models.DecimalField(max_digits=11, decimal_places=5, null=True, blank=True, verbose_name=_("Value"), db_column="VAL")
    cdsc_id = models.ForeignKey("ContDetSubjCode", on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name=_("Container Detail Subjective Code"), db_column="CONT_DET_SUBJ_ID")
    start_date = models.DateField(verbose_name=_("Date detail was recorded"), db_column="DET_START")
    end_date = models.DateField(null=True, blank=True, verbose_name=_("Last Date Detail is valid"), db_column="DET_END")
    det_valid = models.BooleanField(default="False", verbose_name=_("Detail still valid?"), db_column="STILL_VALID")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def clean(self):
        super(BioContainerDet, self).clean()
        if self.det_value > self.contdc_id.max_val or self.det_value < self.contdc_id.min_val:
            raise ValidationError({
                "det_value": ValidationError("Value {} exceeds limits. Max: {}, Min: {}".format(self.det_value,
                                                                                                self.contdc_id.max_val,
                                                                                                self.contdc_id.min_val))
            })


class BioDateModel(BioModel):
    # model with start date/end date, still valid, created by and created date fields
    class Meta:
        abstract = True

    start_date = models.DateField(verbose_name=_("Start Date"), db_column="START")
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"), db_column="END")
    valid = models.BooleanField(default="True", verbose_name=_("Detail still valid?"), db_column="STILL_VALID")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")


class BioDet(BioModel):
    class Meta:
        abstract = True
    det_val = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Value"), db_column="VAL")
    qual_id = models.ForeignKey('QualCode', on_delete=models.CASCADE, verbose_name=_("Quality"), db_column="QUAL_ID")
    detail_date = models.DateField(verbose_name=_("Date detail was recorded"), db_column="DETAIL_DATE")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")
    anidc_id = models.ForeignKey('AnimalDetCode', on_delete=models.CASCADE, verbose_name=_("Animal Detail Code"),
                                 db_column="ANI_DET_ID")
    adsc_id = models.ForeignKey('AniDetSubjCode', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name=_("Animal Detail Subjective Code"), db_column="ANI_DET_SUBJ_ID")

    def clean(self):
        super(BioDet, self).clean()
        if self.is_numeric() and self.det_val is not None:
            if float(self.det_val) > self.anidc_id.max_val or float(self.det_val) < self.anidc_id.min_val:
                raise ValidationError({
                    "det_val": ValidationError("Value {} exceeds limits. Max: {}, Min: {}"
                                               .format(self.det_val, self.anidc_id.max_val, self.anidc_id.min_val))
                })

    def is_numeric(self):
        if self.anidc_id.min_val is not None and self.anidc_id.max_val is not None:
            return True
        else:
            return False


class BioLookup(shared_models.Lookup):
    class Meta:
        abstract = True
        ordering = ['name']

    created_by = models.CharField(max_length=32, verbose_name=_("Created By"))
    created_date = models.DateField(verbose_name=_("Created Date"))

    # to handle unresolved attirbute reference in pycharm
    objects = models.Manager()

    def clean(self):
        # handle null values in uniqueness constraint foreign keys.
        # eg. should only be allowed one instance of a=5, b=null
        super(BioLookup, self).clean()
        if self._meta.unique_together:
            uniqueness_constraints = [constraint for constraint in self._meta.unique_together]
            for constraint in uniqueness_constraints:
                # from stackoverflow
                unique_filter = {}
                unique_fields = []
                null_found = False
                for field_name in constraint:
                    field_value = getattr(self, field_name)
                    if getattr(self, field_name) is None:
                        unique_filter['%s__isnull' % field_name] = True
                        null_found = True
                    else:
                        unique_filter['%s' % field_name] = field_value
                        unique_fields.append(field_name)
                if null_found:
                    unique_queryset = self.__class__.objects.filter(**unique_filter)
                    if self.pk:
                        unique_queryset = unique_queryset.exclude(pk=self.pk)
                    if unique_queryset.exists():
                        msg = self.unique_error_message(self.__class__, tuple(unique_fields))
                        raise ValidationError(msg, code="unique_together")


class BioTimeModel(BioModel):
    # model with start datetime/end datetime, created by and created date fields
    class Meta:
        abstract = True

    start_datetime = models.DateTimeField(verbose_name=_("Start date"), db_column="START")
    end_datetime = models.DateTimeField(null=True, blank=True, verbose_name=_("End date"), db_column="END")

    @property
    def start_date(self):
        return self.start_datetime.date()

    @property
    def start_time(self):
        if self.start_datetime.time() == time(0, 0):
            return None
        return self.start_datetime.time().strftime("%H:%M")

    @property
    def end_date(self):
        if self.end_datetime:
            return self.end_datetime.date()
        else:
            return None

    @property
    def end_time(self):
        if self.end_datetime:
            if self.end_datetime.time() == time(0, 0):
                return None
            return self.end_datetime.time().strftime("%H:%M")
        else:
            return None


class BioCont(BioLookup):
    # cont tag
    key = None

    class Meta:
        abstract = True

    # Make name not unique, is unique together with facility code.
    name = models.CharField(max_length=255, verbose_name=_("name (en)"), db_column="NAME")

    def fish_in_cont(self, at_date=None, select_fields=None, get_grp=False, valid_only=True):
        indv_list = []
        grp_list = []

        if not select_fields:
            select_fields = []

        if not at_date:
            at_date = timezone.now().date()

        filter_in_arg = "contx_end__{}_id".format(self.key)
        filter_out_arg = "contx_start__{}_id".format(self.key)

        move_in_set = MoveDet.objects.filter(**{filter_in_arg: self},
                                             move_date__lte=at_date, ).order_by("move_date")\
            .select_related("anix_id__indv_id", "anix_id__grp_id", *select_fields)

        move_out_set = MoveDet.objects.filter(**{filter_out_arg: self},
                                              move_date__lte=at_date).order_by("move_date").\
            select_related("anix_id__indv_id", "anix_id__grp_id", *select_fields)

        # These dicts can only hold each group/indv once, the order by method on the queryset ensures that the entry
        # has the latest date
        indv_in_dict = {move_det.anix_id.indv_id: move_det.move_date for move_det in move_in_set if move_det.anix_id.indv_id}
        indv_out_dict = {move_det.anix_id.indv_id: move_det.move_date for move_det in move_out_set if move_det.anix_id.indv_id}
        grp_in_dict = {move_det.anix_id.grp_id: move_det.move_date for move_det in move_in_set if move_det.anix_id.grp_id}
        grp_out_dict = {move_det.anix_id.grp_id: move_det.move_date for move_det in move_out_set if move_det.anix_id.grp_id}

        for indv in indv_in_dict.keys():
            if indv.indv_valid or not valid_only:
                if indv not in indv_out_dict.keys():
                    indv_list.append(indv)
                elif indv_in_dict[indv] > indv_out_dict[indv]:
                    indv_list.append(indv)
        for grp in grp_in_dict.keys():
            if (grp.grp_valid or not valid_only) and not grp.past_end_date(at_date):
                if grp not in grp_out_dict.keys():
                    grp_list.append(grp)
                elif grp_in_dict[grp] > grp_out_dict[grp]:
                    grp_list.append(grp)
        if get_grp:
            return grp_list
        else:
            return indv_list, grp_list

    def fish_count(self, at_date=None):
        if not at_date:
            at_date = timezone.now()
        indv_list, grp_list = self.fish_in_cont(at_date=at_date)
        cont_count = len(indv_list)
        for grp in grp_list:
            cont_count += grp.count_fish_in_group(at_date=at_date)
        return cont_count

    def degree_days(self, start_date, end_date):
        return []

    def cont_feed(self, at_date=None, get_string=False):
        if not at_date:
            at_date = timezone.now()
        feed_contx = self.contxs.filter(evnt_id__evntc_id__name="Feeding", evnt_id__start_datetime__lte=at_date).order_by("-evnt_id__start_datetime").first()
        if get_string:
            if feed_contx:
                cont_feed = feed_contx.feed_str
                return cont_feed
            else:
                return ""
        else:
            return feed_contx

    def feed_history(self, start_date=None, end_date=None):

        if not start_date:
            start_date = utils.aware_min()

        if not end_date:
            end_date = timezone.now()

        oldest_contx = self.cont_feed(at_date=start_date)
        feed_contx = self.contxs.filter(evnt_id__evntc_id__name="Feeding", evnt_id__start_datetime__gte=start_date,
                                        evnt_id__start_datetime__lte=end_date).order_by("-evnt_id__start_datetime")
        contx_list = [contx for contx in feed_contx]
        if oldest_contx:
            contx_list.append(oldest_contx)
        return contx_list

    def cont_treatments(self, start_date=None, end_date=None):
        if not start_date:
            start_date = utils.aware_min()

        if not end_date:
            end_date = timezone.now()

        filter_arg = "contx_id__{}_id".format(self.key)
        envt_qs = EnvTreatment.objects.filter(**{filter_arg: self}, start_datetime__gte=start_date,
                                              start_datetime__lte=end_date)
        return envt_qs


class BioUser(models.Model):
    mode_choices = (
        (1, "read"),
        (2, "edit"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="bio_user", verbose_name=_("DM Apps user"))

    # admins can modify helptext and other app settings
    is_admin = models.BooleanField(default=False, verbose_name=_("app administrator"), choices=YES_NO_CHOICES)

    # authors can create/modify/delete records
    is_author = models.BooleanField(default=False, verbose_name=_("app author"), choices=YES_NO_CHOICES)

    # users can view, but not modify records
    is_user = models.BooleanField(default=False, verbose_name=_("app user"), choices=YES_NO_CHOICES)

    facic_id = models.ForeignKey("FacilityCode", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Facility"))

    # admin users can toggle helptext edit mode on and off
    mode = models.IntegerField(choices=mode_choices, default=1)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        ordering = ["-is_admin", "user__first_name", ]


class AnimalDetCode(BioLookup):
    # anidc tag
    min_val = models.DecimalField(max_digits=11, decimal_places=5, blank=True, null=True, verbose_name=_("Minimum Value"), db_column="MIN_VAL")
    max_val = models.DecimalField(max_digits=11, decimal_places=5, blank=True, null=True, verbose_name=_("Maximum Value"), db_column="MAX_VAL")
    unit_id = models.ForeignKey("UnitCode", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Units"), db_column="UNIT_ID")
    ani_subj_flag = models.BooleanField(verbose_name=_("Subjective?"), db_column="ANI_SUBJ_FLAG")

    def __str__(self):
        return "{} ({})".format(self.name, self.unit_id.__str__())

    class Meta:
        ordering = ['name', ]


class AniDetSubjCode(BioLookup):
    # adsc tag
    anidc_id = models.ForeignKey("AnimalDetCode", on_delete=models.CASCADE, verbose_name=_("Type of measurement"), db_column="ANI_DET_ID")


class AniDetailXref(BioModel):
    # anix tag
    evnt_id = models.ForeignKey("Event", on_delete=models.CASCADE, verbose_name=_("Event"), db_column="EVENT_ID",
                                related_name="animal_details")
    contx_id = models.ForeignKey("ContainerXRef", on_delete=models.CASCADE, null=True, blank=True, related_name="animal_details",
                                 verbose_name=_("Container Cross Reference"), db_column="CONTAINER_XREF_ID")
    loc_id = models.ForeignKey("Location", on_delete=models.CASCADE, null=True, blank=True, db_column="LOCATION_ID",
                               related_name="animal_details", verbose_name=_("Location"))
    indv_id = models.ForeignKey("Individual", on_delete=models.CASCADE, null=True, blank=True, db_column="INDIV_ID",
                                related_name="animal_details", verbose_name=_("Individual"))
    pair_id = models.ForeignKey("Pairing", on_delete=models.CASCADE, null=True, blank=True, related_name="animal_details",
                                verbose_name=_("Pairing"), db_column="PAIR_ID")
    grp_id = models.ForeignKey("Group", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Group"),
                               related_name="animal_details", db_column="GROUP_ID")
    team_id = models.ForeignKey("TeamXRef", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Team"),
                                related_name="animal_details", db_column="TEAM_ID")

    class Meta:
        unique_together = (('evnt_id', 'contx_id', 'loc_id', 'indv_id', 'pair_id', 'grp_id', 'team_id'),)

    def clean(self):
        super(AniDetailXref, self).clean()
        if not (self.contx_id or self.loc_id or self.indv_id or self.pair_id or self.grp_id):
            raise ValidationError("You must specify at least one item to reference to the event")

    def __str__(self):
        return "Ani X Ref for {}".format(self.evnt_id.__str__())


class Collection(BioLookup):
    # coll tag
    pass


# This is a special table used to house comment parsing abilities
class CommentKeywords(models.Model):
    # coke tag
    keyword = models.CharField(max_length=255)
    adsc_id = models.ForeignKey('AniDetSubjCode', on_delete=models.CASCADE, verbose_name=_("Animal Detail Subjective Code"))

    class Meta:
        ordering = ['keyword', ]


class ContainerDetCode(BioLookup):
    # contdc tag
    min_val = models.DecimalField(max_digits=11, decimal_places=5, verbose_name=_("Minimum Value"), db_column="MIN_VAL")
    max_val = models.DecimalField(max_digits=11, decimal_places=5, verbose_name=_("Maximum Value"), db_column="MAX_VAL")
    unit_id = models.ForeignKey("UnitCode", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Units"), db_column="UNIT_ID")
    cont_subj_flag = models.BooleanField(verbose_name=_("Subjective detail?"), db_column="CONT_SUBJ_FLAG")


class ContDetSubjCode(BioLookup):
    # cdsc tag
    contdc_id = models.ForeignKey("ContainerDetCode", on_delete=models.CASCADE, db_column="CONT_DET_ID",
                                  verbose_name=_("Container detail code"))

    class Meta:
        unique_together = (('name', 'contdc_id'),)


class ContainerXRef(BioModel):
    # contx tag
    evnt_id = models.ForeignKey("Event", on_delete=models.CASCADE, verbose_name=_("Event"), db_column="EVENT_ID",
                                related_name="containers")
    tank_id = models.ForeignKey("Tank", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Tank"),
                                related_name="contxs", db_column="TANK_ID")
    trof_id = models.ForeignKey("Trough", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Trough"),
                                related_name="contxs", db_column="TROUGH_ID")
    tray_id = models.ForeignKey("Tray", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Tray"),
                                related_name="contxs", db_column="TRAY_ID")
    heat_id = models.ForeignKey("HeathUnit", on_delete=models.CASCADE, null=True, blank=True, db_column="HEATH_UNIT_ID",
                                verbose_name=_("Heath Unit"), related_name="contxs")
    draw_id = models.ForeignKey("Drawer", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Drawer"),
                                related_name="contxs", db_column="DRAWER_ID")
    cup_id = models.ForeignKey("Cup", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Cup"),
                               related_name="contxs", db_column="CUP_ID")
    team_id = models.ForeignKey("TeamXRef", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Team"),
                                related_name="contxs", db_column="TEAM_ID")

    class Meta:
        unique_together = (('evnt_id', 'tank_id', 'trof_id', 'tray_id', 'heat_id', 'draw_id', 'cup_id', 'team_id'),)

    def __str__(self):
        return "{}-{}".format(self.evnt_id.__str__(), self.container)

    def clean(self):
        super(ContainerXRef, self).clean()
        if not (self.tank_id or self.tray_id or self.trof_id or self.heat_id or self.draw_id or self.cup_id):
            raise ValidationError("You must specify at least one container to reference to the event")

    @property
    def container(self):
        cnt = 0
        cont = None
        for cont_id in [self.cup_id, self.draw_id, self.tray_id, self.tank_id, self.trof_id, self.heat_id]:
            if cont_id:
                cont = cont_id
                cnt += 1
        if cnt == 1:
            return cont
        else:
            return None

    @property
    def feed_str(self):
        cont_feed = self.feeding_set.select_related("feedc_id", "feedm_id").all()
        feed_str = ""
        for feed in cont_feed:
            feed_str += "{} #{}, ".format(feed.feedc_id.name, feed.amt)
        return feed_str

    @property
    def feed_props(self):
        feed_dict = {"str": "", "freq": "", "method": "", "comments": ""}
        cont_feed = self.feeding_set.select_related("feedc_id", "feedm_id").all()
        for feed in cont_feed:
            feed_dict["str"] += "{} #{}, ".format(feed.feedc_id.__str__(), feed.amt)
            feed_dict["freq"] += "{}, ".format(feed.freq)
            feed_dict["method"] += "{}, ".format(feed.feedm_id.__str__())
            if feed.comments:
                feed_dict["comments"] += "{} ".format(feed.comments)
        return feed_dict


class Count(BioModel):
    # cnt tag
    loc_id = models.ForeignKey("Location", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Location"),
                               related_name="counts", db_column="LOCATION_ID")
    anix_id = models.ForeignKey("AniDetailXref", on_delete=models.CASCADE, null=True, blank=True, related_name="counts",
                                 verbose_name=_("Animal Cross Reference"), db_column="ANI_DET_XREF_ID")
    contx_ref = models.ForeignKey("ContainerXRef", on_delete=models.CASCADE, null=True, blank=True, related_name="counts",
                                 verbose_name=_("Container Reference"), db_column="CONT_XREF_ID")
    cntc_id = models.ForeignKey("CountCode", on_delete=models.CASCADE, verbose_name=_("Count Code"), db_column="CNT_ID")
    spec_id = models.ForeignKey("SpeciesCode", on_delete=models.CASCADE, verbose_name=_("Species"), db_column="SPEC_ID")
    stok_id = models.ForeignKey('StockCode', on_delete=models.CASCADE, verbose_name=_("Stock Code"),
                                db_column="STOCK_ID", blank=True, null=True)
    cnt_year = models.IntegerField(verbose_name=_("Collection year"), default=None, db_column="YEAR",
                                   validators=[MinValueValidator(2000), MaxValueValidator(2100)], blank=True, null=True)
    coll_id = models.ForeignKey('Collection', on_delete=models.CASCADE, verbose_name=_("Collection"),
                                db_column="COLLECTION_ID", blank=True, null=True)
    cnt = models.DecimalField(max_digits=6, decimal_places=0, verbose_name=_("Count"), db_column="COUNT")
    cnt_date = models.DateField(verbose_name=_("Count Date"), default=datetime.min.date())
    est = models.BooleanField(verbose_name=_("Estimated?"), db_column="ESTIMATED")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    class Meta:
        unique_together = (('loc_id', 'anix_id', 'cntc_id', 'contx_ref', 'spec_id', 'cnt_year', 'coll_id', 'stok_id', 'cnt_date'),)

    def __str__(self):
        return "{}-{}-{}".format(self.loc_id.__str__(), self.spec_id.__str__(), self.cntc_id.__str__())

    def clean(self):
        if not self.loc_id and not self.anix_id:
            raise ValidationError("Animal Detail Xref and location cannot both be null.")
        super(Count, self).clean()

    @property
    def date(self):
        return self.cnt_date

    @property
    def contx_id(self):
        if self.anix_id:
            return self.anix_id.contx_id
        else:
            return None

    @property
    def coll_str(self):
        return "{} {}".format(self.cnt_year, self.coll_id.__str__())

    def prog_group(self, get_string=False):
        # gets program groups this group may be a part of.
        cntd_set = CountDet.objects.filter(cnt_id=self,
                                           anidc_id__name="Program Group",
                                           adsc_id__isnull=False,
                                           ).select_related("adsc_id")
        if get_string:
            prog_grp_list = [cntd.adsc_id.name for cntd in cntd_set]
            prog_str = ", ".join(prog_grp_list)
            return prog_str
        else:
            prog_grp_list = [cntd.adsc_id for cntd in cntd_set]
            return prog_grp_list

    def cnt_detail(self, anidc_name="Length"):
        cntd_id = CountDet.objects.filter(anidc_id__name__icontains=anidc_name, cnt_id=self).first()
        if cntd_id:
            return cntd_id.det_val
        else:
            return None


class CountCode(BioLookup):
    # cntc tag
    pass


class CountDet(BioDet):
    # cntd tag
    cnt_id = models.ForeignKey("Count", on_delete=models.CASCADE, verbose_name=_("Count"), related_name="count_details",
                               db_column="COUNT_ID")
    detail_date = None

    class Meta:
        unique_together = (('cnt_id', 'anidc_id', 'adsc_id'),)

    def __str__(self):
        return "{} - {}".format(self.cnt_id.__str__(), self.anidc_id.__str__())


class Cup(BioCont):
    # cup tag
    key = "cup"

    class Meta:
        unique_together = (('name', 'draw_id', 'start_date'),)
        ordering = ['draw_id', 'name']

    # Make name not unique, is unique together with drawer.
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    draw_id = models.ForeignKey('Drawer', on_delete=models.CASCADE, related_name="cups", verbose_name=_("Drawer"), db_column="DRAWER_ID")
    start_date = models.DateField(verbose_name=_("Start Date"), db_column="START_DATE")
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"), db_column="END_DATE")

    def __str__(self):
        return "HU {}.{}.{}".format(self.draw_id.heat_id.__str__(), self.draw_id.name, self.name)

    def dot_str(self):
        return "{}.{}.{}".format(self.draw_id.heat_id.name, self.draw_id.name, self.name)

    @property
    def facic_id(self):
        return self.draw_id.facic_id


class CupDet(BioContainerDet):
    # cupd tag
    cup_id = models.ForeignKey('Cup', on_delete=models.CASCADE, verbose_name=_("Cup"), db_column="CUP_ID")

    class Meta:
        unique_together = (('cup_id', 'contdc_id', 'cdsc_id', 'start_date'),)

    def __str__(self):
        return "{} - {}".format(self.cup_id.__str__(), self.contdc_id.__str__())


class DataLoader(BioModel):
    # data tag
    evnt_id = models.ForeignKey('Event', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Event"))
    evntc_id = models.ForeignKey('EventCode', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Data Format"))
    facic_id = models.ForeignKey('FacilityCode', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Data Format"))
    data_csv = models.FileField(upload_to="", null=True, blank=True, verbose_name=_("Datafile"))


class Drawer(BioCont):
    # draw tag
    key = "draw"

    class Meta:
        unique_together = (('name', 'heat_id'),)
        ordering = ['heat_id', 'name']

    # Make name not unique, is unique together with drawer.
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    heat_id = models.ForeignKey('HeathUnit', on_delete=models.CASCADE, related_name="draws",
                                verbose_name=_("Heath Unit"), db_column="HEATH_UNIT_ID")

    @property
    def facic_id(self):
        return self.heat_id.facic_id

    def __str__(self):
        return "HU {}.{}".format(self.heat_id.__str__(), self.name)

    def dot_str(self):
        return "{}.{}".format(self.heat_id.name, self.name)


class EnvCode(BioLookup):
    # envc tag
    min_val = models.DecimalField(max_digits=11, decimal_places=5, null=True, blank=True,
                                  verbose_name=_("Minimum Value"), db_column="MIN_VAL")
    max_val = models.DecimalField(max_digits=11, decimal_places=5, null=True, blank=True,
                                  verbose_name=_("Maximum Value"), db_column="MAX_VAL")
    unit_id = models.ForeignKey('UnitCode', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Units"),
                                db_column="UNIT_ID")
    env_subj_flag = models.BooleanField(verbose_name=_("Objective observation?"), db_column="ENV_SUBJ_FLAG")


class EnvCondition(BioTimeModel):
    # env tag
    contx_id = models.ForeignKey('ContainerXRef', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name="env_condition", verbose_name=_("Container Cross Reference"),
                                 db_column="CONTAINER_XREF_ID")
    loc_id = models.ForeignKey('Location', on_delete=models.CASCADE, null=True, blank=True, db_column="LOCATION_ID",
                               verbose_name=_("Location"), related_name="env_condition")
    inst_id = models.ForeignKey('Instrument', on_delete=models.CASCADE, null=True, blank=True, db_column="INSTRUM_ID",
                                verbose_name=_("Instrument"))
    envc_id = models.ForeignKey('EnvCode', on_delete=models.CASCADE, verbose_name=_("Environment variable"),
                                db_column="ENV_ID")
    env_val = models.DecimalField(max_digits=11, decimal_places=5, null=True, blank=True, verbose_name=_("Value"),
                                  db_column="VAL")
    envsc_id = models.ForeignKey('EnvSubjCode', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name=_("Environment Subjective Code"), db_column="ENV_SUBJ_ID")
    env_avg = models.BooleanField(default=False, verbose_name=_("Is value an average?"), db_column="AVERAGED")
    qual_id = models.ForeignKey('QualCode', on_delete=models.CASCADE, verbose_name=_("Quality of observation"),
                                db_column="QUAL_ID")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    class Meta:
        unique_together = (('contx_id', 'loc_id', 'inst_id', 'envc_id', 'envsc_id', 'start_datetime'),)

    def __str__(self):
        if self.contx_id:
            return "{}-{}".format(self.contx_id.__str__(), self.envc_id.__str__())
        elif self.loc_id:
            return "{}-{}".format(self.loc_id.__str__(), self.envc_id.__str__())
        else:
            return "{}-{}".format(self.envc_id.__str__(), self.start_date)

    def clean(self):
        super(EnvCondition, self).clean()
        if self.is_numeric() and self.env_val is not None:
            if float(self.env_val) > float(self.envc_id.max_val) or float(self.env_val) < float(self.envc_id.min_val):
                raise ValidationError({
                    "env_val": ValidationError("Value {} exceeds limits. Max: {}, Min: {}".format(self.env_val,
                                                                                                  self.envc_id.max_val,
                                                                                                  self.envc_id.min_val))
                })

    def is_numeric(self):
        if self.envc_id.min_val is not None and self.envc_id.max_val is not None:
            return True
        else:
            return False


def envcf_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/bio_diversity/env_conditions/<filename>
    return 'bio_diversity/env_conditions/{}'.format(filename)


class EnvCondFile(BioModel):
    # envcf tag
    env_id = models.OneToOneField("EnvCondition", on_delete=models.CASCADE, verbose_name=_("Environment Condition"),
                                  related_name="envcf_id", db_column="ENV_COND_ID")
    env_pdf = models.FileField(upload_to=envcf_directory_path, null=True, blank=True, db_column="RAW_FILE",
                               verbose_name=_("Environment Condition File"))
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def __str__(self):
        return "{}".format(self.env_pdf)

    class Meta:
        ordering = ['created_date']


@receiver(models.signals.post_delete, sender=EnvCondFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.env_pdf:
        if os.path.isfile(instance.env_pdf.path):
            os.remove(instance.env_pdf.path)


@receiver(models.signals.pre_save, sender=EnvCondFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = EnvCondFile.objects.get(pk=instance.pk).env_pdf
    except EnvCondFile.DoesNotExist:
        return False
    new_file = instance.env_pdf
    if old_file and not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class EnvSubjCode(BioLookup):
    # envsc tag
    envc_id = models.ForeignKey('EnvCode', null=True, blank=True, on_delete=models.CASCADE, db_column="ENV_ID",
                                verbose_name=_("Environment Code"))


class EnvTreatCode(BioLookup):
    # envtc tag
    rec_dose = models.CharField(max_length=400, blank=True, null=True, verbose_name=_("Recommended Dosage"),
                                db_column="ENV_REC_DOSAGE")
    manufacturer = models.CharField(max_length=50, verbose_name=_("Treatment Manufacturer"), db_column="MANUFACTURER")


class EnvTreatment(BioTimeModel):
    # envt tag
    contx_id = models.ForeignKey('ContainerXRef', on_delete=models.CASCADE, related_name="env_treatment",
                                 verbose_name=_("Container Cross Reference"), db_column="CONTAINER_XREF_ID")
    envtc_id = models.ForeignKey('EnvTreatCode', on_delete=models.CASCADE, db_column="ENV_TREAT_ID",
                                 verbose_name=_("Environment Treatment Code"))
    lot_num = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Lot Number"),
                               db_column="LOT_NUMBER")
    amt = models.DecimalField(max_digits=7, decimal_places=3, verbose_name=_("Dose"), db_column="AMOUNT")
    concentration = models.DecimalField(max_digits=8, decimal_places=7, null=True, blank=True,
                                        verbose_name=_("Concentration"), db_column="CONCENTRATION")
    unit_id = models.ForeignKey('UnitCode', on_delete=models.CASCADE, verbose_name=_("Units"), db_column="UNIT_ID")
    duration = models.DecimalField(max_digits=5, decimal_places=0, verbose_name=_("Duration (minutes)"),
                                   db_column="DURATION")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def __str__(self):
        return "{}-{}".format(self.contx_id.__str__(), self.envtc_id.__str__())

    class Meta:
        unique_together = (('contx_id', 'envtc_id', 'start_datetime'),)

    @property
    def cont(self):
        for cont_id in [self.contx_id.cup_id, self.contx_id.draw_id, self.contx_id.tray_id, self.contx_id.tank_id, self.contx_id.trof_id, self.contx_id.heat_id]:
            if cont_id:
                return cont_id
        return None

    @property
    def concentration_str(self):
        if self.concentration:
            return "1:{}  |  {:.3}%".format(int(decimal.Decimal(1.0)/self.concentration), decimal.Decimal(100) * self.concentration)
        else:
            return None
    concentration_str.fget.short_description = "Concentration"


class Event(BioTimeModel):
    # evnt tag
    facic_id = models.ForeignKey('FacilityCode', on_delete=models.CASCADE, verbose_name=_("Facility Code"), db_column="FAC_ID")
    evntc_id = models.ForeignKey('EventCode', on_delete=models.CASCADE, verbose_name=_("Event Code"), db_column="EVT_ID")
    perc_id = models.ForeignKey('PersonnelCode', on_delete=models.CASCADE, verbose_name=_("Personnel Code"),
                                limit_choices_to={'perc_valid': True}, db_column="PER_ID")
    prog_id = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name=_("Program"), db_column="PROGRAM_ID",
                                limit_choices_to={'valid': True})
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    @property
    def is_current(self):
        if self.evnt_end and self.evnt_end < datetime.now(tz=timezone.get_current_timezone()):
            return True
        elif not self.evnt_end:
            return True
        else:
            return False

    def __str__(self):
        return "{}-{}".format(self.evntc_id.__str__(), self.start_date)

    class Meta:
        unique_together = (('facic_id', 'evntc_id', 'prog_id', 'start_datetime', 'end_datetime'),)
        ordering = ['-start_datetime']

    def fecu_dict(self):
        fecu_dict = {}
        # the order by call is needed for distinct() to work as expected and return only a single object.
        stok_coll_set = Individual.objects.filter(animal_details__evnt_id=self).values("stok_id", "coll_id",
                                                                                       "stok_id__name",
                                                                                       "coll_id__name").distinct().order_by()
        for stok_coll in stok_coll_set:
            key = "Alpha, Beta for {}-{}".format(stok_coll["stok_id__name"], stok_coll["coll_id__name"])
            fecu_id = Fecundity.objects.filter(stok_id_id=stok_coll["stok_id"], coll_id_id=stok_coll["coll_id"]).first()
            value = ""
            if fecu_id:
                value = "{}, {}".format(fecu_id.alpha, fecu_id.beta)
            fecu_dict[key] = value

        return fecu_dict

    def delete(self, using=None, keep_parents=False):
        # nuke unused groups here:
        grp_qs = Group.objects.filter(animal_details__evnt_id=self).distinct()

        for grp_id in grp_qs:
            anix_set = grp_id.animal_details.filter(evnt_id__isnull=False)
            evnt_list = list(dict.fromkeys([anix.evnt_id for anix in anix_set]))
            if len(evnt_list) == 1:
                grp_id.delete()
        super(Event, self).delete()


@receiver(post_save, sender=Event)
def my_handler(sender, instance, **kwargs):
    utils.add_team_member(instance.perc_id, instance)


class EventCode(BioLookup):
    # evntc tag
    pass


def evntf_directory_path(instance, filename):
    return 'bio_diversity/event_files/{}'.format(filename)


def matp_directory_path(instance, filename):
    return 'bio_diversity/event_files/{}'.format(filename)


class EventFile(BioModel):
    # evntf tag
    evnt_id = models.ForeignKey('Event', on_delete=models.CASCADE, verbose_name=_("Event"), related_name="event_files",
                                db_column="EVENT_ID")
    evntfc_id = models.ForeignKey('EventFileCode', on_delete=models.CASCADE, verbose_name=_("Event File Code"),
                                  related_name="event_files", db_column="EVT_FILE_CODE_ID")
    evntf_xls = models.FileField(upload_to=evntf_directory_path, null=True, blank=True, verbose_name=_("Event File"),
                                 db_column="EVENT_FILE")
    stok_id = models.ForeignKey('StockCode', on_delete=models.CASCADE, blank=True, null=True, db_column="STOCK_ID",
                                verbose_name=_("Stock Code"), related_name="event_files")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    class Meta:
        unique_together = (("evnt_id", "stok_id"),)


@receiver(models.signals.post_delete, sender=EventFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.evntf_xls:
        if os.path.isfile(instance.evntf_xls.path):
            os.remove(instance.evntf_xls.path)


@receiver(models.signals.pre_save, sender=EventFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = EventFile.objects.get(pk=instance.pk).evntf_xls
    except EventFile.DoesNotExist:
        return False
    new_file = instance.evntf_xls
    if old_file and not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class EventFileCode(BioLookup):
    # evntfc tag
    pass


class FacilityCode(BioLookup):
    # facic tag
    pass


class Fecundity(BioDateModel):
    # fecu tag
    stok_id = models.ForeignKey('StockCode', on_delete=models.CASCADE, verbose_name=_("Stock Code"),
                                db_column="STOCK_ID")
    coll_id = models.ForeignKey('Collection', on_delete=models.CASCADE, null=True, blank=True, db_column="COLLECTION_ID",
                                verbose_name=_("Collection"))
    alpha = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_("A"), db_column="A")
    beta = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_("B"), db_column="B")

    class Meta:
        unique_together = (('stok_id', 'coll_id', 'start_date'),)

    def __str__(self):
        return "{}-{}-{}".format(self.stok_id.__str__(), self.alpha, self.beta)


class Feeding(BioModel):
    # feed tag
    contx_id = models.ForeignKey('ContainerXRef', on_delete=models.CASCADE, verbose_name=_("Container Cross Reference"),
                                 db_column="CONTAINER_XREF_ID")
    feedm_id = models.ForeignKey('FeedMethod', on_delete=models.CASCADE, verbose_name=_("Feeding Method"),
                                 db_column="FEEDMETHOD_ID")
    feedc_id = models.ForeignKey('FeedCode', on_delete=models.CASCADE, verbose_name=_("Feeding Code"),
                                 db_column="FEED_ID")
    lot_num = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("Lot Number"),
                               db_column="LOT_NUMBER")
    amt = models.DecimalField(max_digits=7, decimal_places=3, verbose_name=_("Amount of Feed"), db_column="AMOUNT")
    unit_id = models.ForeignKey('UnitCode', on_delete=models.CASCADE, verbose_name=_("Units"), db_column="UNIT_ID")
    freq = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("Description of frequency"),
                            db_column="FREQUENCY")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"),
                                db_column="COMMENTS")

    def __str__(self):
        return "{} {}".format(self.feedc_id.__str__(), self.amt)

    @property
    def feed_date(self):
        return self.contx_id.evnt_id.start_date

    class Meta:
        unique_together = (('contx_id', 'feedm_id', 'feedc_id', 'amt', 'unit_id'),)


class FeedCode(BioLookup):
    # feedc tag
    manufacturer = models.CharField(max_length=50, verbose_name=_("Maufacturer"), db_column="MANUFACTURER")


class FeedMethod(BioLookup):
    # feedm tag
    pass


class Group(BioModel):
    # grp tag
    spec_id = models.ForeignKey('SpeciesCode', on_delete=models.CASCADE, verbose_name=_("Species"), db_column="SPEC_ID")
    stok_id = models.ForeignKey('StockCode', on_delete=models.CASCADE, verbose_name=_("Stock Code"),
                                db_column="STOCK_ID")
    grp_year = models.IntegerField(verbose_name=_("Collection year"), default=2000, db_column="YEAR",
                                   validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    coll_id = models.ForeignKey('Collection', on_delete=models.CASCADE, verbose_name=_("Collection"),
                                db_column="COLLECTION_ID")
    grp_end_date = models.DateField(null=True, blank=True, verbose_name=_("Group end date"), db_column="GROUP_END_DATE")
    grp_valid = models.BooleanField(default="True", verbose_name=_("Group still valid?"), db_column="STILL_VALID")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTTS")

    def __str__(self):
        return "{}-{}-{}-{}".format(self.pk, self.stok_id.__str__(), self.grp_year, self.coll_id.__str__())

    def current_cont(self, at_date=None, valid_only=False, get_string=False):
        if not at_date:
            at_date = timezone.now().date()
        cont_list = []
        if not self.grp_valid and valid_only:
            if get_string:
                return ""
            return cont_list

        if self.grp_end_date:
            if self.grp_end_date < at_date:
                if get_string:
                    return ""
                return cont_list

        move_set = MoveDet.objects.filter(anix_id__grp_id=self, move_date__lte=at_date).order_by("move_date"). \
            select_related('contx_end', 'contx_start')

        # These dicts can only hold each group/indv once, the order by method on the queryset ensures that the entry
        # has the latest date
        cont_in_dict = {move_det.contx_end.container: move_det.move_date for move_det in move_set if
                       move_det.contx_end}
        cont_out_dict = {move_det.contx_start.container: move_det.move_date for move_det in move_set if
                       move_det.contx_start}

        for cont in cont_in_dict.keys():
            if cont not in cont_out_dict.keys() and cont:
                cont_list.append(cont)
            elif cont_in_dict[cont] > cont_out_dict[cont] and cont:
                cont_list.append(cont)

        if get_string:
            cont_str_list = [cont.__str__() for cont in cont_list]
            cont_str = ", ".join(cont_str_list)
            return cont_str
        return cont_list

    def get_cont_history(self, start_date=None, end_date=None, get_str=False):
        if not start_date:
            start_date = utils.aware_min()
        if not end_date:
            end_date = timezone.now()

        anix_evnt_set = AniDetailXref.objects.filter(grp_id=self, contx_id__isnull=False, loc_id__isnull=True,
                                                     pair_id__isnull=True, evnt_id__start_datetime__lte=end_date,
                                                     evnt_id__start_datetime__gte=start_date).select_related("contx_id")

        contx_set = list(dict.fromkeys([anix.contx_id for anix in anix_evnt_set]))
        if get_str:
            out_list = [utils.get_view_cont_list(contx) for contx in contx_set]
        else:
            out_list = [utils.get_cont_evnt(contx) for contx in contx_set]

        return out_list

    def get_move_history(self, start_date=None, end_date=None):
        if not start_date:
            start_date = utils.aware_min()
        if not end_date:
            end_date = timezone.now()

        move_set = MoveDet.objects.filter(anix_id__grp_id=self, move_date__lte=end_date, move_date__gte=start_date).\
            order_by("-move_date").select_related('contx_end', 'contx_start')

        out_list = []
        for move_id in move_set:
            end_move_dict = utils.get_dict_from_move(move_id, True)
            if end_move_dict is not None:
                out_list.append(end_move_dict)
            start_move_dict = utils.get_dict_from_move(move_id, False)
            if start_move_dict is not None:
                    out_list.append(start_move_dict)

        return out_list

    def current_feed(self, at_date=None):

        if not at_date:
            at_date = timezone.now()

        cont_list = self.current_cont(at_date=at_date)
        if len(cont_list) == 1:
            feed_str = cont_list[0].cont_feed(at_date=at_date, get_string=True)
        else:
            feed_str = ""
            for cont in cont_list:
                cont_feed_str = cont.cont_feed(at_date=at_date, get_string=True)
                if cont_feed_str:
                    feed_str += "{}: {}\n".format(cont.__str__(), cont_feed_str)
        return feed_str

    def count_fish_in_group(self, at_date=None):
        fish_count = 0

        if not at_date:
            at_date = timezone.now()
        # ordered oldest to newest
        cnt_set = Count.objects.filter(Q(anix_id__grp_id=self,
                                         anix_id__evnt_id__start_datetime__lte=at_date) |
                                       Q(loc_id__animal_details__grp_id=self, loc_id__loc_date__lte=at_date))\
            .select_related("cntc_id").distinct().order_by('anix_id__evnt_id__start_datetime')

        for cnt in cnt_set:
            if cnt.cntc_id.name in calculation_constants.add_codes:
                fish_count += cnt.cnt
            elif cnt.cntc_id.name in calculation_constants.subtract_codes:
                fish_count -= cnt.cnt
            elif cnt.cntc_id.name in calculation_constants.absolute_codes:
                fish_count = cnt.cnt
        return fish_count

    def fish_in_cont(self, at_date=None, select_fields=[], grp_select_fields=[]):
        if not at_date:
            at_date = timezone.now()

        indv_set = Individual.objects.filter(grp_id=self).select_related(*select_fields)
        # for consistancy with container version:
        indv_list = [indv for indv in indv_set]
        grp_list = [self]
        return indv_list, grp_list

    def get_development(self, at_date=None):
        dev = 0
        if not at_date:
            at_date = timezone.now().date()

        start_date = utils.aware_min().date()
        dev_qs = GroupDet.objects.filter(anix_id__grp_id=self, grpd_valid=True, anidc_id__name="Development")
        if len(dev_qs) == 1:
            dev = float(dev_qs[0] .det_val)
            start_date = dev_qs[0].detail_date
        degree_days = []

        move_set = MoveDet.objects.filter(anix_id__grp_id=self, move_date__lte=at_date).\
            order_by("-move_date").select_related("contx_start", "contx_end")
        end_date = at_date
        for moveDet in move_set:
            # set cont, start_date, end_date
            if end_date > moveDet.move_date > start_date and moveDet.contx_end is not None:
                cont = moveDet.contx_end.container
                degree_days.extend(cont.degree_days(moveDet.move_date, end_date))
                end_date = moveDet.move_date
            elif end_date > moveDet.move_date < start_date < end_date and moveDet.contx_end is not None:
                cont = moveDet.contx_end.container
                degree_days.extend(cont.degree_days(start_date, end_date))
                end_date = moveDet.move_date

        dev += sum([utils.daily_dev(float(degree_day)) for degree_day in degree_days])

        return utils.round_no_nan(dev, 5)

    def get_parent_grp(self, at_date=None):

        if not at_date:
            at_date = timezone.now()

        # gets parent groups this group came from.
        grpd_set = GroupDet.objects.filter(anix_id__grp_id=self,
                                           anidc_id__name="Parent Group",
                                           frm_grp_id__isnull=False,
                                           detail_date__lte=at_date,
                                           ).select_related("frm_grp_id", "frm_grp_id__stok_id", "frm_grp_id__coll_id")
        return grpd_set

    def get_parent_history(self):
        parent_grps = []
        new_grpd_qs = []
        grpd_qs = self.get_parent_grp()
        depth = 1
        while True:
            for grpd in grpd_qs:
                # check if parent is not self:
                if grpd.frm_grp_id.pk != grpd.anix_id.grp_id.pk:
                    parent_grps.append((depth, grpd.frm_grp_id, grpd.detail_date))
                    new_grpd_qs.extend(grpd.frm_grp_id.get_parent_grp(at_date=grpd.detail_date))
            # recursion catch
            if new_grpd_qs:
                grpd_qs = new_grpd_qs
                depth += 1
                new_grpd_qs = []
            else:
                break

        return parent_grps

    def prog_group(self, get_string=False):
        # gets program groups this group may be a part of.
        grpd_set = GroupDet.objects.filter(anix_id__grp_id=self,
                                           anidc_id__name="Program Group",
                                           adsc_id__isnull=False,
                                           ).select_related("adsc_id")
        if get_string:
            prog_grp_list = [grpd.adsc_id.name for grpd in grpd_set]
            prog_str = ", ".join(prog_grp_list)
            return prog_str
        else:
            prog_grp_list = [grpd.adsc_id for grpd in grpd_set]

            return prog_grp_list

    def group_mark(self, get_string=False):
        # gets any marks the group may be tagged with.
        grpd_set = GroupDet.objects.filter(anix_id__grp_id=self,
                                           anidc_id__name="Mark",
                                           adsc_id__isnull=False,
                                           ).select_related("adsc_id")
        if get_string:
            grp_mark_list = [grpd.adsc_id.name for grpd in grpd_set]
            return ", ".join(grp_mark_list)
        else:
            grp_mark_list = [grpd.adsc_id for grpd in grpd_set]
            return grp_mark_list

    def start_date(self):
        first_evnt = self.animal_details.order_by("-evnt_id__start_date").first()
        if first_evnt:
            return first_evnt.evnt_id.start_date
        else:
            return None

    def avg_weight(self, at_date=None):

        if not at_date:
            at_date = timezone.now()

        # INCORPORATE SAMPLE DETS!
        weight_deps = GroupDet.objects.filter(anix_id__grp_id=self, anidc_id__name="Weight", detail_date__lte=at_date)
        if not weight_deps:
            return ""
        weight_deps = weight_deps.order_by("-detail_date")
        last_obs_date = weight_deps.first().detail_date
        last_obs_set = weight_deps.filter(detail_date__gte=last_obs_date)
        avg_weight = last_obs_set.aggregate(Avg('det_val'))["det_val__avg"]
        return avg_weight

    def avg_len(self, at_date=None):
        if not at_date:
            at_date = timezone.now()
        len_deps = GroupDet.objects.filter(anix_id__grp_id=self, anidc_id__name="Length", detail_date__lte=at_date)
        if not len_deps:
            return ""
        len_deps = len_deps.order_by("-detail_date")
        last_obs_date = len_deps.first().detail_date
        last_obs_set = len_deps.filter(detail_date__gte=last_obs_date)
        avg_len = last_obs_set.aggregate(Avg('det_val'))["det_val__avg"]
        return avg_len

    def past_end_date(self, at_date=None):
        if not at_date:
            at_date = timezone.now().date()
        if not self.grp_end_date:
            return False
        else:
            if self.grp_end_date < at_date:
                return False
            else:
                return True


class GroupDet(BioDet):
    # grpd tag
    frm_grp_id = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name=_("From Parent Group"), db_column="FROM_GROUP_ID")
    grpd_valid = models.BooleanField(default="True", verbose_name=_("Detail still valid?"), db_column="STILL_VALID")
    anix_id = models.ForeignKey('AniDetailXRef', on_delete=models.CASCADE, related_name="group_details",
                                verbose_name=_("Animal Detail Cross Reference"), db_column="ANI_DET_XREF_ID")

    class Meta:
        unique_together = (('anix_id', 'anidc_id', 'adsc_id', 'frm_grp_id', 'detail_date'),)

    def __str__(self):
        return "{} Detail".format(self.anidc_id.name)

    def save(self, *args, **kwargs):
        """ Need to set all earlier details with the same code to invalid"""
        if self.grpd_valid:
            grp = self.anix_id.grp_id
            anix_set = grp.animal_details.filter(group_details__isnull=False,
                                                 group_details__grpd_valid=True,
                                                 group_details__anidc_id=self.anidc_id,
                                                 group_details__adsc_id=self.adsc_id,
                                                 )
            old_grpd_set = [anix.group_details.filter(detail_date__lte=self.detail_date, grpd_valid=True) for anix in anix_set]
            for old_grpd_qs in old_grpd_set:
                for old_grpd in old_grpd_qs:
                    old_grpd.grpd_valid = False
                    old_grpd.save()

            current_grpd_set = [anix.group_details.filter(detail_date__gt=self.detail_date) for anix in anix_set]
            for current_grpd in current_grpd_set:
                if current_grpd:
                    self.grpd_valid = False

        super(GroupDet, self).save(*args, **kwargs)

    @property
    def evnt(self):
        return self.anix_id.evnt_id


class HeathUnit(BioCont):
    # heat tag
    key = "heat"

    facic_id = models.ForeignKey('FacilityCode', on_delete=models.CASCADE, verbose_name=_("Facility"), db_column="FAC_ID")

    class Meta:
        unique_together = (('name', 'facic_id'),)
        ordering = ['facic_id', 'name']


class HeathUnitDet(BioContainerDet):
    # heatd tag
    heat_id = models.ForeignKey('HeathUnit', on_delete=models.CASCADE, verbose_name=_("Heath Unit"),
                                db_column="HEATH_UNIT_ID")

    class Meta:
        unique_together = (('heat_id', 'contdc_id', 'cdsc_id', 'start_date'),)

    def __str__(self):
        return "{} - {}".format(self.heat_id.__str__(), self.contdc_id.__str__())


# This is a special table used to house application help text
class HelpText(models.Model):
    field_name = models.CharField(max_length=255)
    eng_text = models.TextField(verbose_name=_("English text"))
    fra_text = models.TextField(blank=True, null=True, verbose_name=_("French text"))
    model = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("eng_text"))):
            return "{}".format(getattr(self, str(_("eng_text"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.eng_text)

    class Meta:
        ordering = ['field_name', ]


def img_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/bio_diversity/images/<filename>
    return 'bio_diversity/images/{}'.format(filename)


class Image(BioModel):
    # img tag
    imgc_id = models.ForeignKey("ImageCode", on_delete=models.CASCADE, verbose_name=_("Document Code"), db_column="IMG_ID")
    loc_id = models.ForeignKey("Location", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                               verbose_name=_("Location"), db_column="LOCATION_ID")
    cntd_id = models.ForeignKey("CountDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                verbose_name=_("Count Detail"), db_column="COUNT_ID")
    grpd_id = models.ForeignKey("GroupDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                verbose_name=_("Group Detail"), db_column="GROUP_DET_ID")
    sampd_id = models.ForeignKey("SampleDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                 verbose_name=_("Sample Detail"), db_column="SAMP_DET_ID")
    indvd_id = models.ForeignKey("IndividualDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                 verbose_name=_("Individual Detail"), db_column="INDIV_DET_ID")
    spwnd_id = models.ForeignKey("SpawnDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                 verbose_name=_("Spawn Detail"), db_column="SPAWN_DETAIL_ID")
    tankd_id = models.ForeignKey("TankDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                 verbose_name=_("Tank Detail"), db_column="TANK_DET_ID")
    heatd_id = models.ForeignKey("HeathUnitDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                 verbose_name=_("Heath Unit Detail"), db_column="HEATH_UNIT_DET_ID")
    draw_id = models.ForeignKey("Drawer", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                verbose_name=_("Drawer"), db_column="DRAWER_ID")
    trofd_id = models.ForeignKey("TroughDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                 verbose_name=_("Trough Detail"), db_column="TROUGH_DET_ID")
    trayd_id = models.ForeignKey("TrayDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                 verbose_name=_("Tray Detail"), db_column="TRAY_DET_ID")
    cupd_id = models.ForeignKey("CupDet", on_delete=models.CASCADE, null=True, blank=True, related_name="images",
                                verbose_name=_("Cup Detail"), db_column="CUP_DET_ID")
    img_png = models.FileField(upload_to=img_directory_path, null=True, blank=True, verbose_name=_("Document File"),
                               db_column="IMAGE")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def __str__(self):
        return "{}".format(self.img_png)

    class Meta:
        unique_together = (("imgc_id", "loc_id", "cntd_id", "grpd_id", "sampd_id", "indvd_id",
                            "spwnd_id", "tankd_id", "heatd_id", "draw_id", "trofd_id", "trayd_id",
                            "cupd_id"),)


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.img_png:
        if os.path.isfile(instance.img_png.path):
            os.remove(instance.img_png.path)


@receiver(models.signals.pre_save, sender=Image)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = Image.objects.get(pk=instance.pk).img_png
    except Image.DoesNotExist:
        return False
    new_file = instance.img_png
    if old_file and not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class ImageCode(BioLookup):
    # imgc tag
    pass


class Individual(BioModel):
    # indv tag

    grp_id = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True, db_column="GROUP_ID",
                               verbose_name=_("From Parent Group"), limit_choices_to={'grp_valid': True})
    spec_id = models.ForeignKey('SpeciesCode', on_delete=models.CASCADE, verbose_name=_("Species"), db_column="SPEC_ID")
    stok_id = models.ForeignKey('StockCode', on_delete=models.CASCADE, verbose_name=_("Stock Code"), db_column="STOCK_ID")
    indv_year = models.IntegerField(verbose_name=_("Collection year"), default=2000, db_column="YEAR",
                                    validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    coll_id = models.ForeignKey('Collection', on_delete=models.CASCADE, default=25, db_column="COLLECTION_ID",
                                verbose_name=_("Collection"))
    # ufid = unique FISH id
    ufid = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name=_("ABL Fish UFID"),
                            db_column="UFID")
    pit_tag = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name=_("PIT tag ID"),
                               db_column="PIT_TAG")
    indv_valid = models.BooleanField(default="True", verbose_name=_("Entry still valid?"), db_column="STILL_VALID")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def __str__(self):
        if self.pit_tag:
            return "{}-{}-{}-{}".format(self.stok_id.__str__(), self.indv_year, self.coll_id.__str__(), self.pit_tag)
        else:
            return "{}-{}-{}".format(self.stok_id.__str__(), self.indv_year, self.coll_id.__str__())

    class Meta:
        ordering = ["pit_tag", "indv_year"]

    def stok_year_coll_str(self):
        return "{}-{}-{}".format(self.stok_id.__str__(), self.indv_year, self.coll_id.__str__())

    def current_cont(self, at_date=None, valid_only=False, get_string=False):
        if not at_date:
            at_date = timezone.now()
        cont_list = []
        if not self.indv_valid and valid_only:
            if get_string:
                return ""
            return cont_list

        last_move = MoveDet.objects.filter(anix_id__indv_id=self, move_date__lte=at_date). \
            select_related('contx_end').order_by("-move_date").first()

        if last_move:
            if last_move.contx_end:
                cont_list = [last_move.contx_end.container]

        if get_string:
            cont_str_list = [cont.__str__() for cont in cont_list]
            cont_str = ", ".join(cont_str_list)
            return cont_str
        return cont_list

    def current_feed(self, at_date=None):
        if not at_date:
            at_date = timezone.now()

        cont_list = self.current_cont(at_date=at_date)
        if len(cont_list) == 1:
            feed_str = cont_list[0].cont_feed(at_date=at_date, get_string=True)
        else:
            feed_str = ""
            for cont in cont_list:
                feed_str += "{}: {}\n".format(cont.__str__(), cont.cont_feed(at_date=at_date, get_string=True))
        return feed_str

    def get_parent_history(self):
        parent_grps = [(0, self.grp_id, self.start_date())]
        if self.grp_id:
            parent_grps.extend(self.grp_id.get_parent_history())
        return parent_grps

    def get_move_history(self, start_date=None, end_date=None):
        if not start_date:
            start_date = utils.aware_min()
        if not end_date:
            end_date = timezone.now()

        move_set = MoveDet.objects.filter(anix_id__indv_id=self, move_date__lte=end_date, move_date__gte=start_date).\
            order_by("-move_date").select_related('contx_end', 'contx_start')

        out_list = []
        for move_id in move_set:
            end_move_dict = utils.get_dict_from_move(move_id, True)
            if end_move_dict is not None:
                out_list.append(end_move_dict)
            start_move_dict = utils.get_dict_from_move(move_id, False)
            if start_move_dict is not None:
                out_list.append(start_move_dict)

        return out_list

    def start_date(self):
        first_evnt = self.animal_details.order_by("-evnt_id__start_date").first()
        if first_evnt:
            return first_evnt.evnt_id.start_date
        else:
            return None

    def individual_detail(self, anidc_name="Length", before_date=None, evnt_id=None):
        if not before_date:
            before_date = timezone.now()
        if evnt_id:
            latest_indvd = IndividualDet.objects.filter(anidc_id__name__icontains=anidc_name, anix_id__indv_id=self,
                                                        detail_date__lte=before_date,
                                                        anix_id__evnt_id=evnt_id).order_by("-detail_date").first()
        else:
            latest_indvd = IndividualDet.objects.filter(anidc_id__name__icontains=anidc_name, anix_id__indv_id=self,
                                                        detail_date__lte=before_date).order_by("-detail_date").first()
        if latest_indvd:
            return latest_indvd.det_val
        else:
            return None

    def individual_subj_detail(self, anidc_name="Animal Health", before_date=None, evnt_id=None):
        if not before_date:
            before_date = timezone.now()
        if evnt_id:
            latest_indvd = IndividualDet.objects.filter(anidc_id__name__icontains=anidc_name, anix_id__indv_id=self,
                                                        detail_date__lte=before_date, anix_id__evnt_id=evnt_id,
                                                        adsc_id__isnull=False).order_by("-detail_date").select_related(
                "adsc_id").first()
        else:
            latest_indvd = IndividualDet.objects.filter(anidc_id__name__icontains=anidc_name, anix_id__indv_id=self,
                                                        detail_date__lte=before_date,
                                                        adsc_id__isnull=False).order_by("-detail_date").select_related("adsc_id").first()
        if latest_indvd:
            return latest_indvd.adsc_id.name
        else:
            return None

    def individual_evnt_details(self, evnt_id):
        indvd_qs = IndividualDet.objects.filter(anix_id__indv_id=self, adsc_id__isnull=False,
                                                anix_id__evnt_id=evnt_id).order_by("-detail_date").select_related("adsc_id")
        out_str = ""
        for indvd in indvd_qs:
            out_str += indvd.adsc_id.name + ", "
        return out_str

    def prog_group(self, get_string=False):
        # gets program groups this group may be a part of.
        indvd_set = IndividualDet.objects.filter(anix_id__indv_id=self,
                                                 anidc_id__name="Program Group",
                                                 adsc_id__isnull=False,
                                                 ).select_related("adsc_id")

        if get_string:
            prog_grp_list = [indvd.adsc_id.name for indvd in indvd_set]
            prog_str = ", ".join(prog_grp_list)
            return prog_str
        else:
            prog_grp_list = [indvd.adsc_id for indvd in indvd_set]
            return prog_grp_list


class IndividualDet(BioDet):
    # indvd tag
    indvd_valid = models.BooleanField(default="True", verbose_name=_("Detail still valid?"), db_column="STILL_VALID")
    anix_id = models.ForeignKey('AniDetailXRef', on_delete=models.CASCADE, related_name="individual_details",
                                verbose_name=_("Animal Detail Cross Reference"), db_column="ANI_DET_XREF_ID")

    class Meta:
        unique_together = (('anix_id', 'anidc_id', 'adsc_id', 'detail_date'),)

    def __str__(self):
        return "{} - {}".format(self.anix_id.__str__(), self.anidc_id.__str__())

    def save(self,  *args, **kwargs):
        """ Need to set all earlier details with the same code to invalid"""
        if self.indvd_valid:
            indv = self.anix_id.indv_id
            if indv:
                anix_set = indv.animal_details.filter(individual_details__isnull=False,
                                                      individual_details__indvd_valid=True,
                                                      individual_details__anidc_id=self.anidc_id,
                                                      individual_details__adsc_id=self.adsc_id,
                                                      )
                old_indvd_set = [anix.individual_details.filter(detail_date__lt=self.detail_date, anidc_id=self.anidc_id, adsc_id=self.adsc_id) for anix in anix_set]
                for old_indvd in old_indvd_set:
                    if old_indvd:
                        old_indvd = old_indvd.get()
                        old_indvd.indvd_valid = False
                        old_indvd.save()

                current_indvd_set = [anix.individual_details.filter(detail_date__gt=self.detail_date, anidc_id=self.anidc_id, adsc_id=self.adsc_id) for anix in anix_set]
                for current_indvd in current_indvd_set:
                    if current_indvd:
                        self.indvd_valid = False

        super(IndividualDet, self).save(*args, **kwargs)

    @property
    def evnt(self):
        return self.anix_id.evnt_id


class IndTreatCode(BioLookup):
    # indvtc tag
    rec_dose = models.CharField(max_length=400, verbose_name=_("Recommended Dosage"), db_column="IND_REC_DOSAGE")
    manufacturer = models.CharField(max_length=50, verbose_name=_("Treatment Manufacturer"), db_column="IND_MANUFACTURER")


class IndTreatment(BioTimeModel):
    # indvt tag
    anix_id = models.ForeignKey('AniDetailXRef', on_delete=models.CASCADE, related_name="individual_treatments",
                                verbose_name=_("Animal Detail Cross Reference"), db_column="ANI_DET_XREF_ID")
    indvtc_id = models.ForeignKey('IndTreatCode', on_delete=models.CASCADE, db_column="IND_TEART_ID",
                                  verbose_name=_("Individual Treatment Code"))
    lot_num = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Lot Number"), db_column="LOT_NUMBER")
    dose = models.DecimalField(max_digits=7, decimal_places=3, verbose_name=_("Dose"), db_column="DOSE")
    unit_id = models.ForeignKey('UnitCode', on_delete=models.CASCADE, verbose_name=_("Units"), db_column="UNIT_ID")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def __str__(self):
        return "{}-{}".format(self.indvtc_id.__str__(), self.lot_num)

    class Meta:
        unique_together = (('anix_id', 'indvtc_id'),)


class Instrument(BioModel):
    # inst tag
    instc_id = models.ForeignKey('InstrumentCode', on_delete=models.CASCADE, verbose_name=_("Instrument Code"),
                                 db_column="INST_ID")
    serial_number = models.CharField(null=True, unique=True, blank=True, max_length=250, db_column="SERIAL_NUMBER",
                                     verbose_name=_("Serial Number"))
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def __str__(self):
        return "{} - {}".format(self.instc_id.__str__(), self.serial_number)


class InstrumentCode(BioLookup):
    # instc tag
    pass


class InstrumentDet(BioDateModel):
    # instd tag
    inst_id = models.ForeignKey('Instrument', on_delete=models.CASCADE, verbose_name=_("Instrument"),
                                db_column="INSTRUM_ID")
    instdc_id = models.ForeignKey('InstDetCode', on_delete=models.CASCADE, verbose_name=_("Instrument Detail Code"),
                                  db_column="INST_DET_ID")
    det_value = models.DecimalField(max_digits=11, decimal_places=5, verbose_name=_("Value"), db_column="VAL")

    class Meta:
        unique_together = (('inst_id', 'instdc_id', 'start_date'),)

    def __str__(self):
        return "{}-{}".format(self.instdc_id.__str__(), self.inst_id.__str__())


class InstDetCode(BioLookup):
    # instdc tag
    pass


class Location(BioModel):
    # loc tag
    evnt_id = models.ForeignKey('Event', on_delete=models.CASCADE, verbose_name=_("Event"), related_name="location",
                                db_column="EVENT_ID")
    locc_id = models.ForeignKey('LocCode', on_delete=models.CASCADE, verbose_name=_("Location Code"), db_column="LOC_ID")
    rive_id = models.ForeignKey('RiverCode', on_delete=models.CASCADE, null=True, blank=True, db_column="RIVER_ID",
                                verbose_name=_("River"))
    trib_id = models.ForeignKey('Tributary', on_delete=models.CASCADE, null=True, blank=True, db_column="TRIB_ID",
                                verbose_name=_("Tributary"))
    subr_id = models.ForeignKey('SubRiverCode', on_delete=models.CASCADE, null=True, blank=True, db_column="SUBRIVER_ID",
                                verbose_name=_("SubRiver Code"))
    relc_id = models.ForeignKey('ReleaseSiteCode', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name=_("Site Code"), related_name="locations", db_column="SITE_ID")
    loc_lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True, db_column="LATITUDE",
                                  verbose_name=_("Latitude"))
    loc_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_column="LONGITUDE",
                                  verbose_name=_("Longitude"))
    end_lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True, db_column="END_LATITUDE",
                                  verbose_name=_("End Latitude"))
    end_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_column="END_LONGITUDE",
                                  verbose_name=_("End Longitude"))
    loc_date = models.DateTimeField(verbose_name=_("Start date"), db_column="LOCATION_DATE")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    @property
    def start_date(self):
        return self.loc_date.date()

    @property
    def start_time(self):
        if self.loc_date.time() == time(0, 0):
            return None
        return self.loc_date.time().strftime("%H:%M")

    def __str__(self):
        return "{} location".format(self.locc_id.__str__())

    class Meta:
        unique_together = (("evnt_id", "locc_id", "rive_id", "trib_id", "subr_id", "relc_id", "loc_lat",
                            "loc_lon", "loc_date"),)

    @property
    def point(self):
        # lon = x, lat = y
        if (self.loc_lat is not None) and (self.loc_lon is not None):
            return Point(self.loc_lon, self.loc_lat)
        else:
            return Point()

    @property
    def end_point(self):
        if (self.end_lat is not None) and (self.end_lon is not None):
            return Point(self.end_lon, self.end_lat)
        else:
            return Point()

    @property
    def linestring(self):
        if (self.loc_lat is not None) and (self.loc_lon is not None) and (self.end_lat is not None) and \
                (self.end_lon is not None):
            return LineString([(self.loc_lon, self.loc_lat), (self.end_lon, self.end_lat)])
        else:
            return Point()

    def set_relc_latlng(self):
        if not self.relc_id and self.point:
            self.relc_id = utils.get_relc_from_point(self.point)
            if not self.relc_id and self.end_point:
                self.relc_id = utils.get_relc_from_point(self.linestring)
        if self.relc_id and not self.point:
            if self.relc_id.bbox:
                self.loc_lon = round(decimal.Decimal(self.relc_id.bbox.centroid.xy[0][0] + 0.0005), 5)
                self.loc_lat = round(decimal.Decimal(self.relc_id.bbox.centroid.xy[1][0]), 5)

    def clean(self, *args, **kwargs):
        if self.relc_id and not self.rive_id:
            self.rive_id = self.relc_id.rive_id
        if self.relc_id and not self.trib_id:
            self.trib_id = self.relc_id.trib_id
        if self.relc_id and not self.subr_id:
            self.sube_id = self.relc_id.subr_id
        super(Location, self).clean(*args, **kwargs)
        if self.loc_lon is not None:  # only check long,that's where minus signs are left off
            if float(self.loc_lon) < calculation_constants.min_long:
                raise ValidationError("Longitude must be within maritimes (>{})".format(calculation_constants.min_long))
            if float(self.loc_lon) > calculation_constants.max_long:
                raise ValidationError("Longitude must be within maritimes (<{}). "
                                      "Should this value be negative?".format(calculation_constants.max_long))

    def get_cont_history(self, start_date=None, end_date=None, get_str=False):
        if not start_date:
            start_date = utils.aware_min()
        if not end_date:
            end_date = timezone.now()

        anix_evnt_set = AniDetailXref.objects.filter(loc_id=self, contx_id__isnull=False, grp_id__isnull=True,
                                                     pair_id__isnull=True, evnt_id__start_datetime__lte=end_date,
                                                     evnt_id__start_datetime__gte=start_date).select_related("contx_id")

        contx_set = list(dict.fromkeys([anix.contx_id for anix in anix_evnt_set]))
        if get_str:
            out_list = [utils.get_view_cont_list(contx) for contx in contx_set]
        else:
            out_list = [utils.get_cont_evnt(contx) for contx in contx_set]

        return out_list


class LocCode(BioLookup):
    # locc tag
    pass


class LocationDet(BioDet):
    # locd tag
    anidc_id = None
    adsc_id = None
    loc_id = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name=_("Location"), related_name="loc_dets",
                               db_column="LOCATION_ID")
    locdc_id = models.ForeignKey('LocationDetCode', on_delete=models.CASCADE, verbose_name=_("Location Detail Code"),
                                 db_column="LOC_DET_ID")
    ldsc_id = models.ForeignKey('LocDetSubjCode', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name=_("Location Detail Subjective Code"), db_column="LOC_DET_SUBJ_ID")

    def clean(self):
        super(BioDet, self).clean()
        if self.is_numeric() and self.det_val is not None:
            if float(self.det_val) > self.locdc_id.max_val or float(self.det_val) < self.locdc_id.min_val:
                raise ValidationError({
                    "det_val": ValidationError("Value {} exceeds limits. Max: {}, Min: {}"
                                               .format(self.det_val, self.locdc_id.max_val, self.locdc_id.min_val))
                })

    def is_numeric(self):
        if self.locdc_id.min_val is not None and self.locdc_id.max_val is not None:
            return True
        else:
            return False

    class Meta:
        unique_together = (('loc_id', 'locdc_id', 'ldsc_id'),)


class LocationDetCode(BioLookup):
    # locdc tag
    min_val = models.DecimalField(max_digits=11, decimal_places=5, blank=True, null=True, verbose_name=_("Minimum Value"), db_column="MIN_VAL")
    max_val = models.DecimalField(max_digits=11, decimal_places=5, blank=True, null=True, verbose_name=_("Maximum Value"), db_column="MAX_VAL")
    unit_id = models.ForeignKey("UnitCode", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Units"),
                                db_column="UNIT_ID")
    loc_subj_flag = models.BooleanField(verbose_name=_("Subjective detail?"), db_column="CONT_SUBJ_FLAG")


class LocDetSubjCode(BioLookup):
    # ldsc tag
    locdc_id = models.ForeignKey("LocationDetCode", on_delete=models.CASCADE, db_column="LOC_DET_ID",
                                 verbose_name=_("Location detail code"))

    class Meta:
        unique_together = (('name', 'locdc_id'),)


class MoveDet(BioModel):
    # move tag
    anix_id = models.ForeignKey('AniDetailXref', null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name=_("Animal Detail X Ref"),
                                db_column="ANI_DET_X_REF_ID")
    contx_start = models.ForeignKey("ContainerXRef", on_delete=models.CASCADE, related_name="move_start", null=True, blank=True,
                                 verbose_name=_("Container Cross Reference"), db_column="CONTAINER_XREF_START_ID")
    contx_end = models.ForeignKey("ContainerXRef", on_delete=models.CASCADE, null=True, blank=True, related_name="move_end",
                                 verbose_name=_("Container Cross Reference End"), db_column="CONTAINER_XREF_END_ID")
    move_date = models.DateField(verbose_name=_("Date move was recorded"), db_column="MOVE_DATE")

    class Meta:
        unique_together = (('anix_id', 'contx_start', 'contx_end', 'move_date'),)

    @property
    def evnt(self):
        return self.anix_id.evnt_id

    @property
    def loc_id(self):
        if self.anix_id.loc_id:
            return self.anix_id.loc_id
        else:
            return None


class Organization(BioLookup):
    # orga tag
    pass


class Pairing(BioDateModel):
    # pair tag
    indv_id = models.ForeignKey('Individual',  on_delete=models.CASCADE, verbose_name=_("Dam"), db_column="INDIVIDUAL",
                                limit_choices_to={'pit_tag__isnull': False, 'indv_valid': True}, related_name="pairings",
                                null=True, blank=True)
    samp_id = models.ForeignKey('Sample',  on_delete=models.CASCADE, verbose_name=_("sample"), db_column="SAMPLE",
                                limit_choices_to={'anix_id__isnull': False}, related_name="pairings", null=True,
                                blank=True)
    prio_id = models.ForeignKey('PriorityCode', on_delete=models.CASCADE, verbose_name=_("Priority of Female"),
                                related_name="female_priorities", db_column="PRIORITY_ID")
    pair_prio_id = models.ForeignKey('PriorityCode', on_delete=models.CASCADE, verbose_name=_("Priority of Pair"),
                                     related_name="pair_priorities", db_column="PAIR_PRIORITY_ID")
    cross = models.IntegerField(verbose_name=_("Cross"), db_column="CROSS")

    def __str__(self):
        if self.indv_id:
            return "{}".format(self.indv_id.__str__())
        elif self.samp_id:
            return "{}".format(self.samp_id.__str__())
        else:
            return None

    class Meta:
        unique_together = (('indv_id', 'samp_id', 'start_date'),)

    @property
    def dam_id(self):
        if self.indv_id:
            return self.indv_id
        elif self.samp_id:
            return self.samp_id
        else:
            return None

    def prog_group(self, get_string=False):
        # gets program groups this group may be a part of.
        spwnd_set = self.spawning_details.filter(spwndc_id__name="Program Group",
                                                 spwnsc_id__isnull=False,
                                                 ).select_related("spwnsc_id")
        if get_string:
            prog_pair_list = [spwnd.spwnsc_id.name for spwnd in spwnd_set]
            prog_str = ", ".join(prog_pair_list)
            return prog_str
        else:
            prog_pair_list = [spwnd.spwnsc_id for spwnd in spwnd_set]

            return prog_pair_list


class PersonnelCode(BioModel):
    # perc tag
    perc_last_name = models.CharField(max_length=32, verbose_name=_("Last Name"),)
    perc_first_name = models.CharField(max_length=32, verbose_name=_("First Name"))
    initials = models.CharField(max_length=4, unique=True, verbose_name=_("Initials"), blank=True, null=True)
    perc_valid = models.BooleanField(default="False", verbose_name=_("Record still valid?"))

    def __str__(self):
        return "{} {}".format(self.perc_first_name, self.perc_last_name)

    class Meta:
        unique_together = (('perc_first_name', 'perc_last_name'),)
        ordering = ["perc_last_name", "perc_first_name"]


class PriorityCode(BioLookup):
    # prio tag
    pass


class Program(BioDateModel):
    # prog tag
    prog_name = models.CharField(max_length=30, unique=True, verbose_name=_("Program Name"), db_column="PROGRAM_NAME")
    prog_desc = models.CharField(max_length=4000, verbose_name=_("Program Description"), db_column="PROGRAM_DESC")
    proga_id = models.ForeignKey('ProgAuthority', on_delete=models.CASCADE, verbose_name=_("Program Authority"),
                                 db_column="PROG_AUTH_ID")
    orga_id = models.ForeignKey('Organization', on_delete=models.CASCADE, verbose_name=_("Organization"),
                                db_column="ORG_ID")

    def __str__(self):
        return self.prog_name


class ProgAuthority(BioModel):
    # proga tag
    proga_last_name = models.CharField(max_length=32, verbose_name=_("Last Name"), db_column="PROG_AUTH_LAST_NAME")
    proga_first_name = models.CharField(max_length=32, verbose_name=_("First Name"), db_column="PROG_AUTH_FIRST_NAME")

    def __str__(self):
        return "{} {}".format(self.proga_first_name, self.proga_last_name)

    class Meta:
        unique_together = (('proga_first_name', 'proga_last_name'),)


class Protocol(BioDateModel):
    # prot tag

    prog_id = models.ForeignKey('Program', on_delete=models.CASCADE, verbose_name=_("Program"),
                                limit_choices_to={'valid': True}, related_name="protocols", db_column="PROGRAM_ID")
    protc_id = models.ForeignKey('ProtoCode', on_delete=models.CASCADE, verbose_name=_("Protocol Code"),
                                 db_column="PROTO_ID")
    facic_id = models.ForeignKey('FacilityCode', on_delete=models.CASCADE, verbose_name=_("Facility"),
                                 db_column="FAC_ID")
    evntc_id = models.ForeignKey('EventCode', blank=True, null=True, on_delete=models.CASCADE, db_column="EVT_ID",
                                 verbose_name=_("Event Code"))
    name = models.CharField(max_length=25, verbose_name=_("Protocol Name"), db_column="PROTOCOL_NAME")
    prot_desc = models.CharField(max_length=4000, verbose_name=_("Protocol Description"), db_column="PROTOCOL_DESC")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'prog_id', 'protc_id', 'start_date'),)


class ProtoCode(BioLookup):
    # protc tag
    pass


def protf_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/bio_diversity/protofiles/<filename>
    return 'bio_diversity/protofiles/{}'.format(filename)


class Protofile(BioModel):
    # protf tag
    prot_id = models.ForeignKey('Protocol', on_delete=models.CASCADE, related_name="protf_id", db_column="PROTOCOL_ID",
                                verbose_name=_("Protocol"), limit_choices_to={'valid': True})
    protf_pdf = models.FileField(upload_to=protf_directory_path, blank=True, null=True, verbose_name=_("Protocol File"),
                                 db_column="PROTO_FILE")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def __str__(self):
        return "{}".format(self.protf_pdf)


@receiver(models.signals.post_delete, sender=Protofile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.protf_pdf:
        if os.path.isfile(instance.protf_pdf.path):
            os.remove(instance.protf_pdf.path)


@receiver(models.signals.pre_save, sender=Protofile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = Protofile.objects.get(pk=instance.pk).protf_pdf
    except Protofile.DoesNotExist:
        return False
    new_file = instance.protf_pdf
    if old_file and not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class QualCode(BioLookup):
    # qual tag
    pass


class ReleaseSiteCode(BioLookup):
    # relc tag
    rive_id = models.ForeignKey('RiverCode', on_delete=models.CASCADE, verbose_name=_("River"), related_name="sites",
                                db_column="RIVER_ID")
    trib_id = models.ForeignKey('Tributary', on_delete=models.CASCADE, null=True, blank=True, db_column="TRIB_ID",
                                verbose_name=_("Tributary"))
    subr_id = models.ForeignKey('SubRiverCode', on_delete=models.CASCADE, null=True, blank=True, db_column="SUBRIVER_ID",
                                verbose_name=_("SubRiver Code"))
    min_lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True, db_column="MIN_LATITUDE",
                                  verbose_name=_("Min Latitude"))
    max_lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True, db_column="MAX_LATITUDE",
                                  verbose_name=_("Max Latitude"))
    min_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_column="MIN_LONGITUDE",
                                  verbose_name=_("Min Longitude"))
    max_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_column="MAX_LONGITUDE",
                                  verbose_name=_("Max Longitude"))

    def clean(self):
        super(ReleaseSiteCode, self).clean()
        if None not in [self.min_lat, self.min_lon, self.max_lat, self.max_lon]:
            if float(self.min_lon) > float(self.max_lon) or float(self.min_lat) > float(self.max_lat):
                raise ValidationError("Max lat/lon must be greater than min lat/lon")
        if self.min_lon is not None:
            lon_float = float(self.min_lon)
            if lon_float < calculation_constants.min_long or lon_float > calculation_constants.max_long:
                raise ValidationError("Min longitude must be within maritimes (>{}, <{})".format(
                    calculation_constants.min_long,
                    calculation_constants.max_long))
        if self.max_lon is not None:
            lon_float = float(self.max_lon)
            if lon_float < calculation_constants.min_long or lon_float > calculation_constants.max_long:
                raise ValidationError("Max longitude must be within maritimes (>{}, <{}). "
                                      "Should this value be negative?".format(calculation_constants.min_long,
                                                                              calculation_constants.max_long))

    @property
    def bbox(self):
        # lon = x, lat = y
        if None not in [self.min_lat, self.min_lon, self.max_lat, self.max_lon]:
            bbox = box(
                    float(self.min_lon),
                    float(self.min_lat),
                    float(self.max_lon),
                    float(self.max_lat),
                )
            return bbox
        else:
            return

    @property
    def point(self):
        # lon = x, lat = y
        if None not in [self.min_lat, self.min_lon]:
            site_point = Point(float(self.min_lon), float(self.min_lat))
            return site_point
        else:
            return Point()

    @property
    def area(self):
        # lon = x, lat = y
        corr_factor = 8 / 11
        if None not in [self.min_lat, self.min_lon, self.max_lat, self.max_lon]:
            delta_y = corr_factor * (float(self.max_lat) - float(self.min_lat))
            delta_x = float(self.max_lon) - float(self.min_lon)
            return abs(delta_x * delta_y)
        else:
            return 0


class RiverCode(BioLookup):
    # rive tag
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    # mpoly = models.MultiPolygonField()
    pass


class RoleCode(BioLookup):
    # role tag
    pass


class Sample(BioModel):
    # samp tag
    loc_id = models.ForeignKey('Location', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Location"),
                               db_column="LOCATION_ID", related_name="samples")
    anix_id = models.ForeignKey('AniDetailXref', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Animal Detail X Ref"),
                                db_column="ANI_DET_X_REF_ID")
    samp_num = models.CharField(max_length=50, verbose_name=_("Sample Fish Number"), db_column="SAMPLE_FISHNO")
    spec_id = models.ForeignKey('SpeciesCode', on_delete=models.CASCADE, verbose_name=_("Species"), db_column="SPEC_ID")
    sampc_id = models.ForeignKey('SampleCode', on_delete=models.CASCADE, verbose_name=_("Sample Code"),
                                 db_column="SAMP_ID")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def __str__(self):
        return "{} - {}".format(self.sampc_id.__str__(), self.samp_num)

    class Meta:
        unique_together = (('loc_id', 'anix_id', 'samp_num', 'spec_id', 'sampc_id'),)

    def clean(self, *args, **kwargs):
        if self.loc_id is None and self.anix_id.grp_id is None:
            raise ValidationError("Sample must come from group or location.")
        super(Sample, self).clean()

    @property
    def coll_id(self):
        if self.anix_id.grp_id:
            return self.anix_id.grp_id.coll_id
        else:
            return None

    @property
    def stok_id(self):
        if self.anix_id.grp_id:
            return self.anix_id.grp_id.stok_id
        else:
            return None

    @property
    def indv_year(self):
        if self.anix_id.grp_id:
            return self.anix_id.grp_id.grp_year
        else:
            return None

    @property
    def samp_date(self):
        if self.loc_id:
            return self.loc_id.loc_date
        elif self.anix_id:
            return self.anix_id.evnt_id.start_date
        else:
            return None

    def samp_detail(self, anidc_name="Length"):
        latest_indvd = SampleDet.objects.filter(anidc_id__name__icontains=anidc_name, samp_id=self).first()
        if latest_indvd:
            return latest_indvd.det_val
        else:
            return None

    def cont(self, get_string=False):
        if self.anix_id:
            cont = utils.get_cont_from_anix(self.anix_id, None)
        else:
            cont = None
        if get_string:
            if cont:
                return cont.__str__()
            else:
                return ""
        return cont

    def sample_detail(self, anidc_name="Length", before_date=None, evnt_id=None):
        if not before_date:
            before_date = timezone.now()
        if evnt_id:
            latest_sampd = SampleDet.objects.filter(anidc_id__name__icontains=anidc_name, samp_id=self,
                                                    detail_date__lte=before_date, samp_id__anix_id__evnt_id=evnt_id).order_by("-detail_date").first()
        else:
            latest_sampd = SampleDet.objects.filter(anidc_id__name__icontains=anidc_name, samp_id=self,
                                                    detail_date__lte=before_date).order_by("-detail_date").first()
        if latest_sampd:
            return latest_sampd.det_val
        else:
            return None

    def prog_group(self, get_string=False):
        if self.anix_id:
            return self.anix_id.grp_id.prog_group(get_string=get_string)
        else:
            return None


class SampleCode(BioLookup):
    # sampc tag
    pass


class SampleDet(BioDet):
    # sampd tag
    samp_id = models.ForeignKey('Sample', on_delete=models.CASCADE, verbose_name=_("Sample"), db_column="SAMPLE_ID")

    class Meta:
        unique_together = (('samp_id', 'anidc_id', 'adsc_id', 'detail_date'),)

    def __str__(self):
        return "{} - {}".format(self.samp_id.__str__(), self.anidc_id.__str__())


class Sire(BioModel):
    # sire tag
    prio_id = models.ForeignKey('PriorityCode', on_delete=models.CASCADE, verbose_name=_("Priority"),
                                db_column="PRIORITY_ID")
    pair_id = models.ForeignKey('Pairing', on_delete=models.CASCADE, verbose_name=_("Pairing"), related_name="sires",
                                limit_choices_to={'valid': True}, db_column="PAIR_ID")
    indv_id = models.ForeignKey('Individual', on_delete=models.CASCADE, verbose_name=_("Individual"), db_column="UFID",
                                limit_choices_to={'pit_tag__isnull':  False, 'indv_valid': True}, related_name="sires",
                                null=True, blank=True)
    samp_id = models.ForeignKey('Sample', on_delete=models.CASCADE, verbose_name=_("Sample"), db_column="SAMPLE",
                                limit_choices_to={'anix_id__isnull':  False}, related_name="sires", null=True,
                                blank=True)
    choice = models.IntegerField(verbose_name=_("Choice"), db_column="CHOICE")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"), db_column="COMMENTS")

    def __str__(self):
        if self.indv_id:
            return "Sire {}".format(self.indv_id.__str__())
        elif self.samp_id:
            return "Sire {}".format(self.samp_id.__str__())
        else:
            return "Unknown Sire"

    @property
    def sire_id(self):
        if self.indv_id:
            return self.indv_id
        elif self.samp_id:
            return self.samp_id
        else:
            return None

    class Meta:
        unique_together = (('indv_id', 'samp_id', 'pair_id'),)


class SpawnDet(BioModel):
    # spwnd tag
    pair_id = models.ForeignKey('Pairing', on_delete=models.CASCADE, related_name="spawning_details",
                                verbose_name=_("Pairing"), db_column="PAIR_ID")
    spwndc_id = models.ForeignKey('SpawnDetCode', on_delete=models.CASCADE, verbose_name=_("Spawning Detail Code"),
                                  db_column="SPAWN_DET_ID")
    spwnsc_id = models.ForeignKey('SpawnDetSubjCode', on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name=_("Spawning Detail Subjective Code"), db_column="SPAWN_DET_SUBJ_ID")
    det_val = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Value"), db_column="VAL")
    qual_id = models.ForeignKey('QualCode', on_delete=models.CASCADE, verbose_name=_("Quality"), db_column="QUAL_ID")
    comments = models.CharField(null=True, blank=True, max_length=2000, verbose_name=_("Comments"),
                                db_column="COMMENTS")

    class Meta:
        unique_together = (('pair_id', 'spwndc_id', 'spwnsc_id'),)

    def __str__(self):
        return "{} - {}".format(self.pair_id.__str__(), self.spwndc_id.__str__())

    def clean(self):
        super(SpawnDet, self).clean()
        if self.is_numeric() and self.det_val is not None:
            if float(self.det_val) > self.spwndc_id.max_val or float(self.det_val) < self.spwndc_id.min_val:
                raise ValidationError({
                    "det_val": ValidationError("Value {} exceeds limits. Max: {}, Min: {}"
                                               .format(self.det_val, self.spwndc_id.max_val, self.spwndc_id.min_val))
                })

    def is_numeric(self):
        if self.spwndc_id.min_val is not None and self.spwndc_id.max_val is not None:
            return True
        else:
            return False


class SpawnDetCode(BioLookup):
    # spwndc tag
    min_val = models.DecimalField(blank=True, null=True, max_digits=11, decimal_places=5,
                                  verbose_name=_("Minimum Value"), db_column="MIN_VAL")
    max_val = models.DecimalField(blank=True, null=True, max_digits=11, decimal_places=5,
                                  verbose_name=_("Maximum Value"), db_column="MAX_VAL")
    unit_id = models.ForeignKey("UnitCode", on_delete=models.CASCADE, null=True, blank=True, db_column="UNIT_ID",
                                verbose_name=_("Units"))
    spwn_subj_flag = models.BooleanField(verbose_name=_("Subjective?"), db_column="SPAWN_SUBJ_FLAG")


class SpawnDetSubjCode(BioLookup):
    # spwnsc tag
    spwndc_id = models.ForeignKey('SpawnDetCode', on_delete=models.CASCADE, verbose_name=_("Spawn Detail Code"))


class SpeciesCode(BioModel):
    # spec tag
    name = models.CharField(max_length=10, verbose_name=_("Species Name"), db_column="SPEC_SHORT")
    species = models.CharField(max_length=100, verbose_name=_("Species"), db_column="SPECIES")
    com_name = models.CharField(max_length=35, null=True, blank=True, verbose_name=_("Species Common Name"),
                                db_column="COMMON_NAME")

    def __str__(self):
        return self.name


class StockCode(BioLookup):
    # stok tag
    pass


class SubRiverCode(BioLookup):
    # subr tag
    # make name not unique
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    rive_id = models.ForeignKey('RiverCode', on_delete=models.CASCADE, verbose_name=_("River"), db_column="RIVER_ID")
    trib_id = models.ForeignKey('Tributary', on_delete=models.CASCADE, null=True, blank=True, db_column="TRIB_ID",
                                verbose_name=_("Tributary"))

    class Meta:
        unique_together = (('name', 'rive_id', 'trib_id'),)

    def __str__(self):
        return "{} - {}".format(self.rive_id.name, self.name)

    def clean(self):
        super(SubRiverCode, self).clean()
        if self.trib_id and self.rive_id != self.trib_id:
            raise ValidationError({
                "trib_id": ValidationError("Tributary River {} must match River {}"
                                           .format(self.trib_id.rive_id, self.rive_id))
            })


class Tank(BioCont):
    # tank tag
    key = "tank"
    facic_id = models.ForeignKey('FacilityCode', on_delete=models.CASCADE, verbose_name=_("Facility"), db_column="FAC_ID")

    class Meta:
        unique_together = (('name', 'facic_id'),)
        ordering = ['facic_id', 'name']


class TankDet(BioContainerDet):
    # tankd tag
    tank_id = models.ForeignKey('Tank', on_delete=models.CASCADE, verbose_name=_("Tank"), db_column="TANK_ID")

    class Meta:
        unique_together = (('tank_id', 'contdc_id', 'start_date'),)

    def __str__(self):
        return "{} - {}".format(self.tank_id.__str__(), self.contdc_id.__str__())

    def save(self,  *args, **kwargs):
        """ Need to set all earlier details with the same code to invalid"""
        if self.det_valid:
            old_tankd_set = TankDet.objects.filter(tank_id=self.tank_id, contdc_id=self.contdc_id, cdsc_id=self.cdsc_id,
                                                   det_valid=True, start_date__lte=self.start_date)
            for old_tankd in old_tankd_set:
                if old_tankd:
                    old_tankd = old_tankd.get()
                    old_tankd.det_valid = False
                    old_tankd.end_date = self.start_date
                    old_tankd.save()

            current_tankd_set = TankDet.objects.filter(tank_id=self.tank_id, contdc_id=self.contdc_id,
                                                       cdsc_id=self.cdsc_id, det_valid=True,
                                                       start_date__gt=self.start_date)
            for current_tankd in current_tankd_set:
                if current_tankd:
                    self.det_valid = False

        super(TankDet, self).save(*args, **kwargs)


class TeamXRef(BioModel):
    # team tag
    perc_id = models.ForeignKey("PersonnelCode", on_delete=models.CASCADE, verbose_name=_("Team Member"),
                                limit_choices_to={'perc_valid': True})
    role_id = models.ForeignKey("RoleCode", blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Role Code"))
    evnt_id = models.ForeignKey("Event", on_delete=models.CASCADE, verbose_name=_("Event"))
    loc_id = models.ForeignKey("Location", blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Location"))

    class Meta:
        unique_together = (('perc_id', 'role_id', 'evnt_id', 'loc_id'),)


class Tray(BioCont):
    # tray tag
    key = "tray"

    class Meta:
        unique_together = (('name', 'trof_id', 'start_date'),)
        ordering = ['trof_id', 'name']

    # Make name not unique, is unique together with trough code.
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    trof_id = models.ForeignKey('Trough', on_delete=models.CASCADE, related_name="trays", verbose_name=_("Trough"),
                                db_column="TROUGH_ID")
    start_date = models.DateField(verbose_name=_("Start Date"), db_column="START_DATE")
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"), db_column="END_DATE")

    def degree_days(self, start_date=None, end_date=None):
        if not start_date:
            start_date = self.start_date
        if not end_date:
            end_date = self.end_date
        if end_date:
            degree_days = self.trof_id.degree_days(start_date, end_date)
        else:
            degree_days = self.trof_id.degree_days(start_date, timezone.now().date())
        return degree_days

    def __str__(self):
        return "TR{}-{}".format(self.trof_id.__str__(), self.name)

    @property
    def facic_id(self):
        return self.trof_id.facic_id


class TrayDet(BioContainerDet):
    # trayd tag
    tray_id = models.ForeignKey('Tray', on_delete=models.CASCADE, verbose_name=_("Tray"), db_column="TRAY_ID")

    class Meta:
        unique_together = (('tray_id', 'contdc_id', 'start_date'),)

    def __str__(self):
        return "{} - {}".format(self.tray_id.__str__(), self.contdc_id.__str__())


class Tributary(BioLookup):
    # trib tag
    # make name not unique
    name = models.CharField(max_length=255, verbose_name=_("name (en)"))
    rive_id = models.ForeignKey('RiverCode', on_delete=models.CASCADE, verbose_name=_("River"), db_column="RIVER_ID")
    subr_id = models.ForeignKey('SubRiverCode', on_delete=models.CASCADE, null=True, blank=True,
                                db_column="SUBRIVER_ID", verbose_name=_("Subriver"))

    class Meta:
        unique_together = (('name', 'rive_id', 'subr_id'),)

    def clean(self):
        super(Tributary, self).clean()
        if self.subr_id and self.rive_id != self.subr_id.rive_id:
            raise ValidationError({
                "subr_id": ValidationError("Sub River river {} must match River {}"
                                           .format(self.subr_id.rive_id, self.rive_id))
            })


class Trough(BioCont):
    # trof tag
    key = "trof"
    facic_id = models.ForeignKey('FacilityCode', on_delete=models.CASCADE, verbose_name=_("Facility"), db_column="FAC_ID")

    class Meta:
        unique_together = (('name', 'facic_id'),)
        ordering = ['facic_id', 'name']

    def degree_days(self, start_date, end_date):
        start_datetime = naive_to_aware(start_date)
        end_datetime = naive_to_aware(end_date)
        env_qs = EnvCondition.objects.filter(contx_id__trof_id=self,
                                             start_datetime__gte=start_datetime,
                                             start_datetime__lte=end_datetime,
                                             envc_id__name="Temperature")

        delta = end_datetime - start_datetime
        temp_list = []
        for i in range(delta.days + 1):
            day = start_datetime.date() + timedelta(days=i)
            day_temps = []
            for env in env_qs:
                if env.start_datetime.date() == day:
                    day_temps.append(env.env_val)
            if day_temps:
                temp_list.append(round(sum(day_temps) / len(day_temps), 3))

        return temp_list


class TroughDet(BioContainerDet):
    # trofd tag
    trof_id = models.ForeignKey('Trough', on_delete=models.CASCADE, verbose_name=_("Trough"), db_column="TROUGH_ID")

    class Meta:
        unique_together = (('trof_id', 'contdc_id', 'start_date'),)

    def __str__(self):
        return "{} - {}".format(self.trof_id.__str__(), self.contdc_id.__str__())


class UnitCode(BioLookup):
    # unit tag
    pass
