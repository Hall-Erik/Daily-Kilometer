from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import timedelta
from .models import Run


class RunCreateViewTests(TestCase):
    pass  # gotta tinker with the view a bit first.


class RunDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'test', 'test@test.org', 'python123')

    def test_run_with_duration(self):
        '''
        Run information should appear on the detail page.
        '''
        run = Run(distance=3.1, units='km',
                  user_id=self.user.id, duration=timedelta(minutes=15))
        run.save()
        response = self.client.get(
            reverse('runs:detail', kwargs={'pk': run.id}))
        self.assertContains(response, run.date.strftime('%Y-%m-%d'))
        self.assertContains(response, run.distance)
        self.assertContains(response, run.units)
        self.assertContains(response, run.duration)

    def test_run_with_no_duration(self):
        '''
        Run information should appear on the detail page.
        If a duration was not saved for this run, an empty
        duration (e.g. 0:00:00) should not appear.
        '''
        run = Run(distance=3.1, units='km', user_id=self.user.id)
        run.save()
        response = self.client.get(
            reverse('runs:detail', kwargs={'pk': run.id}))
        self.assertContains(response, run.date.strftime('%Y-%m-%d'))
        self.assertContains(response, run.distance)
        self.assertContains(response, run.units)
        self.assertNotContains(response, run.duration)

    def test_anon_user_cannot_update_delete(self):
        '''
        Edit and Delete buttons are not available to anonymous
        users.
        '''
        run = Run(distance=3.1, units='km',
                  user_id=self.user.id, duration=timedelta(minutes=15))
        run.save()
        response = self.client.get(
            reverse('runs:detail', kwargs={'pk': run.id}))
        update_url = reverse('runs:update', kwargs={'pk': run.id})
        delete_url = reverse('runs:delete', kwargs={'pk': run.id})
        self.assertNotContains(response, f'href="{update_url}"')
        self.assertNotContains(response, f'href="{delete_url}"')

    def test_non_owner_cannot_edit_delete(self):
        '''
        Edit and Delete buttons are not available to users that
        did not create the run.
        '''
        User.objects.create_user('steve', 's@s.com', 'blahblah')
        run = Run(distance=3.1, units='km', user_id=self.user.id)
        run.save()
        self.client.login(username='steve', password='blahblah')
        response = self.client.get(
            reverse('runs:detail', kwargs={'pk': run.id}))
        update_url = reverse('runs:update', kwargs={'pk': run.id})
        delete_url = reverse('runs:delete', kwargs={'pk': run.id})
        self.assertNotContains(response, f'href="{update_url}"')
        self.assertNotContains(response, f'href="{delete_url}"')


class RunUpdateViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', None, 'python123')
        self.run = user.run_set.create(distance=100, units='mi')

    def test_anon_user_redirected(self):
        '''
        Anonymous user should get redirected (302 status)
        '''
        response = self.client.get(reverse(
            'runs:update', kwargs={'pk': self.run.id}))
        self.assertEqual(response.status_code, 302)

    def test_other_user_forbidden(self):
        '''
        User who did not author run is forbidden.
        '''
        User.objects.create_user('steve', None, 'python123')
        self.client.login(username='steve', password='python123')
        response = self.client.get(reverse(
            'runs:update', kwargs={'pk': self.run.id}))
        self.assertEqual(response.status_code, 403)

    def test_author_ok(self):
        '''
        The author of the run can access this view.
        '''
        self.client.login(username='test', password='python123')
        response = self.client.get(reverse(
            'runs:update', kwargs={'pk': self.run.id}))
        self.assertEqual(response.status_code, 200)


class RunDeleteViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', None, 'python123')
        self.run = user.run_set.create(distance=100, units='mi')

    def test_anon_user_redirected(self):
        '''
        Anonymous user should get redirected (302 status)
        '''
        response = self.client.get(reverse(
            'runs:delete', kwargs={'pk': self.run.id}))
        self.assertEqual(response.status_code, 302)

    def test_other_user_forbidden(self):
        '''
        User who did not author run is forbidden.
        '''
        User.objects.create_user('steve', None, 'python123')
        self.client.login(username='steve', password='python123')
        response = self.client.get(reverse(
            'runs:delete', kwargs={'pk': self.run.id}))
        self.assertEqual(response.status_code, 403)

    def test_author_ok(self):
        '''
        The author of the run can access this view.
        '''
        self.client.login(username='test', password='python123')
        response = self.client.get(reverse(
            'runs:delete', kwargs={'pk': self.run.id}))
        self.assertEqual(response.status_code, 200)


class GearCreateViewTests(TestCase):
    def test_anon_user_redirected(self):
        '''
        Anonymous user should get redirected (302 status)
        '''
        response = self.client.get(reverse('runs:gear-create'))
        self.assertEqual(response.status_code, 302)

    def test_user_ok(self):
        '''
        A user can access this view.
        '''
        User.objects.create_user('test', None, 'python123')
        self.client.login(username='test', password='python123')
        response = self.client.get(reverse('runs:gear-create'))
        self.assertEqual(response.status_code, 200)


class GearListViewTests(TestCase):
    def test_anon_user_redirected(self):
        '''
        Anonymous user should get redirected (302 status)
        '''
        response = self.client.get(reverse('runs:gear-list'))
        self.assertEqual(response.status_code, 302)

    def test_user_ok(self):
        '''
        A user can access this view.
        '''
        User.objects.create_user('test', None, 'python123')
        self.client.login(username='test', password='python123')
        response = self.client.get(reverse('runs:gear-list'))
        self.assertEqual(response.status_code, 200)


class GearDetailViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', None, 'python123')
        self.gear = user.gear_set.create(name='Nike')
        user.run_set.create(distance=5, units='mi', gear=self.gear)

    def test_gear_info_in_response(self):
        '''
        Information about the gear appears in respone
        '''
        response = self.client.get(reverse(
            'runs:gear-detail', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.gear.name)
        self.assertContains(response, self.gear.get_total_miles())

    def test_no_edit_delete_btn_for_anon(self):
        '''
        Edit and delete buttons are not visible to anonymous users.
        '''
        response = self.client.get(reverse(
            'runs:gear-detail', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 200)
        url = reverse('runs:gear-update', kwargs={'pk': self.gear.id})
        self.assertNotContains(response, f'href="{url}"')
        url = reverse('runs:gear-delete', kwargs={'pk': self.gear.id})
        self.assertNotContains(response, f'href="{url}"')

    def test_no_edit_delete_btn_for_other_user(self):
        '''
        Edit and delete buttons are not visible to users who do not
        own the gear.
        '''
        User.objects.create_user('steve', None, '1234')
        self.client.login(username='steve', password='1234')
        response = self.client.get(reverse(
            'runs:gear-detail', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 200)
        url = reverse('runs:gear-update', kwargs={'pk': self.gear.id})
        self.assertNotContains(response, f'href="{url}"')
        url = reverse('runs:gear-delete', kwargs={'pk': self.gear.id})
        self.assertNotContains(response, f'href="{url}"')

    def test_edit_delete_btn_for_owner(self):
        '''
        Edit and delete buttons are visible to owner.
        '''
        self.client.login(username='test', password='python123')
        response = self.client.get(reverse(
            'runs:gear-detail', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 200)
        url = reverse('runs:gear-update', kwargs={'pk': self.gear.id})
        self.assertContains(response, f'href="{url}"')
        url = reverse('runs:gear-delete', kwargs={'pk': self.gear.id})
        self.assertContains(response, f'href="{url}"')


class GearUpdateViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', None, 'python123')
        self.gear = user.gear_set.create(name='Nike')

    def test_anon_user_redirected(self):
        '''
        Anonymous user should get redirected (302 status)
        '''
        response = self.client.get(reverse(
            'runs:gear-update', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 302)

    def test_other_user_forbidden(self):
        '''
        User who does not own the gear is forbidden.
        '''
        User.objects.create_user('steve', None, 'python123')
        self.client.login(username='steve', password='python123')
        response = self.client.get(reverse(
            'runs:gear-update', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 403)

    def test_owner_ok(self):
        '''
        The owner of the gear can access this view.
        '''
        self.client.login(username='test', password='python123')
        response = self.client.get(reverse(
            'runs:gear-update', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 200)


class GearDeleteViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', None, 'python123')
        self.gear = user.gear_set.create(name='Nike')

    def test_anon_user_redirected(self):
        '''
        Anonymous user should get redirected (302 status)
        '''
        response = self.client.get(reverse(
            'runs:gear-delete', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 302)

    def test_other_user_forbidden(self):
        '''
        User who does not own the gear is forbidden.
        '''
        User.objects.create_user('steve', None, 'python123')
        self.client.login(username='steve', password='python123')
        response = self.client.get(reverse(
            'runs:gear-delete', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 403)

    def test_owner_ok(self):
        '''
        The owner of the gear can access this view.
        '''
        self.client.login(username='test', password='python123')
        response = self.client.get(reverse(
            'runs:gear-delete', kwargs={'pk': self.gear.id}))
        self.assertEqual(response.status_code, 200)
