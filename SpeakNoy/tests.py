from django.test import TestCase
from django.urls import reverse
from .models import Flashcard

class CebuanoFlashcardTest(TestCase):
    def setUp(self):
        self.card = Flashcard.objects.create(
            word="pinulongan",
            pronunciation="/pi-nu-lu-ngan/",
            definition="Language, as in the language that a person speaks.",
            purpose="Noun",
            dialect="Cebuano",
            cardtype="Custom"
        )

    def test_flashcard_str(self):
        self.assertEqual(str(self.card), "pinulongan")

    def test_flashcard_list(self):
        response = self.client.get(reverse("SpeakNoy:cardlist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Currently studying")

    def test_flashcard_detail(self):
        response = self.client.get(reverse("SpeakNoy:card", args=[self.card.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pinulongan")

class IlocanoFlashcardTest(TestCase):
    def setUp(self):
        self.card = Flashcard.objects.create(
            word="pagsasao",
            pronunciation="/pag-sa-sao/",
            definition="Language, as in the language that a person speaks.",
            purpose="Noun",
            dialect="Ilocano",
            cardtype="Custom"
        )

    def test_flashcard_str(self):
        self.assertEqual(str(self.card), "pagsasao")

    def test_flashcard_list(self):
        response = self.client.get(reverse("SpeakNoy:cardlist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Currently studying")

    def test_flashcard_detail(self):
        response = self.client.get(reverse("SpeakNoy:card", args=[self.card.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pagsasao")

class CebuanoAddCardTest(TestCase):
    def setUp(self):
        session = self.client.session
        session['selected_dialect'] = "Cebuano"
        session.save()

    def test_add_card(self):
        data = {
            "word": "tubig",
            "pronunciation": "/tu-big/",
            "definition": "Water.",
            "purpose": "Noun",
        }

        response = self.client.post(reverse("SpeakNoy:cardcreate"), data, follow=True)

        self.assertEqual(response.status_code, 200)

        card = Flashcard.objects.get(word="tubig")
        self.assertEqual(card.dialect, "Cebuano")
        self.assertEqual(card.cardtype, "Custom")
        self.assertEqual(card.purpose, "Noun")

class IlocanoAddCardTest(TestCase):
    def setUp(self):
        session = self.client.session
        session['selected_dialect'] = "Ilocano"
        session.save()

    def test_add_card(self):
        data = {
            "word": "puraw",
            "pronunciation": "/pu-raw/",
            "definition": "White.",
            "purpose": "Adjective",
        }

        response = self.client.post(reverse("SpeakNoy:cardcreate"), data, follow=True)

        self.assertEqual(response.status_code, 200)

        card = Flashcard.objects.get(word="puraw")
        self.assertEqual(card.dialect, "Ilocano")
        self.assertEqual(card.cardtype,"Custom")
        self.assertEqual(card.purpose, "Adjective")