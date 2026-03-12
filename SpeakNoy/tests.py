from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Flashcard
from .forms import FlashcardForm

class DefaultCardTest(TestCase):
    def test_default_values(self):
        card = Flashcard.objects.create(
            word="default",
            pronunciation="/de-fault/",
            definition="Ginagamit upang malaman kung gumagana.",
        )

        self.assertEqual(card.purpose, "Noun")
        self.assertEqual(card.dialect, "Cebuano")
        self.assertEqual(card.cardtype, "Custom")

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

class InvalidCardTest(TestCase):
    def test_invalid_purpose(self):
        card = Flashcard(
            word="test",
            pronunciation="/test/",
            definition="Basta-bastang salita.",
            purpose="InvalidChoice",
        )

        with self.assertRaises(ValidationError):
            card.full_clean()

class FlashcardFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "word": "dagat",
            "pronunciation": "/da-gat/",
            "definition": "Sea.",
            "purpose": "Noun",
        }

        form = FlashcardForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_word_out(self):
        form_data = {
            "pronunciation": "/da-gat/",
            "definition": "Sea.",
            "purpose": "Noun",
        }

        form = FlashcardForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_pronunciation_out(self):
        form_data = {
            "word": "dagat",
            "definition": "Sea.",
            "purpose": "Noun",
        }

        form = FlashcardForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_definition_out(self):
        form_data = {
            "word": "dagat",
            "pronunciation": "/da-gat/",
            "purpose": "Noun",
        }

        form = FlashcardForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_purpose_out(self):
        form_data = {
            "word": "dagat",
            "pronunciation": "/da-gat/",
            "definition": "Sea.",
        }

        form = FlashcardForm(data=form_data)
        self.assertFalse(form.is_valid())


class TableDropTest(TestCase):
    def setUp(self):
        self.card = Flashcard.objects.create(
            word="pagsasao",
            pronunciation="/pag-sa-sao/",
            definition="Language, as in the language that a person speaks.",
            purpose="Noun",
            dialect="Ilocano",
            cardtype="Custom"
        )

    def test_initial(self):
        response = self.client.get(reverse("SpeakNoy:card", args=[self.card.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pagsasao")

    def test_table_dropped_when_card_flawed(self):
        self.flawed_card = Flashcard.objects.create(
            word="DROP TABLE IF EXISTS SpeakNoy_flashcard;",
            pronunciation="DROP TABLE IF EXISTS SpeakNoy_flashcard;",
            definition="Language, as in the language that a person speaks.",
            purpose="Noun",
            dialect="Ilocano",
            cardtype="Custom"
        )

        response = self.client.get(reverse("SpeakNoy:card", args=[self.card.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pagsasao")

        response = self.client.get(reverse("SpeakNoy:card", args=[self.flawed_card.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DROP TABLE IF EXISTS SpeakNoy_flashcard;")
    
    def test_table_dropped_when_form_flawed(self):
        form_data = {
            "word": "DROP TABLE IF EXISTS SpeakNoy_flashcard;",
            "definition": "DROP TABLE IF EXISTS SpeakNoy_flashcard;",
            "pronunciation": "/da-gat/",
            "purpose": "Noun",
        }
        form = FlashcardForm(data=form_data)
        self.assertTrue(form.is_valid())

        response = self.client.get(reverse("SpeakNoy:card", args=[self.card.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pagsasao")

class ListViewTest(TestCase):
    def setUp(self):
        self.card = Flashcard.objects.create(
            word="init",
            pronunciation="/i-nit/",
            definition="Heat",
            purpose="Noun",
            dialect="Cebuano"
        )

    def test_requires_authentication(self):
        response = self.client.get(reverse("SpeakNoy:cardlist"))
        self.assertContains(response, "Please Login to Continue")

    def test_detail_view_404(self):
        response = self.client.get(reverse("SpeakNoy:card", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_create_view_post_invalid(self):
        response = self.client.post(reverse("SpeakNoy:cardcreate"), {
            "word": "",
            "pronunciation": "/no-word/",
            "definition": "Invalid",
            "purpose": "Noun"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
