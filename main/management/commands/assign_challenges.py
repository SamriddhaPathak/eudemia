from django.core.management.base import BaseCommand
from main.models import Challenge, Question, Class

class Command(BaseCommand):
    help = 'Assign questions to existing challenges (daily and weekly) for grades 4 to 8'

    def handle(self, *args, **kwargs):
        grades = Class.objects.filter(grade__in=[4, 5, 6, 7, 8])

        for grade in grades:
            # Process daily challenges for this grade
            daily_challenges = Challenge.objects.filter(grade=grade, challenge_type="daily")
            for challenge in daily_challenges:
                # Get 10 random unassigned questions for this grade
                questions = Question.objects.filter(
                    grade=grade, 
                    challenge__isnull=True
                ).order_by('?')[:10]

                # Assign the questions to the challenge
                for question in questions:
                    question.challenge = challenge
                    question.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Assigned {questions.count()} questions to daily challenge: {challenge.name} (Grade {grade.grade})."
                    )
                )

            # Process weekly challenges for this grade
            weekly_challenges = Challenge.objects.filter(grade=grade, challenge_type="weekly")
            for challenge in weekly_challenges:
                # Get 2 random unassigned questions for this grade
                questions = Question.objects.filter(
                    grade=grade, 
                    challenge__isnull=True
                ).order_by('?')[:2]

                # Assign the questions to the challenge
                for question in questions:
                    question.challenge = challenge
                    question.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Assigned {questions.count()} questions to weekly challenge: {challenge.name} (Grade {grade.grade})."
                    )
                )

        self.stdout.write(self.style.SUCCESS("Challenges updated successfully!"))
