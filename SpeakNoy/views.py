from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from datetime import date, datetime
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def flashcard_list_view(request):
    show_login_popup = False
    if not request.user.is_authenticated:
        show_login_popup = True

    new_dialect = request.GET.get('set_dialect')
    show_review_popup = False
    schedule_saved = False

    if request.method == 'POST' and request.POST.get('daily_review_time'):
        # Persist the time the user wants to be prompted for daily review
        daily_review_time = request.POST.get('daily_review_time')
        if request.user.is_authenticated:
            # Save schedule to user profile (persistent across browsers/devices)
            profile = getattr(request.user, 'profile', None)
            if profile:
                try:
                    profile.daily_review_time = datetime.strptime(daily_review_time, "%H:%M").time()
                except ValueError:
                    profile.daily_review_time = None
                profile.save(update_fields=['daily_review_time'])
        else:
            # Fallback for anonymous users (session-only)
            request.session['review_popup_time'] = daily_review_time

        # Reset the popup shown marker so we can show it again at the scheduled time
        request.session.pop('review_popup_shown_date', None)
        schedule_saved = True

    if new_dialect:
        request.session['selected_dialect'] = new_dialect
    
    selected_dialect = request.session.get('selected_dialect')
    show_selection_prompt = False
    if request.user.is_authenticated and not selected_dialect:
        show_selection_prompt = True
    
    # Determine whether we can still review today
    today = str(date.today())
    review_completed_date = request.session.get('review_completed_date')
    can_review = selected_dialect and review_completed_date != today

    # Determine if we should show the review reminder popup
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        review_popup_time = None
        if profile and profile.daily_review_time:
            review_popup_time = profile.daily_review_time.strftime("%H:%M")
    else:
        review_popup_time = request.session.get('review_popup_time')

    last_popup_date = request.session.get('review_popup_shown_date')
    now = timezone.localtime()
    now_time = now.time().replace(tzinfo=None)

    if can_review:
        if review_popup_time:
            try:
                scheduled_time = datetime.strptime(review_popup_time, "%H:%M").time()
            except ValueError:
                scheduled_time = None

            if scheduled_time and now_time >= scheduled_time and last_popup_date != today:
                show_review_popup = True
                request.session['review_popup_shown_date'] = today
        else:
            # Default behavior: show popup once per day on first open
            if new_dialect and last_popup_date != today:
                show_review_popup = True
                request.session['review_popup_shown_date'] = today

    flashcards = Flashcard.objects.filter(Q(creator=request.user) | Q(is_public=True))
    if selected_dialect:
        flashcards = flashcards.filter(dialect=selected_dialect)

    context = {
        'show_login_popup': show_login_popup,
        'flashcard': flashcards if request.user.is_authenticated else [],
        'show_selection_prompt': show_selection_prompt,
        'show_review_popup': show_review_popup,
        'selected_dialect': selected_dialect,
        'can_review': can_review,
        'dialects': ['Cebuano', 'Ilocano'],
        'review_popup_time': review_popup_time,
        'schedule_saved': schedule_saved,
    }

    return render(request, "flashcards/flashcard_list.html", context)

def flashcard_detail_view(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    context = {'flashcard': flashcard}
    return render(request, "flashcards/flashcard_detail.html", context)

@login_required
def daily_review_view(request):
    selected_dialect = request.session.get('selected_dialect')
    # Get all flashcards for the dialect and pick 5 random ones
    all_flashcards = Flashcard.objects.filter(Q(creator=request.user) | Q(is_public=True))
    if selected_dialect:
        select_flashcards = all_flashcards.filter(dialect=selected_dialect) if selected_dialect else []
        flashcards = list(select_flashcards.order_by('?')[:5])
    else:
        flashcards = []
    
    # Mark review as completed for today
    today = str(date.today())
    request.session['review_completed_date'] = today
    
    context = {
        'selected_dialect': selected_dialect,
        'flashcard': flashcards,
    }
    return render(request, "flashcards/daily_review.html", context)

@login_required
def dialect_review_view(request):
    """Review page that shows all cards for the selected dialect.

    Includes an option to draw a random card via ?random=1.
    """
    selected_dialect = request.session.get('selected_dialect')
    all_flashcards = Flashcard.objects.filter(Q(creator=request.user) | Q(is_public=True))
    if selected_dialect:
        select_flashcards = all_flashcards.filter(dialect=selected_dialect) if selected_dialect else []
    else:
        flashcards = []

    # Determine whether the user can still do their daily review today
    today = str(date.today())
    review_completed_date = request.session.get('review_completed_date')
    can_review = selected_dialect and review_completed_date != today

    random_card = None
    if request.GET.get('random') and all_flashcards:
        random_card = all_flashcards.order_by('?').first()

    context = {
        'selected_dialect': selected_dialect,
        'flashcard': select_flashcards,
        'random_card': random_card,
        'can_review': can_review,
    }
    return render(request, "flashcards/dialect_review.html", context)

@login_required
def flashcard_create_view(request):
    selected_dialect = request.session.get('selected_dialect', "Cebuano")

    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.dialect = selected_dialect
            flashcard.cardtype = "Custom"
            flashcard.creator = request.user
            flashcard.save()
            return redirect("SpeakNoy:cardlist")
    else:
        form = FlashcardForm(initial={
            'dialect': selected_dialect,
            'cardtype': "Custom"
        })

    return render(request, "flashcards/flashcard_create.html", {"form": form})

def flashcard_remove(request, pk):
    if request.method == 'POST':
        flashcard = get_object_or_404(Flashcard, pk=pk)
        flashcard.delete()

    return redirect('SpeakNoy:cardlist')

def collection_list_view(request):
    collections = FlashcardCollection.objects.filter(creator=request.user)
    return render(request, "flashcards/collection_list.html", {"collections": collections})

def collection_detail_view(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    return render(request, "flashcards/collection_detail.html", {"collection": collection})

@login_required
def collection_create_view(request):
    if request.method == 'POST':
        form = FlashcardCollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.creator = request.user
            collection.save()
            return redirect("SpeakNoy:collection", pk=collection.pk)
    else:
        form = FlashcardCollectionForm()
    return render(request, "flashcards/collection_create.html", {"form": form})

def collection_add_card(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    if request.method == 'POST':
        form = AddToCollectionForm(request.POST, user=request.user)
        if form.is_valid():
            collection = form.cleaned_data['collection']
            collection.flashcards.add(flashcard)
            return redirect("SpeakNoy:collection", pk=collection.pk)
    else:
        form = AddToCollectionForm(user=request.user)
    return render(request, "flashcards/add_to_collection.html", {
        "form": form,
        "flashcard": flashcard
    })

def collection_remove_view(request, pk):
    if request.method == 'POST':
        collection = get_object_or_404(FlashcardCollection, pk=pk)
        collection.delete()
    return redirect('SpeakNoy:collectionlist')

def collection_remove_card(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    if request.method == 'POST':
        form = RemoveFromCollectionForm(request.POST, collection_id=pk)
        if form.is_valid():
            flashcard = form.cleaned_data['collection']
            collection.flashcards.remove(flashcard)
            return redirect("SpeakNoy:collection", pk=collection.pk)
    else:
        form = RemoveFromCollectionForm(collection_id=pk)
    return render(request, "flashcards/remove_from_collection.html", {
        "form": form,
        "collection": collection
    })
    
def publicspace_view(request):
    publicspace, _ = PublicSpace.objects.get_or_create(name="Public Space")

    if publicspace:
        collections = publicspace.collections.all()
        flashcards = publicspace.flashcards.all()
    else:
        collections = []
        flashcards = []

    context = {
        "publicspace_collections": collections,
        "publicspace_cards": flashcards,
    }

    return render(request, "flashcards/publicspace.html", context)

def publicspace_upload_card(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    publicspace_cards, created = PublicSpace.objects.get_or_create(name="Public Space")
    if publicspace_cards:
        publicspace_cards.flashcards.add(flashcard)
        return redirect("SpeakNoy:publicspace")
    else:
        return redirect("SpeakNoy:cardlist")

def publicspace_upload_collection(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    publicspace_collections, created = PublicSpace.objects.get_or_create(name="Public Space")
    if publicspace_collections:
        publicspace_collections.collections.add(collection)
        return redirect("SpeakNoy:publicspace")
    else:
        return redirect("SpeakNoy:collectionlist")

def publicspace_save_card(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    saved_card = Flashcard.objects.create(
        word = flashcard.word,
        pronunciation = flashcard.pronunciation,
        definition = flashcard.definition,
        purpose = flashcard.purpose,
        dialect = flashcard.dialect,
        cardtype = "Custom",
        creator = request.user,
    )
    return redirect("SpeakNoy:cardlist")

def publicspace_save_collection(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    saved_collection = FlashcardCollection.objects.create(
        name = collection.name,
        creator = request.user,
    )
    for flashcard in collection.flashcards.all():
        saved_card = Flashcard.objects.create(
            word = flashcard.word,
            pronunciation = flashcard.pronunciation,
            definition = flashcard.definition,
            purpose = flashcard.purpose,
            dialect = flashcard.dialect,
            cardtype = "Custom",
            creator = request.user,
        )
        saved_collection.flashcards.add(saved_card)
    return redirect("SpeakNoy:collectionlist")

def publicspace_remove_card(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    publicspace_cards, created = PublicSpace.objects.get_or_create(name="Public Space")
    if publicspace_cards:
        publicspace_cards.flashcards.remove(flashcard)
        return redirect("SpeakNoy:publicspace")
    else:
        return redirect("SpeakNoy:cardlist")

def publicspace_remove_collection(request, pk):
    collection = get_object_or_404(FlashcardCollection, pk=pk)
    publicspace_collections, created = PublicSpace.objects.get_or_create(name="Public Space")
    if publicspace_collections:
        publicspace_collections.collections.remove(collection)
        return redirect("SpeakNoy:publicspace")
    else:
        return redirect("SpeakNoy:collectionlist")