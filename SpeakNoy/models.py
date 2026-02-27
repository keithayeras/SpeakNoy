from django.db import models

# Create your models here.
class Flashcard(models.Model):
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
        default=None
    )
    cardtype = models.CharField(
        max_length=9,
        choices=CARDTYPE_CHOICES,
        default="Custom"
    )

    def __str__(self):
        return self.word