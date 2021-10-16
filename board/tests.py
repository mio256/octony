import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Thread


def create_thread(thread_text, days):
    """
    Create a thread with the given `thread_text` and published the
    given number of `days` offset to now (negative for threads published
    in the past, positive for threads that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Thread.objects.create(thread_text=thread_text, pub_date=time)


class ThreadIndexViewTests(TestCase):
    def test_no_threads(self):
        """
        If no threads exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('board:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No board are available.")
        self.assertQuerysetEqual(response.context['latest_thread_list'], [])

    def test_past_thread(self):
        """
        Threads with a pub_date in the past are displayed on the
        index page.
        """
        thread = create_thread(thread_text="Past thread.", days=-30)
        response = self.client.get(reverse('board:index'))
        self.assertQuerysetEqual(
            response.context['latest_thread_list'],
            [thread],
        )

    def test_future_thread(self):
        """
        Threads with a pub_date in the future aren't displayed on
        the index page.
        """
        create_thread(thread_text="Future thread.", days=30)
        response = self.client.get(reverse('board:index'))
        self.assertContains(response, "No board are available.")
        self.assertQuerysetEqual(response.context['latest_thread_list'], [])

    def test_future_thread_and_past_thread(self):
        """
        Even if both past and future threads exist, only past threads
        are displayed.
        """
        thread = create_thread(thread_text="Past thread.", days=-30)
        create_thread(thread_text="Future thread.", days=30)
        response = self.client.get(reverse('board:index'))
        self.assertQuerysetEqual(
            response.context['latest_thread_list'],
            [thread],
        )

    def test_two_past_threads(self):
        """
        The threads index page may display multiple threads.
        """
        thread1 = create_thread(thread_text="Past thread 1.", days=-30)
        thread2 = create_thread(thread_text="Past thread 2.", days=-5)
        response = self.client.get(reverse('board:index'))
        self.assertQuerysetEqual(
            response.context['latest_thread_list'],
            [thread2, thread1],
        )


class ThreadDetailViewTests(TestCase):
    def test_future_thread(self):
        """
        The detail view of a thread with a pub_date in the future
        returns a 404 not found.
        """
        future_thread = create_thread(thread_text='Future thread.', days=5)
        url = reverse('board:detail', args=(future_thread.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_thread(self):
        """
        The detail view of a thread with a pub_date in the past
        displays the thread's text.
        """
        past_thread = create_thread(thread_text='Past Thread.', days=-5)
        url = reverse('board:detail', args=(past_thread.id,))
        response = self.client.get(url)
        self.assertContains(response, past_thread.thread_text)
