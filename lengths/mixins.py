from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

from .utils import is_admin, is_crud_user


class LengthsBasicMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        if self.request.user.id:
            return True

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result and self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/denied/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = is_admin(self.request.user)
        return context


class AdminRequiredMixin(LengthsBasicMixin):
    def test_func(self):
        return is_admin(self.request.user)


class CRUDRequiredMixin(LengthsBasicMixin):
    def test_func(self):
        return is_crud_user(self.request.user) or is_admin(self.request.user)


class SuperuserOrAdminRequiredMixin(LengthsBasicMixin):
    def test_func(self):
        return self.request.user.is_superuser or is_admin(self.request.user)

#
# class LoginAccessRequiredMixin(CsasBasicRequiredMixin):
#     def test_func(self):
#         if self.request.user.id:
#             return True
#
#
# class CsasNationalAdminRequiredMixin(CsasBasicRequiredMixin):
#     def test_func(self):
#         return in_csas_national_admin_group(self.request.user)
#
#
# class SuperuserOrCsasNationalAdminRequiredMixin(CsasBasicRequiredMixin):
#     def test_func(self):
#         return self.request.user.is_superuser or in_csas_national_admin_group(self.request.user)
#
#
# class CsasAdminRequiredMixin(CsasBasicRequiredMixin):
#     def test_func(self):
#         return in_csas_admin_group(self.request.user) or in_csas_web_pub_group(self.request.user) or in_csas_regional_admin_group(self.request.user)
#
#
# class CsasNCRStaffRequiredMixin(CsasBasicRequiredMixin):
#     def test_func(self):
#         return in_csas_admin_group(self.request.user) or in_csas_web_pub_group(self.request.user)
#
#
# class CanModifyRequestRequiredMixin(CsasBasicRequiredMixin):
#     def test_func(self):
#         # the assumption is that either we are passing in a Project object or an object that has a project as an attribute
#         request_id = None
#         try:
#             obj = self.get_object()
#             if isinstance(obj, models.CSASRequest):
#                 request_id = obj.id
#             elif isinstance(obj, models.CSASRequestReview) or isinstance(obj, models.CSASRequestFile):
#                 request_id = obj.csas_request_id
#
#         except AttributeError:
#             pass
#             if self.kwargs.get("crequest"):
#                 request_id = self.kwargs.get("crequest")
#             # elif self.kwargs.get("project_year"):
#             #     project_year = get_object_or_404(models.ProjectYear, pk=self.kwargs.get("project_year"))
#             #     project_id = project_year.project_id
#
#         finally:
#             if request_id:
#                 return can_modify_request(self.request.user, request_id)
#
#
# class CanModifyProcessRequiredMixin(CsasBasicRequiredMixin):
#     def test_func(self):
#         # the assumption is that either we are passing in a Project object or an object that has a project as an attribute
#         process_id = None
#         try:
#             obj = self.get_object()
#             if isinstance(obj, models.Process):
#                 process_id = obj.id
#             elif isinstance(obj, models.Meeting) or isinstance(obj, models.Document) or isinstance(obj, models.TermsOfReference):
#                 process_id = obj.process.id
#             elif isinstance(obj, models.MeetingFile):
#                 process_id = obj.meeting.process.id
#         except AttributeError:
#             if self.kwargs.get("process"):
#                 process_id = self.kwargs.get("process")
#             elif self.kwargs.get("meeting"):
#                 meeting = get_object_or_404(models.Meeting, pk=self.kwargs.get("meeting"))
#                 process_id = meeting.process_id
#         finally:
#             if process_id:
#                 return can_modify_process(self.request.user, process_id)
