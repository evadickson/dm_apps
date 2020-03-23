import requests
import unicodecsv as csv
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, TemplateView, FormView, ListView
from django_filters.views import FilterView
from shapely.geometry import box

from . import models
from . import forms
from . import filters


class SpringCleanupRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return True

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)


class IndexTemplateView(SpringCleanupRequiredMixin, ListView):
    template_name = 'spring_cleanup/index.html'
    model = models.Route

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["google_api_key"] = settings.GOOGLE_API_KEY
        # messages.success(self.request, _("Click on an area!"))
        return context


class RouteDetailView(LoginRequiredMixin, DetailView):
    model = models.Route

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["google_api_key"] = settings.GOOGLE_API_KEY
        context["field_list"] = [
            'id',
            'tdesc|{}'.format(_("Description")),
            'recommended_people',
            'estimated_time_required',
            'approx_area|{}'.format(_("approximate area (km.sq.)")),
        ]
        # messages.success(self.request, _("Click on an area!"))
        return context