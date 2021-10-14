from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from shared_models.api.views import _get_labels
from shared_models.models import Section
from . import serializers
from .permissions import CanModifyApplicationOrReadOnly
from .. import models, utils


# USER
#######
class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserDisplaySerializer(instance=request.user)
        data = serializer.data
        qp = request.GET
        data["is_admin"] = utils.in_res_admin_group(request.user)
        if qp.get("application"):
            data["can_modify"] = utils.can_modify_application(request.user, qp.get("application"), return_as_dict=True)
        return Response(data)


class ApplicationViewSet(ModelViewSet):
    serializer_class = serializers.ApplicationSerializer
    permission_classes = [CanModifyApplicationOrReadOnly]
    queryset = models.Application.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'section__division__branch__sector__region',
        "section__division__branch__sector",
        "section__division__branch",
        "section__division",
        "section",
        "fiscal_year",
        "status",
    ]


#
# # Observations
# ##############
#
# class ObservationListCreateAPIView(ListCreateAPIView):
#     serializer_class = serializers.ObservationSerializer
#     permission_classes = [permissions.resCRUDOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(section_id=self.request.data["section_id"], created_by=self.request.user)
#
#     def get_queryset(self):
#         qs = models.Observation.objects.order_by("section", "id")
#         qp = self.request.query_params
#
#         if qp.get("dive"):
#             dive = get_object_or_404(models.Dive, pk=qp.get("dive"))
#             qs = qs.filter(section__dive=dive)
#
#         return qs
#
#
# class ObservationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = models.Observation.objects.all()
#     serializer_class = serializers.ObservationSerializer
#     permission_classes = [permissions.resCRUDOrReadOnly]
#
#     def perform_update(self, serializer):
#         serializer.save(updated_by=self.request.user)
#
#
# # Sections
# ##############
#
# class SectionListCreateAPIView(ListCreateAPIView):
#     serializer_class = serializers.SectionSerializer
#     permission_classes = [permissions.resCRUDOrReadOnly]
#
#     def get_queryset(self):
#         qs = models.Section.objects.order_by("dive", "interval")
#         qp = self.request.query_params
#
#         if qp.get("dive"):
#             dive = get_object_or_404(models.Dive, pk=qp.get("dive"))
#             qs = qs.filter(dive=dive)
#
#         return qs
#
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)
#
#
# class SectionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = models.Section.objects.all()
#     serializer_class = serializers.SectionSerializer
#     permission_classes = [permissions.resCRUDOrReadOnly]
#
#     def perform_update(self, serializer):
#         serializer.save(updated_by=self.request.user)


# Lookups


class ApplicationModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.Application

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        data['applicant_choices'] = [dict(text=str(c), value=c.id) for c in User.objects.all()]
        data['group_level_choices'] = [dict(text=str(c), value=c.id) for c in models.GroupLevel.objects.all()]
        data['section_choices'] = [dict(text=c.full_name, value=c.id) for c in Section.objects.all()]
        return Response(data)
