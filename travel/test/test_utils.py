from django.test import tag
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import activate

from shared_models.test.SharedModelsFactoryFloor import UserFactory
from travel.test import FactoryFloor
from travel.test.common_tests import CommonTravelTest as CommonTest
from travel.views import can_modify_request
from .. import utils

class UtilsTest(CommonTest):

    def setUp(self):
        super().setUp()  # used to import fixutres

    @tag("utils", 'can_modify')
    def test_can_modify_rules(self):
        activate('en')

        # actors
        trip_request = FactoryFloor.IndividualTripRequestFactory()
        reg_user = self.get_and_login_user()
        admin_user = self.get_and_login_user(in_group="travel_admin")

        # RULE 1: travel admin = True
        self.assertEqual(can_modify_request(admin_user, trip_request.id), True)

        # RULE 2: a current reviewer; they must be able to edit a child trip and the parent trip
        # a)
        my_reviewer = FactoryFloor.ReviewerFactory(trip_request=trip_request, status_id=1)
        self.assertEqual(can_modify_request(my_reviewer.user, trip_request.id), True)
        # b)
        child_trip_request = FactoryFloor.ChildTripRequestFactory()
        parent_trip_request = child_trip_request.parent_request
        my_reviewer = FactoryFloor.ReviewerFactory(trip_request=parent_trip_request, status_id=1)
        self.assertEqual(can_modify_request(my_reviewer.user, child_trip_request.id), True)
        self.assertEqual(can_modify_request(my_reviewer.user, parent_trip_request.id), True)

        # RULE 3: when a trip is unsubmitted, randos cannot edit
        self.assertIsNone(can_modify_request(reg_user, trip_request.id), False)
        # ** THERE IS AN EXCEPTION HERE: if the trip request user is None, then anyone can edit
        trip_request.user = None
        trip_request.save()
        self.assertEqual(can_modify_request(reg_user, trip_request.id), True)
        trip_request.user = UserFactory()
        trip_request.save()

        # RULE 4: when a trip is unsubmitted, owners can edit
        self.assertEqual(can_modify_request(trip_request.user, trip_request.id), True)
        self.assertEqual(can_modify_request(parent_trip_request.user, parent_trip_request.id), True)
        self.assertEqual(can_modify_request(parent_trip_request.user, child_trip_request.id), True)

        # RULE 5: when a trip is unsubmitted, travellers can edit
        self.assertEqual(can_modify_request(child_trip_request.user, child_trip_request.id), True)
        self.assertEqual(can_modify_request(child_trip_request.user, parent_trip_request.id), True)

        # RULE 6: owners are always able to unsubmit a trip
        trip_request.submitted = timezone.now()
        trip_request.save()
        self.assertEqual(can_modify_request(trip_request.user, trip_request.id, True), True)

    @tag("utils", 'get_related_trips')
    def test_get_related_trips(self):
        activate('en')

        # actors
        ind_request = FactoryFloor.IndividualTripRequestFactory()
        child_request = FactoryFloor.ChildTripRequestFactory()
        parent_request = child_request.parent_request
        random_request = FactoryFloor.IndividualTripRequestFactory()

        reg_user = self.get_and_login_user()

        # to start, this user should have 0 trips
        self.assertEqual(utils.get_related_trips(reg_user).count(), 0)

        # setting the individual request to user should result in 1 trip
        ind_request.user = reg_user
        ind_request.save()
        self.assertIn(ind_request, utils.get_related_trips(reg_user))
        self.assertEqual(utils.get_related_trips(reg_user).count(), 1)

        # setting parent of group trip to user should increase by 1...
        parent_request.user = reg_user
        parent_request.save()
        self.assertIn(parent_request, utils.get_related_trips(reg_user))
        self.assertEqual(utils.get_related_trips(reg_user).count(), 2)

        # setting parent of child trip to user should increase by 1...
        child_request.user = reg_user
        child_request.save()
        self.assertIn(child_request, utils.get_related_trips(reg_user))
        self.assertEqual(utils.get_related_trips(reg_user).count(), 3)

        # setting created_by of random trip to user should increase by 1...
        random_request.created_by = reg_user
        random_request.save()
        self.assertIn(random_request, utils.get_related_trips(reg_user))
        self.assertEqual(utils.get_related_trips(reg_user).count(), 4)

