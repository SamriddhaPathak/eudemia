import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from main.models import Challenge, Subject, Class

class Command(BaseCommand):
    help = "Import challenges from a CSV file"

    def handle(self, *args, **options):
        CSV_FILE_PATH = Path("main/management/commands/challenges.csv")
        try:
            with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                if not {"subject", "grade", "name", "challenge_type"}.issubset(reader.fieldnames):
                    self.stdout.write(
                        "CSV file is missing one or more required headers: subject, grade, name, challenge_type"
                    )
                    return

                for row in reader:
                    subject_name = row.get("subject", "").strip().lower()
                    grade_name = row.get("grade", "").strip()
                    name = row.get("name", "").strip()
                    challenge_type = row.get("challenge_type", "").strip()

                    # Map to correct values
                    subject_map = {"maths": "Maths", "english": "English", "science": "Science"}
                    grade_map = {"Four": "Four", "Five": "Five", "Six": "Six", "Seven": "Seven", "Eight": "Eight"}
                    challenge_type_map = {"Weekly": "Weekly", "Daily": "Daily"}

                    try:
                        # Get or create the Subject instance
                        subject, _ = Subject.objects.get_or_create(name=subject_map.get(subject_name, None))

                        # Get or create the Class instance
                        grade, _ = Class.objects.get_or_create(name=grade_map.get(grade_name, None))

                        # Create the Challenge instance
                        challenge = Challenge(
                            subject=subject,  # Assign the Subject instance
                            grade=grade,  # Assign the Class instance
                            name=name,
                            challenge_type=challenge_type_map.get(challenge_type, None),
                        )
                        
                        # Validate the model instance
                        challenge.full_clean()
                        
                        # Save to database
                        challenge.save()
                        self.stdout.write(f"Imported: {challenge}")
                    except KeyError as e:
                        self.stdout.write(f"Invalid data for key: {e}. Row skipped: {row}")
                    except ValidationError as e:
                        self.stdout.write(f"Validation error: {e}. Row skipped: {row}")
                    except IntegrityError as e:
                        self.stdout.write(f"Database error: {e}. Row skipped: {row}")
                    except Exception as e:
                        self.stdout.write(f"Unexpected error: {e}. Row skipped: {row}")

        except FileNotFoundError:
            self.stdout.write(f"CSV file not found at path: {CSV_FILE_PATH}")
        except Exception as e:
            self.stdout.write(f"An unexpected error occurred: {e}")
