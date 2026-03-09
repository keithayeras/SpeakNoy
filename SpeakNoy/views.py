from django.shortcuts import render, get_object_or_404
from .models import Flashcard
from datetime import date

def flashcard_list_view(request):
    show_login_popup = False
    if not request.user.is_authenticated:
        show_login_popup = True

    new_dialect = request.GET.get('set_dialect')
    show_review_popup = False
    
    if new_dialect:
        request.session['selected_dialect'] = new_dialect
        
        # Only show popup once per day
        today = str(date.today())
        last_popup_date = request.session.get('review_popup_shown_date')
        
        if last_popup_date != today:
            show_review_popup = True
            request.session['review_popup_shown_date'] = today
    
    selected_dialect = request.session.get('selected_dialect')
    show_selection_prompt = False
    if request.user.is_authenticated and not selected_dialect:
        show_selection_prompt = True
    
    # Check if user can still review today
    today = str(date.today())
    review_completed_date = request.session.get('review_completed_date')
    can_review = selected_dialect and review_completed_date != today
    
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
        'dialects': ['Cebuano', 'Ilocano']
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