from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime, time
from unittest.mock import patch
import pytz
from .models import *
from .forms import *

User = get_user_model()

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
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_flashcard_str(self):
        self.assertEqual(str(self.card), "pinulongan")

    def test_flashcard_list(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse("SpeakNoy:cardlist"))
        self.assertEqual(response.status_code, 200)

    def test_flashcard_detail(self):
        self.client.login(username='testuser', password='testpass123')
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
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_flashcard_str(self):
        self.assertEqual(str(self.card), "pagsasao")

    def test_flashcard_list(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse("SpeakNoy:cardlist"))
        self.assertEqual(response.status_code, 200)

    def test_flashcard_detail(self):
        self.client.login(username='testuser', password='testpass123')
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
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_requires_authentication(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse("SpeakNoy:cardlist"))

    def test_detail_view_404(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse("SpeakNoy:card", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_create_view_post_invalid(self):
        self.client.login(username='testuser', password='testpass123')
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
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.customCard = Flashcard.objects.create(
            word="Goku",
            pronunciation="/Go-koo/",
            definition="Solos your verse",
            purpose="Noun",
            dialect="Cebuano",
            cardtype="Custom"
        )

    def test_custom_card_removal(self):
        self.client.login(username='testuser', password='testpass123')
        self.assertTrue(Flashcard.objects.filter(pk=self.customCard.pk).exists())
        response = self.client.post(reverse("SpeakNoy:cardremove", args=[self.customCard.pk]), follow=True)
        self.assertFalse(Flashcard.objects.filter(pk=self.customCard.pk).exists())

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
        form = FlashcardCollectionForm(data={"name": "A" * 78})
        self.assertFalse(form.is_valid())

    def test_add_to_collection_form_valid(self):
        collection = FlashcardCollection.objects.create(name="Test")
        form = AddToCollectionForm(data={"collection": collection.pk})
        self.assertTrue(form.is_valid())

    def test_add_to_collection_form_no_selection(self):
        form = AddToCollectionForm(data={"collection": ""})
        self.assertFalse(form.is_valid())

    def test_add_to_collection_form_invalid_pk(self):
        form = AddToCollectionForm(data={"collection": 9876})
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
        response = self.client.get(reverse("SpeakNoy:collection", args=[31415]))
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

# This tests the collection create view.
class CollectionCreateViewTest(TestCase):
    def test_collection_create(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse("SpeakNoy:collectioncreate"))
        self.assertEqual(response.status_code, 200)

    def test_collection_create_form_valid(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse("SpeakNoy:collectioncreate"),
            {"name": "New Collection"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(FlashcardCollection.objects.filter(name="New Collection").exists())

    def test_collection_create_form_invalid(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse("SpeakNoy:collectioncreate"), {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertEqual(FlashcardCollection.objects.count(), 0)

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
        self.collection = FlashcardCollection.objects.create(name="Collection Test")
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_add_to_collection(self):
        response = self.client.get(reverse("SpeakNoy:add_to_collection", args=[self.card.pk]))
        self.assertEqual(response.status_code, 200)

    def test_add_to_collection_missing_card_404(self):
        response = self.client.get(reverse("SpeakNoy:add_to_collection", args=[2026]))
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

# The tests below will test if the Remove from Collection form works.

class RemoveFromCollectionFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.collection = FlashcardCollection.objects.create(name="Collection Test")
 
    def test_invalid_blank_selection(self):
        self.client.login(username='testuser', password='testpass123')
        form = RemoveFromCollectionForm(data={"collection": ""})
        self.assertFalse(form.is_valid())
 
    def test_invalid_invalid_primary_key(self):
        self.client.login(username='testuser', password='testpass123')
        form = RemoveFromCollectionForm(data={"collection": 9876})
        self.assertFalse(form.is_valid())

# Public Space Tests

# The tests below will test the Public Space model.

class PublicSpaceModelTest(TestCase):
    def setUp(self):
        self.space = PublicSpace.objects.create(name="Public Space Test")
        self.card = Flashcard.objects.create(
            word="bulan",
            pronunciation="/bu-lan/",
            definition="Moon.",
            purpose="Noun",
            dialect="Cebuano"
        )
        self.collection = FlashcardCollection.objects.create(name="Collection Test")

    def test_publicspace_initialized_empty(self):
        self.assertEqual(self.space.flashcards.count(), 0)
        self.assertEqual(self.space.collections.count(), 0)

    def test_add_card_to_publicspace(self):
        self.space.flashcards.add(self.card)
        self.assertIn(self.card, self.space.flashcards.all())

    def test_add_collection_to_publicspace(self):
        self.space.collections.add(self.collection)
        self.assertIn(self.collection, self.space.collections.all())

    def test_remove_card_from_publicspace(self):
        self.space.flashcards.add(self.card)
        self.space.flashcards.remove(self.card)
        self.assertNotIn(self.card, self.space.flashcards.all())

    def test_remove_collection_from_publicspace(self):
        self.space.collections.add(self.collection)
        self.space.collections.remove(self.collection)
        self.assertNotIn(self.collection, self.space.collections.all())

# The tests below will check if the form for the Public Space works.

class PublicSpaceFormTest(TestCase):
    def test_if_form_valid(self):
        form = PublicSpaceForm(data={"name": "Public Space Test"})
        self.assertTrue(form.is_valid())
 
    def test_invalid_name_not_given(self):
        form = PublicSpaceForm(data={"name": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
 
    def test_invalid_name_too_long(self):
        form = PublicSpaceForm(data={"name": "A" * 98})
        self.assertFalse(form.is_valid())

# These test if the Public Space interface or view works

class PublicSpaceViewTest(TestCase):
    def test_publicspace_view_returns_200(self):
        response = self.client.get(reverse("SpeakNoy:publicspace"))
        self.assertEqual(response.status_code, 200)
 
    def test_publicspace_view_shows_cards(self):
        space = PublicSpace.objects.create(name="Public Space")
        card = Flashcard.objects.create(
            word="bulan",
            pronunciation="/bu-lan/",
            definition="Moon.",
            purpose="Noun",
            dialect="Cebuano"
        )
        space.flashcards.add(card)
        response = self.client.get(reverse("SpeakNoy:publicspace"))
        self.assertContains(response, "bulan")
 
    def test_publicspace_view_shows_collections(self):
        space = PublicSpace.objects.create(name="Public Space")
        collection = FlashcardCollection.objects.create(name="Collection Test")
        space.collections.add(collection)
        response = self.client.get(reverse("SpeakNoy:publicspace"))
        self.assertContains(response, "Collection Test")


class DailyReviewPopupTest(TestCase):
    """Test the daily review popup functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.url = reverse('SpeakNoy:cardlist')
    
    def test_popup_does_not_show_without_scheduled_time(self):
        """Test that popup doesn't show when no time is set"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertFalse(response.context['show_review_popup'])
    
    def test_popup_shows_when_time_passed(self):
        """Test that popup shows when current time is >= scheduled time"""
        # Set user's daily review time to a past time
        self.user.profile.daily_review_time = time(8, 0)
        self.user.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
        
        # Mock timezone to be after scheduled time
        with patch('SpeakNoy.views.timezone.localtime') as mock_now:
            mock_now.return_value = datetime(2026, 4, 22, 15, 30, tzinfo=pytz.UTC)
            response = self.client.get(self.url)
            self.assertTrue(response.context['show_review_popup'])
    
    def test_popup_not_shows_before_scheduled_time(self):
        """Test that popup doesn't show before scheduled time"""
        # Set user's daily review time to a future time
        self.user.profile.daily_review_time = time(20, 0)
        self.user.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
        
        # Mock timezone to be before scheduled time
        with patch('SpeakNoy.views.timezone.localtime') as mock_now:
            mock_now.return_value = datetime(2026, 4, 22, 10, 0, tzinfo=pytz.UTC)
            response = self.client.get(self.url)
            self.assertFalse(response.context['show_review_popup'])
    
    def test_popup_shown_only_once_per_day(self):
        """Test that popup is shown only once per day"""
        self.user.profile.daily_review_time = time(8, 0)
        self.user.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
        
        with patch('SpeakNoy.views.timezone.localtime') as mock_now:
            mock_now.return_value = datetime(2026, 4, 22, 15, 30, tzinfo=pytz.UTC)
            
            # First visit
            response1 = self.client.get(self.url)
            self.assertTrue(response1.context['show_review_popup'])
            
            # Second visit same day
            response2 = self.client.get(self.url)
            self.assertFalse(response2.context['show_review_popup'])
    
    def test_popup_resets_next_day(self):
        """Test that popup resets the next day"""
        self.user.profile.daily_review_time = time(8, 0)
        self.user.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
        
        with patch('SpeakNoy.views.timezone.localtime') as mock_now:
            # First day
            mock_now.return_value = datetime(2026, 4, 22, 15, 30, tzinfo=pytz.UTC)
            response1 = self.client.get(self.url)
            self.assertTrue(response1.context['show_review_popup'])
            
            # Second day
            mock_now.return_value = datetime(2026, 4, 23, 15, 30, tzinfo=pytz.UTC)
            response2 = self.client.get(self.url)
            self.assertTrue(response2.context['show_review_popup'])
    
    def test_popup_independent_of_dialect_selection(self):
        """Test that popup appears regardless of dialect selection"""
        self.user.profile.daily_review_time = time(8, 0)
        self.user.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
        
        # Don't select a dialect
        session = self.client.session
        # Make sure no dialect is selected
        if 'selected_dialect' in session:
            del session['selected_dialect']
        session.save()
        
        with patch('SpeakNoy.views.timezone.localtime') as mock_now:
            mock_now.return_value = datetime(2026, 4, 22, 15, 30, tzinfo=pytz.UTC)
            response = self.client.get(self.url)
            self.assertTrue(response.context['show_review_popup'])
    
    def test_popup_independent_of_review_completion(self):
        """Test that popup appears regardless of review completion"""
        self.user.profile.daily_review_time = time(8, 0)
        self.user.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
        
        # Mark review as completed for today
        session = self.client.session
        session['review_completed_date'] = str(timezone.now().date())
        session.save()
        
        with patch('SpeakNoy.views.timezone.localtime') as mock_now:
            mock_now.return_value = datetime(2026, 4, 22, 15, 30, tzinfo=pytz.UTC)
            response = self.client.get(self.url)
            self.assertTrue(response.context['show_review_popup'])
    
    def test_schedule_saved_message(self):
        """Test that schedule saved message appears after POST"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {'daily_review_time': '14:30'})
        self.assertTrue(response.context['schedule_saved'])
    
    def test_popup_time_in_context(self):
        """Test that popup time is available in context"""
        self.user.profile.daily_review_time = time(9, 30)
        self.user.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.context['review_popup_time'], '09:30')
    
    def test_multiple_time_changes(self):
        """Test that popup time can be changed multiple times"""
        self.client.login(username='testuser', password='testpass123')
        
        # Change time first time
        self.client.post(self.url, {'daily_review_time': '08:00'})
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.daily_review_time, time(8, 0))
        
        # Change time second time
        self.client.post(self.url, {'daily_review_time': '17:00'})
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.daily_review_time, time(17, 0))
