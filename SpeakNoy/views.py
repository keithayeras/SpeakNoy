from django.shortcuts import render, get_object_or_404, redirect
from .models import Flashcard
from .forms import FlashcardForm

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

def flashcard_create_view(request):
    selected_dialect = request.session.get('selected_dialect', "Cebuano")

    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.dialect = selected_dialect
            flashcard.cardtype = "Custom"
            flashcard.save()
            return redirect("SpeakNoy:cardlist")
    else:
        form = FlashcardForm(initial={
            'dialect': selected_dialect,
            'cardtype': "Custom"
        })
    
    return render(request, "flashcards/flashcard_create.html", {"form": form})
