from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Run, Gear
from .forms import RunForm, GearForm


class RunCreateViewTests(TestCase):
    '''
    Okay, this is also the Index view.
    '''
    def setUp(self):
        other = User.objects.create_user('other', None, '1234')
        gear = other.gear_set.create(name='Noke')
        other.run_set.create(
            distance=5, units='km', gear=gear,
            duration=timedelta(minutes=18))
        self.user = User.objects.create_user('test', None, '1234')

    def test_other_users_runs_appear_on_index(self):
        '''
        Runs appear on the index page.
        '''
        respone = self.client.get('/')
        run = Run.objects.first()
        self.assertEqual(respone.context['runs'][0], run)
        self.assertContains(respone, run.distance)
        self.assertContains(respone, run.units)
        self.assertContains(respone, run.gear.name)

    def test_user_gear_appears_in_form(self):
        '''
        A user's gear should appear as an option in the choice field.
        '''
        gear = self.user.gear_set.create(name='ASICS')
        self.client.login(username='test', password='1234')
        response = self.client.get('/')
        self.assertContains(
            response,
            f'<option value="{gear.id}" selected>{gear.name}</option>')

    def test_must_be_logged_in_to_post(self):
        '''
        Must be an authenticated user to save runs.
        '''
        response = self.client.post('/', {
            'distance': 3, 'units': 'mi', 'date': '05/16/2016',
            'duration_1': 20})
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertEqual(Run.objects.count(), 1)

    def test_logged_in_user_can_post(self):
        '''
        Logged in user can add runs
        '''
        self.client.login(username='test', password='1234')
        response = self.client.post('/', {
            'distance': 3, 'units': 'mi', 'date': '05/16/2016',
            'duration_1': 20, 'description': 'Awesome run!'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your run has been saved.')
        self.assertEqual(Run.objects.count(), 2)

    def test_form_must_be_valid_to_save(self):
        '''
        Can't save a run if the form is invalid.
        '''
        self.client.login(username='test', password='1234')
        response = self.client.post('/', {
            'distance': 3, 'units': 'mi', 'date': 'Steve',
            'duration_1': 20}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There was a problem. Please try again.')
        self.assertEqual(Run.objects.count(), 1)


class RunDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'test', 'test@test.org', 'python123')

    def test_run_with_duration(self):
        '''
        Run information should appear on the detail page.
        '''

        d = timezone.datetime(
            year=2019, month=5, day=16,
            tzinfo=timezone.pytz.timezone('America/Denver'))
        run = Run(distance=3.1, units='km', date=d,
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
        d = timezone.datetime(
            year=2019, month=5, day=16,
            tzinfo=timezone.pytz.timezone('America/Denver'))
        run = Run(distance=3.1, units='km', date=d, user_id=self.user.id)
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
        self.run = user.run_set.create(
            distance=100, units='mi', duration=timedelta(minutes=17))

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

    def test_adds_to_user_gear_set(self):
        '''
        Posting valid data to this view adds to the
        user's gear_set.
        '''
        user = User.objects.create_user('test', None, 'python123')
        self.client.login(username='test', password='python123')
        gear_before = user.gear_set.count()
        self.client.post(
            reverse('runs:gear-create'), {
                'name': 'Nike', 'date_added': '05/16/2019'})
        gear_after = user.gear_set.count()
        self.assertGreater(gear_after, gear_before)

    def test_invalid_data_does_not_add_gear(self):
        '''
        Posting invalid data to this view does not add
        to the user's gear_set.
        '''
        user = User.objects.create_user('test', None, 'python123')
        self.client.login(username='test', password='python123')
        gear_before = user.gear_set.count()
        total_gear_before = Gear.objects.count()
        self.client.post(
            reverse('runs:gear-create'), {
                'name': 'Nike', 'date_added': 'Steve'})
        gear_after = user.gear_set.count()
        total_gear_after = Gear.objects.count()
        self.assertEqual(gear_after, gear_before)
        self.assertEqual(total_gear_after, total_gear_before)


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


class RunFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', None, '1234')

    def test_form_valid(self):
        form = RunForm(data={
            'distance': 5,
            'units': 'km',
            'duration': ['', 17, ''],
            'date': '05/16/2019',
            'description': 'Blah blah',
        }, user=self.user)
        self.assertTrue(form.is_valid())

    def test_minimum_valid_form(self):
        form = RunForm(data={
            'distance': 5,
            'units': 'km',
            'date': '05/16/2019'
        }, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = RunForm(data={
            'distance': 'bob',
            'units': 5,
            'duration': ['eighty', 17, ''],
            'date': 'Steve'
        }, user=self.user)
        self.assertFalse(form.is_valid())


class GearFormTests(TestCase):
    def test_form_valid(self):
        form = GearForm(data={
            'name': 'Noke',
            'date_added': '05/16/2019'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = GearForm(data={
            'name': '',
            'date_added': '05/16/2019'
        })
        self.assertFalse(form.is_valid())
