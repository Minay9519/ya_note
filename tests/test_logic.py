from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


from notes.models import Note

User = get_user_model()

class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Василий')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
    
    def test_user_can_create_comment(self):
        self.author_client.force_login(self.author)
        note = Note.objects.create(
            title='Title',
            text='Текст',
            author=self.author,
        )
        url = reverse('notes:detail',args=(note.slug,))
        url_add = reverse('notes:add')
        form_data = {'form': note}
        
        response = self.author_client.post(url_add, data=form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.author, self.author)