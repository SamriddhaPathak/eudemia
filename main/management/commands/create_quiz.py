import random
from django.core.management.base import BaseCommand
from main.models import Quiz, QuizQuestion, Class

class Command(BaseCommand):
    help = 'Create quizzes for grades 4 to 8 with 10 random questions each'

    def handle(self, *args, **kwargs):
        # Grades for which quizzes will be created
        grades = Class.objects.filter(grade__in=[4, 5, 6, 7, 8])

        for grade in grades:
            # Count existing quizzes to determine the starting number
            quiz_count = Quiz.objects.filter(name__startswith=f"Grade {grade.grade}").count()

            for i in range(1, 4):  # Create 3 quizzes
                # Generate a readable quiz name
                quiz_name = f"Grade {grade.grade} Quiz {quiz_count + i}"

                # Create the quiz
                quiz = Quiz.objects.create(name=quiz_name, num_of_questions=10)

                # Fetch 10 random questions for this grade
                questions = QuizQuestion.objects.filter(grade=grade).order_by('?')[:10]

                # Assign the questions to the quiz
                for question in questions:
                    question.quiz = quiz
                    question.save()

                self.stdout.write(
                    self.style.SUCCESS(f"Created {quiz_name} with {questions.count()} questions.")
                )

        self.stdout.write(self.style.SUCCESS("Quizzes created successfully!"))
