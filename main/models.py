from django.db import models
from django.contrib.auth.models import User
from math import floor
from django.utils.timezone import now
from datetime import date

quiz_choices = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
)

challenge_type_choices = [
    ("weekly", "Weekly"),
    ("daily", "Daily"),
]

item_type_choices = [
    ("avatar_border", "Avatar Border"),
    ("avatar", "Avatar"),
]

class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"

class Challenge(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey("users.Class", default=4, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    challenge_type = models.CharField(max_length=50, choices=challenge_type_choices)
    created_by = models.ForeignKey("users.Teacher", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Challenge for {self.grade}: {self.name}"

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question = models.TextField(max_length=200)
    answer = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, blank=True)
    question_type = models.CharField(max_length=50, blank=True, null=True, choices=challenge_type_choices, default="daily")
    grade = models.ForeignKey("users.Class", default=4, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Subject: {self.subject}, Grade: {self.grade}, Type: {self.question_type}"

class ChallengeTracker(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    current_question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE)
    correct_questions = models.ManyToManyField(Question, blank=True, related_name="completed_by_correct")
    incorrect_questions = models.ManyToManyField(Question, blank=True, related_name="completed_by_incorrect")
    answer = models.CharField(max_length=50, blank=True, null=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def progress_percentage(self):
        completed = self.correct_questions.count() + self.incorrect_questions.count()
        total = self.challenge.question_set.count()
        if total == 0:
            return 0
        return (completed / total) * 100
    
    def completed_questions(self):
        completed_list = self.correct_questions.all().union(self.incorrect_questions.all())
        return completed_list
    
    def is_complete(self):
        return self.completed_questions().count() == self.challenge.question_set.count()
    
    def grant_rewards(self):
        if self.is_complete() and not self.completed_at:
            points = 50 if self.challenge.challenge_type == "weekly" else 25
            xp = self.completed_questions().count() * ( 5 if self.challenge.challenge_type == "daily" else 10) # 5 XP per question
            grant_points(self.student.id, points)
            grant_xp(self.student.id, xp)
            self.completed_at = now()

    def __str__(self):
        return f"{self.student.user.username} - {self.challenge.name}"

class Quiz(models.Model):
    name = models.CharField(max_length=50)
    num_of_questions = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name

class QuizTracker(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    current_question = models.ForeignKey(Question, on_delete=models.CASCADE)

class QuizQuestion(models.Model):
    grade = models.ForeignKey("users.Class", default=4, on_delete=models.CASCADE)
    question = models.TextField(max_length=150)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct = models.PositiveIntegerField(choices=quiz_choices)
    quiz = models.ForeignKey(Quiz, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question for grade {self.grade}"
  
class Attendance(models.Model):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
    ]

    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)
    # days_attended = models.PositiveIntegerField(default=0)
    # days_passed = models.PositiveIntegerField(default=60)

    def __str__(self):
        return f"{self.student.user.username} - {self.date}"

class Quote(models.Model):
    quote = models.TextField(max_length=1000)
    by = models.TextField(max_length=50)

    def __str__(self):
        return f"Quote by {self.by}"

class ShopItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="reward_images", blank=True, null=True)
    cost = models.PositiveIntegerField()
    item_type = models.CharField(max_length=100, choices=item_type_choices)
    date_created = models.DateTimeField(auto_now_add=True)

    def purchase(self, student):
        if student.points >= self.cost:
            student.points -= self.cost
            student.save()
            self.save()
            Purchase.objects.create(student=student, shop_item=self)
            return True
        return False

    def __str__(self):
        return f"{self.name} ({self.item_type})"

class Purchase(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="purchases")
    shop_item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, related_name="purchases")
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.shop_item.name}"
    

def next_level(level):
    base_xp = 20
    exponent = 1.5
    return floor(base_xp * (level ** exponent))

def grant_xp(student_id, xp):
    from users import Student
    student = Student.objects.get(id=student_id)
    required_xp = next_level(student.level)
    student.xp += xp
    if student.xp >= required_xp:
        student.level += 1
        student.xp -= required_xp
    student.save()

def grant_points(student_id, points):
    from users import Student
    student = Student.objects.get(id=student_id)
    student.points += points
    student.save()