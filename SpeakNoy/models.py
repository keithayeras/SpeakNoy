from django.db import models
from django.conf import settings

class Flashcard(models.Model):
    is_public = models.BooleanField(default=False)
    PURPOSE_CHOICES = [
        ("Noun", "Noun"),
        ("Pronoun", "Pronoun"),
        ("Verb", "Verb"),
        ("Adjective", "Adjective"),
        ("Adverb", "Adverb"),
        ("Expression", "Expression"),
    ]

    DIALECT_CHOICES = [
        ("Cebuano", "Cebuano"),
        ("Ilocano", "Ilocano"),
    ]

    CARDTYPE_CHOICES = [
        ("Universal", "Universal"),
        ("Custom", "Custom")
    ]

    word = models.CharField(max_length=63)
    pronunciation = models.CharField(max_length=63)
    definition = models.TextField()
    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES,
        default="Noun"
    )
    dialect = models.CharField(
        max_length=20,
        choices=DIALECT_CHOICES,
        default="Cebuano"
    )
    cardtype = models.CharField(
        max_length=9,
        choices=CARDTYPE_CHOICES,
        default="Custom"
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.word
    

class FlashcardCollection(models.Model):
    name = models.CharField(max_length=63)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    flashcards = models.ManyToManyField(
        Flashcard,
        blank=True,
        related_name='collections'
    )

    def __str__(self):
        return self.name

class PublicSpace(models.Model):
    name = models.CharField(max_length=63)
    flashcards = models.ManyToManyField(
        Flashcard,
        blank=True,
        related_name='publicspace_flashcards'
    )

    collections = models.ManyToManyField(
        FlashcardCollection,
        blank=True,
        related_name='publicspace_collections'
    )

    def __str__(self):
        return self.name