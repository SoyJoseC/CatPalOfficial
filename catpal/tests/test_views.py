from django import test
from django.http import response
from django.test import TestCase
from django.urls import reverse

from catpal.models import Document, MendeleyGroup

from members.models import User

class AdminGroupsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 15 Mendeley Groups
        number_of_groups = 15

        for group_id in range(number_of_groups):
            MendeleyGroup.objects.create(mendeley_username="Pedro {group_id}",
            mendeley_password='gjogrqrjgoregjoqejg[',
            name='Grupo {group_id}',
            )

    def test_view_exists_at_desired_location(self):
        response = self.client.get(reverse('admin-groups'))
        self.assertEqual(response.status_code, 200)
