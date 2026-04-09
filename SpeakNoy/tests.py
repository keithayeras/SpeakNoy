from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import *
from .forms import *

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

# These test if the database for the cards can hold a card.
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

# These tests the Add Card form.
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

# This test if the invalid card won't get added to the database.
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

# This test if the Add Card form can handle invalid inputs.
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

# This tests if the List View will work as expected.
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

# This will test if a flashcard can be removed.
class FlashcardRemoveTest(TestCase):
    def setUp(self):
        self.customCard = Flashcard.objects.create(
            word="Goku",
            pronunciation="/Go-koo/",
            definition="Solos your verse",
            purpose="Noun",
            dialect="Cebuano",
            cardtype="Custom"
        )

    def test_custom_card_removal(self):
        self.assertTrue(Flashcard.objects.filter(pk=self.customCard.pk).exists())
        response = self.client.post(reverse("SpeakNoy:cardremove", args=[self.customCard.pk]), follow=True)
        self.assertFalse(Flashcard.objects.filter(pk=self.customCard.pk).exists())
        self.assertRedirects(response, reverse("SpeakNoy:cardlist"))

# Card Collection Tests

# This tests if the card collection feature works.

class CollectionModelTest(TestCase):
    def setUp(self):
        self.card = Flashcard.objects.create(
            word="tubig",
            pronunciation="/tu-big/",
            definition="Water.",
            purpose="Noun",
            dialect="Cebuano",
            cardtype="Custom"
        )
        self.collection = FlashcardCollection.objects.create(name="My Collection")

    def test_collection_correct_name(self):
        self.assertEqual(str(self.collection), "My Collection")

    def test_collection_starts_with_nothing(self):
        self.assertEqual(self.collection.flashcards.count(), 0)

    def test_add_card_to_collection(self):
        self.collection.flashcards.add(self.card)
        self.assertEqual(self.collection.flashcards.count(), 1)
        self.assertIn(self.card, self.collection.flashcards.all())

    def test_collection_unli_cards(self):
        cards = [
            Flashcard.objects.create(
                word=f"word{i}",
                pronunciation=f"/word{i}/",
                definition="Test",
                purpose="Noun",
                dialect="Cebuano"
            )
            for i in range(50)
        ]
        self.collection.flashcards.add(*cards)
        self.assertEqual(self.collection.flashcards.count(), 50)

    def test_card_in_multi_collection(self):
        col2 = FlashcardCollection.objects.create(name="Second Collection")
        self.collection.flashcards.add(self.card)
        col2.flashcards.add(self.card)
        self.assertIn(self.card, self.collection.flashcards.all())
        self.assertIn(self.card, col2.flashcards.all())

# This tests if the Collection form works.

class CollectionFormTest(TestCase):
    def test_collection_form_validity(self):
        form = FlashcardCollectionForm(data={"name": "My Collection"})
        self.assertTrue(form.is_valid())

    def test_collection_form_no_name(self):
        form = FlashcardCollectionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_collection_form_name_too_long(self):
        form = FlashcardCollectionForm(data={"name": "A" * 64})
        self.assertFalse(form.is_valid())

    def test_add_to_collection_form_valid(self):
        collection = FlashcardCollection.objects.create(name="Test")
        form = AddToCollectionForm(data={"collection": collection.pk})
        self.assertTrue(form.is_valid())

    def test_add_to_collection_form_no_selection(self):
        form = AddToCollectionForm(data={"collection": ""})
        self.assertFalse(form.is_valid())

    def test_add_to_collection_form_invalid_pk(self):
        form = AddToCollectionForm(data={"collection": 9999})
        self.assertFalse(form.is_valid())

# This tests if the collection feature views work.

# This will test if the collection list works.
class CollectionListViewTest(TestCase):
    def test_collection_list(self):
        response = self.client.get(reverse("SpeakNoy:collectionlist"))
        self.assertEqual(response.status_code, 200)

    def test_collection_list_empty_msg(self):
        response = self.client.get(reverse("SpeakNoy:collectionlist"))
        self.assertContains(response, "no collections")

    def test_collection_list_contains_collection(self):
        FlashcardCollection.objects.create(name="Vocab Set")
        response = self.client.get(reverse("SpeakNoy:collectionlist"))
        self.assertContains(response, "Vocab Set")

    def test_collection_list_shows_card_count(self):
        col = FlashcardCollection.objects.create(name="Counted Set")
        Flashcard.objects.create(
            word="init", pronunciation="/i-nit/", definition="Heat",
            purpose="Noun", dialect="Cebuano"
        )
        response = self.client.get(reverse("SpeakNoy:collectionlist"))
        self.assertContains(response, "0 card")

# This will test if the collection detail works.
class CollectionDetailViewTest(TestCase):
    def setUp(self):
        self.collection = FlashcardCollection.objects.create(name="Detail Test")
        self.card = Flashcard.objects.create(
            word="adlaw",
            pronunciation="/ad-law/",
            definition="Sun or day.",
            purpose="Noun",
            dialect="Cebuano"
        )

    def test_collection_detail(self):
        response = self.client.get(reverse("SpeakNoy:collection", args=[self.collection.pk]))
        self.assertEqual(response.status_code, 200)

    def test_collection_detail_missing_gives_404(self):
        response = self.client.get(reverse("SpeakNoy:collection", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_collection_detail_shows_collection_name(self):
        response = self.client.get(reverse("SpeakNoy:collection", args=[self.collection.pk]))
        self.assertContains(response, "Detail Test")

    def test_collection_detail_shows_cards(self):
        self.collection.flashcards.add(self.card)
        response = self.client.get(reverse("SpeakNoy:collection", args=[self.collection.pk]))
        self.assertContains(response, "adlaw")

    def test_collection_detail_empty_msg(self):
        response = self.client.get(reverse("SpeakNoy:collection", args=[self.collection.pk]))
        self.assertContains(response, "no flashcards")

# This tests the collection create view.
class CollectionCreateViewTest(TestCase):
    def test_collection_create(self):
        response = self.client.get(reverse("SpeakNoy:collectioncreate"))
        self.assertEqual(response.status_code, 200)

    def test_collection_create_form_valid(self):
        response = self.client.post(
            reverse("SpeakNoy:collectioncreate"),
            {"name": "New Collection"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(FlashcardCollection.objects.filter(name="New Collection").exists())

    def test_collection_create_form_invalid(self):
        response = self.client.post(reverse("SpeakNoy:collectioncreate"), {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertEqual(FlashcardCollection.objects.count(), 0)

    def test_collection_create_redirects_to_collection_list(self):
        response = self.client.post(
            reverse("SpeakNoy:collectioncreate"),
            {"name": "Redirect Test"}
        )
        self.assertRedirects(response, reverse("SpeakNoy:collectionlist"))

# This tests if the card's "Add to Collection" button and view works.
class AddCardToCollectionViewTest(TestCase):
    def setUp(self):
        self.card = Flashcard.objects.create(
            word="bulan",
            pronunciation="/bu-lan/",
            definition="Moon.",
            purpose="Noun",
            dialect="Cebuano"
        )
        self.collection = FlashcardCollection.objects.create(name="Space Words")

    def test_add_to_collection(self):
        response = self.client.get(reverse("SpeakNoy:add_to_collection", args=[self.card.pk]))
        self.assertEqual(response.status_code, 200)

    def test_add_to_collection_missing_card_404(self):
        response = self.client.get(reverse("SpeakNoy:add_to_collection", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_add_card_to_collection(self):
        response = self.client.post(
            reverse("SpeakNoy:add_to_collection", args=[self.card.pk]),
            {"collection": self.collection.pk},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.card, self.collection.flashcards.all())

    def test_add_to_collection_redirects_to_card_detail(self):
        response = self.client.post(
            reverse("SpeakNoy:add_to_collection", args=[self.card.pk]),
            {"collection": self.collection.pk}
        )
        self.assertRedirects(response, reverse("SpeakNoy:card", args=[self.card.pk]))

    def test_add_to_collection_no_add_if_invalid(self):
        self.client.post(
            reverse("SpeakNoy:add_to_collection", args=[self.card.pk]),
            {"collection": ""}
        )
        self.assertEqual(self.collection.flashcards.count(), 0)

    def test_add_to_collection_no_duplicate_in_collection(self):
        self.collection.flashcards.add(self.card)
        self.collection.flashcards.add(self.card)
        self.assertEqual(self.collection.flashcards.count(), 1)