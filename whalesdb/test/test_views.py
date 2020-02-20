from django.test import TestCase, tag
from django.urls import reverse_lazy
from django.utils.translation import activate
from django.contrib.auth.models import User, Group

from django.core.files.base import ContentFile
from django.utils.six import BytesIO
from django.conf import settings

from PIL import Image

from whalesdb import views, models, forms

import os


###########################################################################################
# Common Test for all views, this includes checking that a view is accessible or provides
# a redirect if permissions are required to access a view
###########################################################################################
class CommonTest(TestCase):
    test_url = None
    test_expected_template = None
    login_url_base = '/accounts/login_required/?next='
    login_url_en = login_url_base + "/en/"
    login_url_fr = login_url_base + "/fr/"

    # All views should at a minimum have a title field
    def assert_context_fields(self, response):
        self.assertIn("title", response.context)

    # This is a standard view test most classes should run at some point to ensure
    # that a view is reachable and to check permissions/redirect if required
    def assert_view(self, lang='en', test_url=None, expected_template=None, expected_code=200):
        activate(lang)

        response = self.client.get(self.test_url if not test_url else test_url)

        self.assertEquals(expected_code, response.status_code)
        # if it's a 302 redirect
        template = self.test_expected_template if not expected_template else expected_template
        if not expected_code == 302 and expected_template is not None:
            self.assertTemplateUsed(response, template)
        elif expected_code == 302:
            self.assertEqual(expected_code, response.status_code)
            self.assertEqual("{}{}".format(self.login_url_base, self.test_url), response.url)


###########################################################################################
# Index View is a bit different from most views as it is basically just a landing page
###########################################################################################
class TestIndexView(CommonTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:index')
        self.test_expected_template = 'whalesdb/index.html'

    # Users should be able to view the whales index page which corresponds to the whalesdb/index.html template
    @tag('index_view', 'response', 'access')
    def test_index_view_en(self):
        super().assert_view()

    # Users should be able to view the whales index page corresponding to the whalesdb/index.html template, in French
    @tag('index_view', 'response', 'access')
    def test_index_view_fr(self):
        super(). assert_view(lang='fr')

    # The index view should return a context to be used on the index.html template
    # this should consist of a "Sections" dictionary containing sub-sections
    @tag('index_view', 'context')
    def test_index_view_context(self):
        activate('en')

        response = self.client.get(self.test_url)

        # expect to see section in the context
        self.assertIn("section", response.context)

        # expect to see an 'entry form' section as the first element of section
        entry_forms = response.context['section'][0]

        self.assertEquals('Entry Forms', entry_forms['title'])

        # Expected there to be a station list object
        stn_list = entry_forms['forms'][0]
        self.assertEquals('Station List', stn_list['title'])

        # Expected there to be a project list object
        prj_list = entry_forms['forms'][1]
        self.assertEquals('Project List', prj_list['title'])

        # Expected there to be a project list object
        mor_list = entry_forms['forms'][2]
        self.assertEquals('Mooring Setup List', mor_list['title'])


###########################################################################################
# List Test contain tests used from common Test also adding tests specific for list/filter views
###########################################################################################
class CommonListTest(CommonTest):

    def setUp(self):
        super().setUp()

        self.test_expected_template = 'whalesdb/whale_filter.html'

    # List context should return:
    #   - a title to display in the html template
    #   - a list of fields to display
    #   - a url to use for the create button
    #   - a url to use for the detail links
    def assert_list_view_context_fields(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)
        self.assertIn("fields", response.context)
        self.assertIn("create_url", response.context)
        self.assertIn("details_url", response.context)

        # determine if a user is logged in and has access to see "add" button
        self.assertIn("auth", response.context)

        return response


class TestListStation(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_stn')

    # User should be able to view lists without login required
    @tag('stn_list', 'response', 'access')
    def test_stn_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('stn_list', 'response', 'access')
    def test_stn_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    # The station view should use create_stn and details_stn for the create and details buttons
    @tag('stn_list', 'response', 'context')
    def test_stn_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_stn", response.context['create_url'])
        self.assertEqual("whalesdb:details_stn", response.context['details_url'])
        self.assertEqual("whalesdb:update_stn", response.context['update_url'])


class TestListProject(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_prj')

    # User should be able to view lists without login required
    @tag('prj_list', 'response', 'access')
    def test_prj_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('prj_list', 'response', 'access')
    def test_prj_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    # The project view should use create_mor and details_prj for the create and details buttons
    @tag('prj_list', 'response', 'context')
    def test_prj_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_prj", response.context['create_url'])
        self.assertEqual("whalesdb:details_prj", response.context['details_url'])
        self.assertEqual("whalesdb:update_prj", response.context['update_url'])


class TestListMooring(CommonListTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:list_mor')

    # User should be able to view lists without login required
    @tag('mor_list', 'response', 'access')
    def test_mor_list_en(self):
        super().assert_view()

    # User should be able to view lists without login required
    @tag('mor_list', 'response', 'access')
    def test_mor_list_fr(self):
        super().assert_view(lang='fr')

    # make sure project list context returns expected context objects
    # The mooring view should use create_mor and details_mor for the create and details buttons
    @tag('mor_list', 'response', 'context')
    def test_mor_list_context_fields(self):
        response = super().assert_list_view_context_fields()

        self.assertEqual("whalesdb:create_mor", response.context['create_url'])
        self.assertEqual("whalesdb:details_mor", response.context['details_url'])
        self.assertEqual("whalesdb:update_mor", response.context['update_url'])


###########################################################################################
# Create Tests include tests from common tests also adding tests for views extending the Create View
###########################################################################################
class CommonCreateTest(CommonTest):

    expected_form = None
    expected_view = None
    expected_success_url = reverse_lazy("whalesdb:close_me")
    data = None
    test_password = "test1234"

    def setUp(self):
        super().setUp()

        # CreateViews intended to be used from a views.ListCommon should use the _entry_form.html template
        self.test_expected_template = 'whalesdb/_entry_form.html'

    # use when a user needs to be logged in.
    def login_regular_user(self):
        user = User.objects.create_user(username="Regular", first_name="Joe", last_name="Average",
                                                     email="Average.Joe@dfo-mpo.gc.ca", password=self.test_password)
        user.save()

        self.client.login(username=user.username, password=self.test_password)

        return user

    # use when a user needs to be logged in.
    def login_whale_user(self):
        whale_group = Group(name="whalesdb_admin")
        whale_group.save()

        user = User.objects.create_user(username="Whale", first_name="Hump", last_name="Back",
                                                     email="Hump.Back@dfo-mpo.gc.ca", password=self.test_password)
        user.groups.add(whale_group)
        user.save()

        self.client.login(username=user.username, password=self.test_password)

        return user

    # If a user is logged in and not in 'whalesdb_admin' they should be get a 403 restriction
    def assert_logged_in_not_access(self):
        regular_user = self.login_regular_user()

        self.assertEqual(int(self.client.session['_auth_user_id']), regular_user.pk)

        super().assert_view(expected_code=403)

    # If a user is logged in and in 'whalesdb_admin' they should not be redirected
    def assert_logged_in_has_access(self):
        whale_user = self.login_whale_user()

        self.assertEqual(int(self.client.session['_auth_user_id']), whale_user.pk)

        super().assert_view()

    # check that the creation view is using the correct form
    def assert_create_form(self):
        activate("en")

        view = self.expected_view

        self.assertEquals(self.expected_form, view.form_class)

    # All CommonCreate views should at a minimum have a title.
    # This will return the response for other create view tests to run further tests on context if required
    def assert_create_view_context_fields(self):
        activate('en')

        self.login_whale_user()
        response = self.client.get(self.test_url)

        super().assert_context_fields(response)

        return response

    # test that upon a successful form the view redirects to the expected success url
    #   - Requires: self.test_url
    #   - Requires: self.data
    #   - Requires: self.expected_success_url
    def assert_successful_url(self):
        activate('en')

        self.login_whale_user()
        response = self.client.post(self.test_url, self.data)

        self.assertRedirects(response=response, expected_url=self.expected_success_url)


class TestCreateProject(CommonCreateTest):
    data = {
        "prj_name": 'PRJ_001',
        "prj_description": "Some project description here",
        "prj_url": "https//noneOfYourBusiness.com"
    }

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:create_prj')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'whalesdb/_entry_form.html'

        self.expected_view = views.CreatePrj

        self.expected_form = forms.PrjForm

    # Users must be logged in to create new objects
    @tag('create_prj', 'response', 'access')
    def test_create_prj_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('create_prj', 'response', 'access')
    def test_create_prj_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the _entry_form.html template
    @tag('create_prj', 'response', 'access')
    def test_create_prj_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('create_prj', 'form')
    def test_create_prj_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('create_prj', 'context')
    def test_create_prj_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('create_prj', 'redirect')
    def test_create_prj_successful_url(self):
        super().assert_successful_url()


class TestCreateStation(CommonCreateTest):
    data = {
            "stn_name": "STN_001",
            "stn_code": "STN",
            "stn_revision": "1",
            "stn_planned_lat": "25",
            "stn_planned_lon": "50",
            "stn_planned_depth": "10",
            "stn_notes": "Some Notes"
        }

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:create_stn')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'whalesdb/_entry_form.html'

        self.expected_view = views.CreateStn

        self.expected_form = forms.StnForm

    # Users must be logged in to create new stations
    @tag('create_stn', 'response', 'access')
    def test_create_stn_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new stations
    @tag('create_stn', 'response', 'access')
    def test_create_stn_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the _entry_form.html template
    @tag('create_stn', 'response', 'access')
    def test_create_stn_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('create_stn', 'form')
    def test_create_stn_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('create_stn', 'context')
    def test_create_stn_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('create_stn', 'redirect')
    def test_create_stn_successful_url(self):
        super().assert_successful_url()


class TestCreateMooring(CommonCreateTest):

    img_file_name = None
    img_file_path = None

    data = {
        "mor_name": "MOR_001",
        "mor_max_depth": "10",
        "mor_link_setup_image": "https://somelink.com/images/img001.png",
        "mor_additional_equipment": "None",
        "mor_general_moor_description": "This is a mooring description",
        "more_notes": "Notes",
    }

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:create_mor')

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'whalesdb/_entry_form.html'

        self.expected_view = views.CreateMor
        self.expected_form = forms.MorForm

        self.img_file_name = "MooringSetupTest.png"
        self.img_file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + self.img_file_name

        data = BytesIO()
        Image.open(self.img_file_path).save(data, "PNG")
        data.seek(0)

        file = ContentFile(data.read(), self.img_file_name)
        # add the image to the data array
        self.data['mor_setup_image'] = self.img_file_path

    # Users must be logged in to create new objects
    @tag('create_mor', 'response', 'access')
    def test_create_mor_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to create new objects
    @tag('create_mor', 'response', 'access')
    def test_create_mor_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the _entry_form.html template
    @tag('create_mor', 'response', 'access')
    def test_create_mor_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('create_mor', 'form')
    def test_create_mor_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('create_mor', 'context')
    def test_create_mor_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('create_mor', 'redirect')
    def test_create_mor_successful_url(self):
        super().assert_successful_url()


###########################################################################################
# Common update test has access to tests from Common Creation tests also adding test specific to
# views extending UpdateView
###########################################################################################
class CommonUpdateTest(CommonCreateTest):
    pass


class TestUpdateStn(CommonUpdateTest):
    data = {
            "stn_name": "STN_001",
            "stn_code": "STN",
            "stn_revision": "1",
            "stn_planned_lat": "25",
            "stn_planned_lon": "50",
            "stn_planned_depth": "10",
            "stn_notes": "Some Notes"
        }

    def setUp(self):
        super().setUp()

        obj = models.StnStation(
            stn_name=self.data['stn_name'],
            stn_code=self.data['stn_code'],
            stn_revision=self.data['stn_revision'],
            stn_planned_lat=self.data['stn_planned_lat'],
            stn_planned_lon=self.data['stn_planned_lon'],
            stn_planned_depth=self.data['stn_planned_depth'],
            stn_notes=self.data['stn_notes']
        )
        obj.save()

        self.test_url = reverse_lazy('whalesdb:update_stn', args=(obj.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'whalesdb/_entry_form.html'

        self.expected_view = views.UpdateStn

        self.expected_form = forms.StnForm

    # Users must be logged in to create new stations
    @tag('update_stn', 'response', 'access')
    def test_update_stn_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update stations
    @tag('update_stn', 'response', 'access')
    def test_update_stn_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the _entry_form.html template
    @tag('update_stn', 'response', 'access')
    def test_update_stn_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('update_stn', 'form')
    def test_update_stn_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('update_stn', 'context')
    def test_update_stn_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('update_stn', 'redirect')
    def test_update_stn_successful_url(self):
        super().assert_successful_url()


class TestUpdatePrj(CommonUpdateTest):
    data = {
        "prj_name": 'PRJ_001',
        "prj_description": "Some project description here",
        "prj_url": "https//noneOfYourBusiness.com"
    }

    def setUp(self):
        super().setUp()

        obj = models.PrjProject(
            prj_name=self.data['prj_name'],
            prj_description=self.data['prj_description'],
            prj_url=self.data['prj_url'],
        )
        obj.save()

        self.test_url = reverse_lazy('whalesdb:update_prj', args=(obj.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'whalesdb/_entry_form.html'

        self.expected_view = views.UpdatePrj

        self.expected_form = forms.PrjForm

    # Users must be logged in to create new stations
    @tag('update_prj', 'response', 'access')
    def test_update_prj_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update stations
    @tag('update_prj', 'response', 'access')
    def test_update_prj_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the _entry_form.html template
    @tag('update_prj', 'response', 'access')
    def test_update_prj_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('update_prj', 'form')
    def test_update_prj_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('update_prj', 'context')
    def test_update_prj_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('update_prj', 'redirect')
    def test_update_prj_successful_url(self):
        super().assert_successful_url()


class TestUpdateMor(CommonUpdateTest):
    data = {
        "mor_name": "MOR_001",
        "mor_max_depth": "10",
        "mor_link_setup_image": "https://somelink.com/images/img001.png",
        "mor_additional_equipment": "None",
        "mor_general_moor_description": "This is a mooring description",
        "more_notes": "Notes",
    }

    def setUp(self):
        super().setUp()

        obj = models.MorMooringSetup(
            mor_name=self.data['mor_name'],
            mor_max_depth=self.data['mor_max_depth'],
            mor_link_setup_image=self.data['mor_link_setup_image'],
            mor_additional_equipment=self.data['mor_additional_equipment'],
            mor_general_moor_description=self.data['mor_general_moor_description'],
            more_notes=self.data['more_notes'],
        )
        obj.save()

        self.test_url = reverse_lazy('whalesdb:update_mor', args=(obj.pk,))

        # Since this is intended to be used as a pop-out form, the html file should start with an underscore
        self.test_expected_template = 'whalesdb/_entry_form.html'

        self.expected_view = views.UpdateMor

        self.expected_form = forms.MorForm

    # Users must be logged in to create new stations
    @tag('update_mor', 'response', 'access')
    def test_update_mor_en(self):
        super().assert_view(expected_code=302)

    # Users must be logged in to update stations
    @tag('update_mor', 'response', 'access')
    def test_update_mor_fr(self):
        super().assert_view(lang='fr', expected_code=302)

    # Logged in user in the whalesdb_admin group should get to the _entry_form.html template
    @tag('update_mor', 'response', 'access')
    def test_update_mor_en_access(self):
        # ensure a user not in the whalesdb_admin group cannot access creation forms
        super().assert_logged_in_not_access()

        # ensure a user in the whales_db_admin group can access creation forms
        super().assert_logged_in_has_access()

    # Test that projects is using the project form
    @tag('update_mor', 'form')
    def test_update_mor_form(self):
        super().assert_create_form()

    # test that the context is returning the required context fields
    # at a minimum this should include a title field
    # Each view might require specific context fields
    @tag('update_mor', 'context')
    def test_update_mor_context_fields(self):
        super().assert_create_view_context_fields()

    # test that given some valid data the view will redirect to the list
    @tag('update_mor', 'redirect')
    def test_update_mor_successful_url(self):
        super().assert_successful_url()


###########################################################################################
# Common Detail test includes tests from Common Test also adding tests specific for views extending DetailsView
###########################################################################################
class CommonDetailsTest(CommonTest):

    fields = []
    _details_dict = None

    def createDict(self):
        pass

    # used to destroy test objects created during a test
    def tearDown(self) -> None:
        _details_dict = self.createDict()

        for key in self._details_dict:
            _details_dict[key].delete()

    def assert_field_in_fields(self, response):
        for field in self.fields:
            self.assertIn(field, response.context['fields'])

    def assert_context_fields(self, response):
        super().assert_context_fields(response)

        self.assertIn("list_url", response.context)
        self.assertIn("update_url", response.context)


class TestDetailsStation(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        stn_1 = models.StnStation(stn_name='Station 1', stn_code='ST1', stn_revision=1, stn_planned_lat=52,
                                  stn_planned_lon=25, stn_planned_depth=1)
        stn_1.save()

        self._details_dict['stn_1'] = stn_1

        return self._details_dict

    def setUp(self):
        super().setUp()

        stn_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_stn', args=(stn_dic['stn_1'].pk,))
        self.test_expected_template = 'whalesdb/station_details.html'
        self.fields = ['stn_name', 'stn_code', 'stn_revision', 'stn_planned_lat', 'stn_planned_lon',
                       'stn_planned_depth', 'stn_notes']

    # Station Details are visible to all
    @tag('details_stn', 'response', 'access')
    def test_details_stn_en(self):
        super().assert_view(expected_template='whalesdb/stnstation_detail.html')

    # Station Details are visible to all
    @tag('details_stn', 'response', 'access')
    def test_details_stn_fr(self):
        super().assert_view(lang='fr', expected_template='whalesdb/stnstation_detail.html')

    # Test that the context contains the proper fields
    @tag('details_stn', 'context')
    def test_context_fields_stn(self):
        activate('fr')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)
        self.assertEqual(response.context['list_url'], 'whalesdb:list_stn')
        self.assertEqual(response.context['update_url'], 'whalesdb:update_stn')

        self.assertEqual(response.context['object'], self.createDict()['stn_1'])
        super().assert_field_in_fields(response)


class TestDetailsMooring(CommonDetailsTest):

    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        img_file_name = "MooringSetupTest.png"
        img_file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + img_file_name

        data = BytesIO()
        Image.open(img_file_path).save(data, "PNG")
        data.seek(0)

        file = ContentFile(data.read(), img_file_name)

        mor_1 = models.MorMooringSetup(mor_name="MOR001", mor_max_depth=100,
                                       mor_link_setup_image="https://somelink.com",
                                       mor_setup_image=file)
        mor_1.save()

        self._details_dict['mor_1'] = mor_1

        return self._details_dict

    def setUp(self):
        super().setUp()

        mor_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_mor', args=(mor_dic['mor_1'].pk,))
        self.test_expected_template = 'whalesdb/mormooringsetup_detail.html'
        self.fields = ['mor_name', 'mor_max_depth', 'mor_link_setup_image', 'mor_additional_equipment',
                       'mor_general_moor_description', 'more_notes']

    # Station Details are visible to all
    @tag('details_mor', 'response', 'access')
    def test_details_mor_en(self):
        super().assert_view()

    # Station Details are visible to all
    @tag('details_mor', 'response', 'access')
    def test_details_mor_fr(self):
        super().assert_view(lang='fr')

    # Test that the context contains the proper fields
    @tag('details_mor', 'context')
    def test_context_fields_mor(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)
        self.assertEqual(response.context['list_url'], 'whalesdb:list_mor')
        self.assertEqual(response.context['update_url'], 'whalesdb:update_mor')

        self.assertEqual(response.context["object"], self.createDict()['mor_1'])
        super().assert_field_in_fields(response)


class TestDetailsProject(CommonDetailsTest):
    def createDict(self):
        if self._details_dict:
            return self._details_dict

        self._details_dict = {}

        prj_1 = models.PrjProject(prj_name="Project 1", prj_description="Sample Project",
                                  prj_url="http://someproject.com")
        prj_1.save()

        self._details_dict['prj_1'] = prj_1

        return self._details_dict

    def setUp(self):
        super().setUp()

        stn_dic = self.createDict()

        self.test_url = reverse_lazy('whalesdb:details_prj', args=(stn_dic['prj_1'].pk,))
        self.test_expected_template = 'whalesdb/whales_detail.html'

    # Project Details are visible to all
    @tag('details_prj', 'response', 'access')
    def test_details_prj_en(self):
        super().assert_view()

    # Project Details are visible to all
    @tag('details_prj', 'response', 'access')
    def test_details_prj_fr(self):
        super().assert_view(lang='fr')

    # Test that the context contains the proper fields
    @tag('details_prj', 'context')
    def test_context_fields_prj(self):
        activate('en')

        response = self.client.get(self.test_url)

        super().assert_context_fields(response)
        self.assertEqual(response.context['list_url'], 'whalesdb:list_prj')
        self.assertEqual(response.context['update_url'], 'whalesdb:update_prj')

        self.assertEqual(response.context['object'], self.createDict()['prj_1'])
        super().assert_field_in_fields(response)