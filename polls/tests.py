import datetime
from django.test import TestCase

from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Question

def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionMethodTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() should return false for questions whose
		pub_date is in the future 

		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_past_question(self):
		"""
		should return false if event was earlier than one day ago
		"""
		time = timezone.now() - datetime.timedelta(days=2)
		past_question = Question(pub_date=time)
		self.assertEqual(past_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		should return true, as question is recent(<=1 day ago)
		"""
		time = timezone.now() - datetime.timedelta(days=0.5)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)

	class QuestionViewTests(TestCase):
		def test_index_view_with_no_questions(self):
			"""
			If no questions exist, an appropriate message should be displayed
			"""

			response = self.client.get(reverse('polls:index'))
			self.assertEqual(response.status_code, 200)
			self.assertContains(response, "No polls are available.")
			# Should be empty!!
			self.assertQuerysetEqual(response.context['latest_question_list'], [])

		def test_index_view_with_past_question(self):
			"""
			Questions with a pub date in the past should be displayed in index 
			"""
			create_question(question_text="Past Question", days=-40)
			response = self.client.get(reverse('polls:index'))
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.context['latest_question_list'].length > 0, True)

		def test_index_view_with_future_question(self):
			"""
			Questions with a pub_date in the future should not be displayed
			in the index
			"""
			create_question(question_text="Future Question", days=40)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.context['latest_question_list'], [])
			print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")




