import csv
import os
from django.core.management.base import BaseCommand
from main.models import Question, Subject  # Replace 'app_name' with your app's name
from users.models import Class


class Command(BaseCommand):
    help = 'Import questions from a default CSV file into the Question model.'

    def handle(self, *args, **kwargs):
        # Default CSV file path
        csv_file = "main/management/commands/questions.csv"  # Replace with your actual file path

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f"The file '{csv_file}' does not exist."))
            return

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            if set(reader.fieldnames) != {'subject', 'question', 'answer', 'unit', 'question_type', 'grade'}:
                self.stdout.write(self.style.ERROR("CSV file headers must be: subject, question, answer, unit, question_type, grade"))
                return

            count = 0
            errors = 0

            for row in reader:
                try:
                    # Map the subject name to a Subject object
                    subject = Subject.objects.get(name=row['subject'].strip())
                    grade_instance = Class.objects.get(name=row['grade'].strip())  # Adjust field if necessary
                    Question.objects.create(
                        subject=subject,
                        question=row['question'].strip(),
                        answer=row['answer'].strip(),
                        unit=row['unit'].strip(),  # Call strip() as a method
                        question_type=row['question_type'].strip(),  # Call strip() as a method
                        grade = grade_instance # Call strip() as a method
                    )
                    count += 1
                except Subject.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Subject '{row['subject']}' does not exist."))
                    errors += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error adding question: {e}"))
                    errors += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} questions."))
            if errors > 0:
                self.stdout.write(self.style.WARNING(f"{errors} errors occurred."))
