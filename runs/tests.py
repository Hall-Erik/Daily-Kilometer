from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from datetime import timedelta
from .models import Run, Gear
from .serializers import RunSerializer, GearSerializer


def create_user(username="test", email="test@test.com", password="test123"):
    '''Convenience method for creating a user'''
    return User.objects.create_user(
        username=username,
        email=email,
        password=password)


def create_gear(owner, name='Nike', start_distance=5,
                start_units='mi'):
    '''Convenience method for creating a gear'''
    return Gear.objects.create(
        owner=owner,
        name=name,
        start_distance=start_distance,
        start_units=start_units)


def create_run(user, distance=5, units='mi',
               duration=timedelta(seconds=360),
               description=None, run_type=None, gear=None):
    '''Convenience method for creating a run'''
    return Run.objects.create(
        user=user,
        distance=distance,
        units=units,
        duration=duration,
        description=description,
        run_type=run_type,
        gear=None)


class RunViewSetTests(TestCase):
    def test_anon_can_list_runs(self):
        '''Anonymous users can GET a list of runs'''
        user = create_user()
        create_run(user)
        create_run(user, distance=15, units='km')

        # There should be two runs
        self.assertEqual(Run.objects.count(), 2)

        serializer = RunSerializer(Run.objects.all(), many=True)
        url = reverse('runs:run-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_user_can_list_runs(self):
        '''Logged in users can GET a list of runs'''
        client = APIClient()
        user = create_user()
        create_run(user)
        create_run(user, distance=15, units='km')

        # There should be two runs
        self.assertEqual(Run.objects.count(), 2)

        client.force_authenticate(user=user)
        serializer = RunSerializer(Run.objects.all(), many=True)
        url = reverse('runs:run-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_anon_cannot_post_runs(self):
        '''Anonymous user cannot POST a run'''
        url = reverse('runs:run-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Run.objects.count(), 0)

    def test_user_can_post_runs(self):
        '''Logged in user can POST a run'''
        client = APIClient()
        user = create_user()
        # There should be no runs
        self.assertEqual(Run.objects.count(), 0)

        client.force_authenticate(user=user)
        url = reverse('runs:run-list')
        response = client.post(url, {
            'distance': 5,
            'units': 'mi'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Run.objects.count(), 1)

    def test_anon_can_get_run_detail(self):
        '''Anonymous user can GET a run detail'''
        user = create_user()
        run = create_run(user)
        url = reverse('runs:run-detail', kwargs={'id': run.id})
        serializer = RunSerializer(run)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_can_get_run_detail(self):
        '''Logged in user can GET a run detail'''
        client = APIClient()
        owner = create_user()
        run = create_run(owner)
        user = create_user('user', 'user@user.com')
        url = reverse('runs:run-detail', kwargs={'id': run.id})
        serializer = RunSerializer(run)
        client.force_authenticate(user=user)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_owner_can_get_run_detail(self):
        '''Run owner can GET its detail'''
        client = APIClient()
        owner = create_user()
        run = create_run(owner)
        url = reverse('runs:run-detail', kwargs={'id': run.id})
        serializer = RunSerializer(run)
        client.force_authenticate(user=owner)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_anon_cannot_patch_runs(self):
        '''Anonymous user cannot PATCH updates to a run'''
        user = create_user()
        run = create_run(user)
        url = reverse('runs:run-detail', kwargs={'id': run.id})
        response = self.client.patch(url, {
            'units': 'km'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        del run.units  # force refresh from db
        self.assertEqual(run.units, 'mi')

    def test_user_cannot_patch_runs(self):
        '''Non owner user cannot PATCH updates to a run'''
        client = APIClient()
        owner = create_user()
        run = create_run(owner)
        user = create_user('user', 'user@user.com')
        client.force_authenticate(user=user)
        url = reverse('runs:run-detail', kwargs={'id': run.id})
        response = client.patch(url, {
            'units': 'km'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        del run.units  # force refresh from db
        self.assertEqual(run.units, 'mi')

    def test_owner_can_patch_runs(self):
        '''Owner can PATCH updates to a run'''
        client = APIClient()
        owner = create_user()
        run = create_run(owner)
        client.force_authenticate(user=owner)
        url = reverse('runs:run-detail', kwargs={'id': run.id})
        response = client.patch(url, {
            'units': 'km'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        del run.units  # force refresh from db
        self.assertEqual(run.units, 'km')

    def test_annon_cannot_delete_run(self):
        '''Anonymous user cannot DELETE a run'''
        user = create_user()
        run = create_run(user)
        url = reverse('runs:run-detail', kwargs={'id': run.id})
        self.assertEqual(Run.objects.count(), 1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Run.objects.count(), 1)

    def test_user_cannot_delete_run(self):
        '''Non owning user cannot DELETE a run'''
        client = APIClient()
        owner = create_user()
        run = create_run(owner)
        user = create_user('user', 'user@user.com')
        client.force_authenticate(user=user)
        url = reverse('runs:run-detail', kwargs={'id': run.id})
        self.assertEqual(Run.objects.count(), 1)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Run.objects.count(), 1)

    def test_owner_can_delete_run(self):
        '''Owner can DELETE a run'''
        client = APIClient()
        owner = create_user()
        run = create_run(owner)
        client.force_authenticate(user=owner)
        url = reverse('runs:run-detail', kwargs={'id': run.id})
        self.assertEqual(Run.objects.count(), 1)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Run.objects.count(), 0)


class GearViewSetTests(TestCase):
    def test_anon_cannot_list_gear(self):
        '''Anonymous users cannot GET a list of gear'''
        user = create_user()
        create_gear(user)
        create_gear(user, name='ASICS')

        # There should be two gear
        self.assertEqual(Gear.objects.count(), 2)

        url = reverse('runs:gear-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_list_gear(self):
        '''Logged in users can GET a list of their own gear'''
        client = APIClient()
        user = create_user()
        create_gear(user)
        create_gear(user, name='ASICS')

        # There should be two runs
        self.assertEqual(Gear.objects.count(), 2)

        client.force_authenticate(user=user)
        serializer = GearSerializer(Gear.objects.all(), many=True)
        url = reverse('runs:gear-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_anon_cannot_post_gear(self):
        '''Anonymous user cannot POST gear'''
        url = reverse('runs:gear-list')
        self.assertEqual(Gear.objects.count(), 0)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Gear.objects.count(), 0)

    def test_user_can_post_gear(self):
        '''Logged in user can POST gear'''
        client = APIClient()
        user = create_user()
        # There should be no runs
        self.assertEqual(Gear.objects.count(), 0)

        client.force_authenticate(user=user)
        url = reverse('runs:gear-list')
        response = client.post(url, {
            'name': 'Saucony',
            'start_distance': 5,
            'start_units': 'km'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Gear.objects.count(), 1)

    def test_anon_cannot_get_gear_detail(self):
        '''Anonymous user cannot GET a gear detail'''
        user = create_user()
        gear = create_gear(user)
        url = reverse('runs:gear-detail', kwargs={'id': gear.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_get_gear_detail(self):
        '''Logged in user cannot GET a gear detail on another user's gear'''
        client = APIClient()
        owner = create_user()
        gear = create_gear(owner)
        user = create_user('user', 'user@user.com')
        url = reverse('runs:gear-detail', kwargs={'id': gear.id})
        client.force_authenticate(user=user)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_get_gear_detail(self):
        '''Gear owner can GET its detail'''
        client = APIClient()
        owner = create_user()
        gear = create_gear(owner)
        url = reverse('runs:gear-detail', kwargs={'id': gear.id})
        serializer = GearSerializer(gear)
        client.force_authenticate(user=owner)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_anon_cannot_patch_gear(self):
        '''Anonymous user cannot PATCH updates to a gear'''
        user = create_user()
        gear = create_gear(user)
        url = reverse('runs:gear-detail', kwargs={'id': gear.id})
        response = self.client.patch(url, {
            'name': 'ASICS'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        del gear.name  # force refresh from db
        self.assertEqual(gear.name, 'Nike')

    def test_user_cannot_patch_gear(self):
        '''Non owner user cannot PATCH updates to a gear'''
        client = APIClient()
        owner = create_user()
        gear = create_gear(owner)
        user = create_user('user', 'user@user.com')
        client.force_authenticate(user=user)
        url = reverse('runs:gear-detail', kwargs={'id': gear.id})
        response = client.patch(url, {
            'name': 'ASICS'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        del gear.name  # force refresh from db
        self.assertEqual(gear.name, 'Nike')

    def test_owner_can_patch_gear(self):
        '''Owner can PATCH updates to a gear'''
        client = APIClient()
        owner = create_user()
        gear = create_gear(owner)
        client.force_authenticate(user=owner)
        url = reverse('runs:gear-detail', kwargs={'id': gear.id})
        response = client.patch(url, {
            'name': 'ASICS'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        del gear.name  # force refresh from db
        self.assertEqual(gear.name, 'ASICS')

    def test_annon_cannot_delete_gear(self):
        '''Anonymous user cannot DELETE gear'''
        user = create_user()
        gear = create_gear(user)
        url = reverse('runs:gear-detail', kwargs={'id': gear.id})
        self.assertEqual(Gear.objects.count(), 1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Gear.objects.count(), 1)

    def test_user_cannot_delete_gear(self):
        '''Non owning user cannot DELETE gear'''
        client = APIClient()
        owner = create_user()
        gear = create_gear(owner)
        user = create_user('user', 'user@user.com')
        client.force_authenticate(user=user)
        url = reverse('runs:gear-detail', kwargs={'id': gear.id})
        self.assertEqual(Gear.objects.count(), 1)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Gear.objects.count(), 1)

    def test_owner_can_delete_gear(self):
        '''Owner can DELETE gear'''
        client = APIClient()
        owner = create_user()
        gear = create_gear(owner)
        client.force_authenticate(user=owner)
        url = reverse('runs:gear-detail', kwargs={'id': gear.id})
        self.assertEqual(Gear.objects.count(), 1)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Gear.objects.count(), 0)
