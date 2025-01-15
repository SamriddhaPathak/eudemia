import csv
from django.core.management.base import BaseCommand
from main.models import Quiz, Class  # Replace 'main' with your app name


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
                    grade = row.get('grade')  # Grade should match an existing Class instance
                    question = row.get('question')
                    option1 = row.get('option1')
                    option2 = row.get('option2')
                    option3 = row.get('option3')
                    option4 = row.get('option4')
                    correct = row.get('correct')

                    # Fetch the Class instance
                    try:
                        grade_instance = Class.objects.get(name=grade)  # Adjust field if necessary
                    except Class.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Grade '{grade}' does not exist. Row skipped."))
                        continue

                    # Ensure all fields are valid and not empty
                    if all([question, option1, option2, option3, option4, correct]):
                        Quiz.objects.create(
                            grade=grade_instance,  # Use the Class instance
                            question=question,
                            option1=option1,
                            option2=option2,
                            option3=option3,
                            option4=option4,
                            correct=int(correct),  # Convert to integer
                        )
                        count += 1

                self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} quizzes."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
