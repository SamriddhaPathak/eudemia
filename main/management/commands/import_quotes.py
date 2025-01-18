import csv
from django.core.management.base import BaseCommand
from main.models import Quote

class Command(BaseCommand):
    help = 'Import quotes from a predefined CSV file'

    def handle(self, *args, **kwargs):
        file_path = "main/management/commands/quotes.csv"  # Hardcoded file path
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    quote = row['quote']
                    by = row['by']
                    # Create a Quote object and save it to the database
                    Quote.objects.create(quote=quote, by=by)
                self.stdout.write(self.style.SUCCESS(f"Successfully imported quotes from {file_path}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(f"CSV error: {e}"))
