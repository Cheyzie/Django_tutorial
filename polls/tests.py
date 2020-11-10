from django.test import TestCase
import datetime
from django.urls import reverse
from django.utils import timezone
from .models import Question

# Create your tests here.
def create_question(question_text, days):
    """
    Создает вопрос с указаным текстом и опубликован через определенное количество дней(отрицательное 
    для опубликованых в прошлом, положительные – в будущем).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
    
class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """
        Если нету вопросов, выводится сообщение.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "Вопросоу нету?")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Опросы опубликованые в прошлом отображаются на index
        """
        create_question("Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Опросы с датой публикации в будующем не отображаються.
        """
        create_question("Future question", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Вопросоу нету?")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_future_question_and_past_question(self):
        """
        Если есть опросы с датой публикации в прошлом и в будующем,
        отображаются только опросы с датой публикации в будующем не отображаються.
        """
        create_question("Past question.", -10)
        create_question("Future question.", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        Страница результатов для опроса с датой пудликации в будующем возваращает 404 
        """
        future_question = create_question("Future question.", days=5)
        url= reverse('polls:detail', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question("Past question.", days=-5)
        url = reverse('polls:results', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() возвращает False если дата публикации в будущем.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() возвращает False если публикация устарела.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() возвращает True если публикация написана меньше 1 дня назад.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)