from django.shortcuts import render, get_object_or_404
from .models import Flashcard

def flashcard_list_view(request):
    show_login_popup = False
    if not request.user.is_authenticated:
        show_login_popup = True

    new_dialect = request.GET.get('set_dialect')
    if new_dialect:
        request.session['selected_dialect'] = new_dialect
    selected_dialect = request.session.get('selected_dialect')
    show_selection_prompt = False
    if request.user.is_authenticated and not selected_dialect:
        show_selection_prompt = True
    
    flashcards = Flashcard.objects.all()
    if selected_dialect:
        flashcards = Flashcard.objects.filter(dialect=selected_dialect)
    else:
        flashcards = Flashcard.objects.none()

    context = {
        'show_login_popup': show_login_popup,
        'flashcard': flashcards if request.user.is_authenticated else [],
        'show_selection_prompt': show_selection_prompt,
        'selected_dialect': selected_dialect,
        'dialects': ['Cebuano', 'Ilocano']
    }

    return render(request, "flashcards/flashcard_list.html", context)

def flashcard_detail_view(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    context = {'flashcard': flashcard}
    return render(request, "flashcards/flashcard_detail.html", context)