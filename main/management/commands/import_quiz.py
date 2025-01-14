import csv
from django.core.management.base import BaseCommand
from main.models import Quiz  # Replace 'main' with your app name


class Command(BaseCommand):
    help = "Import Quiz data from Quiz.csv into the Quiz model"

    def handle(self, *args, **kwargs):
        # Use forward slashes or a raw string for the file path
        file_path = r"main/management/commands/Quiz.csv"  # Adjust path as needed

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0

                for row in reader:
                    grade = row.get('grade')
                    question = row.get('question')
                    option1 = row.get('option1')
                    option2 = row.get('option2')
                    option3 = row.get('option3')
                    option4 = row.get('option4')
                    correct = row.get('correct')

                    # Ensure all fields are valid and not empty
                    if all([question, option1, option2, option3, option4, correct]):
                        Quiz.objects.create(
                            grade=grade,
                            question=question,
                            option1=option1,
                            option2=option2,
                            option3=option3,
                            option4=option4,
                            correct=int(correct),  # Convert check to integer
                        )
                        count += 1

                self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} quizzes."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
