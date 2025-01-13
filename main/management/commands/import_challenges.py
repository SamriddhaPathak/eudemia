import csv
from django.core.management.base import BaseCommand
from main.models import Challenge  # Replace 'your_app' with the name of your app

class Command(BaseCommand):
    help = "Import challenges from Challenge.csv into the Challenge model"

    def handle(self, *args, **kwargs):
        file_path = "main\management\commands\Challenge.csv"  # Path to your CSV file

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0

                for row in reader:
                    question = row.get("question")
                    answer = row.get("answer")

                    if question and answer:
                        Challenge.objects.create(question=question, answer=answer)
                        count += 1

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully imported {count} challenges.")
                )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
