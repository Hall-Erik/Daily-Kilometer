from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import timedelta
from .models import Run


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
