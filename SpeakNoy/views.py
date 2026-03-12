from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Flashcard
from datetime import date, datetime

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

    flashcards = Flashcard.objects.all()
    if selected_dialect:
        flashcards = Flashcard.objects.filter(dialect=selected_dialect)
    else:
        flashcards = Flashcard.objects.none()

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

def daily_review_view(request):
    selected_dialect = request.session.get('selected_dialect')
    
    # Get all flashcards for the dialect and pick 5 random ones
    all_flashcards = Flashcard.objects.filter(dialect=selected_dialect) if selected_dialect else []
    flashcards = list(all_flashcards.order_by('?')[:5])
    
    # Mark review as completed for today
    today = str(date.today())
    request.session['review_completed_date'] = today
    
    context = {
        'selected_dialect': selected_dialect,
        'flashcard': flashcards,
    }
    return render(request, "flashcards/daily_review.html", context)