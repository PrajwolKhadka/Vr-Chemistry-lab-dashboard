# # import uuid
# # from django.db import models
# # from datetime import datetime

# # def unique_image_filename(instance, filename):
# #     # You can use a combination of instance-specific data (e.g., name, key) and UUID to ensure uniqueness
# #     extension = filename.split('.')[-1]
# #     # Generate a unique identifier for the file and append the original extension
# #     unique_filename = f"{instance.key}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{extension}"
# #     return f"images/{unique_filename}"

# # class KeyValueData(models.Model):
# #     key = models.CharField(max_length=255, unique=True)  # Store key as a unique string
# #     value = models.TextField()  # Store the value as text
    
# #     # Add a name field
# #     name = models.CharField(max_length=255)
    
# #     # Add gender field with choices
# #     GENDER_CHOICES = [
# #         ('M', 'Male'),
# #         ('F', 'Female'),
# #         ('O', 'Other'),
# #     ]
# #     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
# #     # Store multiple integers (as a comma-separated string)
# #     multiple_int_values = models.TextField(blank=True, null=True)  # Example: store as comma-separated string
    
# #     # Add an image field with unique filename logic
# #     image = models.ImageField(upload_to=unique_image_filename, blank=True, null=True)  # Store images in the 'images/' folder inside MEDIA_ROOT

# #     def __str__(self):
# #         return self.key

# # # Model to store the API response data
# # class SurveyResponse(models.Model):
# #     id = models.CharField(max_length=50, primary_key=True)
# #     name = models.CharField(max_length=100, blank=True, null=True)
# #  # Add gender field with choices
# #     GENDER_CHOICES = [
# #         ('M', 'Male'),
# #         ('F', 'Female'),
# #         ('O', 'Other'),
# #     ]
# #     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
# #     selected_options_from_one_to_five = models.TextField(blank=True, null=True)
# #     selected_options_rest_questions = models.TextField(blank=True, null=True)
# #     score = models.IntegerField()
# #     correctly_answered = models.TextField(blank=True, null=True)  # New field for correctness
# #     skipped = models.BooleanField(default=False)  # New field for skipped status

# #     def __str__(self):
# #         return f"SurveyResponse {self.id}"

# #     class Meta:
# #         verbose_name = "Survey Response"
# #         verbose_name_plural = "Survey Responses"


# from django.db import models
# import json

# class SurveyResponse(models.Model):
#     id = models.CharField(max_length=50, primary_key=True)
#     answers = models.TextField(blank=True, null=True)  # Stores user's answers [1,0,0,1,1,0,0,0]
#     player_answers = models.TextField(blank=True, null=True)  # Stores correct answers [3,3,3,3,2,3,3,3]
#     score = models.IntegerField()
#     correctly_answered = models.TextField(blank=True, null=True)  # Stores correctness as "1,0,0,1,1,0,0,0"
#     passed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def get_answers(self):
#         return json.loads(self.answers) if self.answers else []
    
#     def get_player_answers(self):
#         return json.loads(self.player_answers) if self.player_answers else []
    
#     def get_correctness(self):
#         if self.correctly_answered:
#             return [int(x) for x in self.correctly_answered.split(',')]
#         return []
    
#     def __str__(self):
#         return f"Response {self.id} - Score: {self.score}"

#     class Meta:
#         ordering = ['-created_at']


from django.db import models
from django.core.exceptions import ValidationError
import json
from django.contrib.auth.models import User

def validate_comma_separated_ints(value):
    if value and not all(x.strip() in ('0', '1') for x in value.split(',')):
        raise ValidationError('Must be comma-separated 0s and 1s')

class SurveyResponse(models.Model):
    """
    Stores survey response data including:
    - User's answers (answers)
    - Correct answers (player_answers)
    - Score (0-8)
    - Correctness flags (1=correct, 0=incorrect)
    - Whether they passed (score ≥ 5)
    """
    id = models.CharField(max_length=50, primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    player_name = models.CharField(max_length=100, blank=True, null=True)  # Add this line
    answers = models.TextField(blank=True, null=True)
    player_answers = models.TextField(blank=True, null=True)
    score = models.IntegerField()
    correctly_answered = models.TextField(
        blank=True, 
        null=True,
        validators=[validate_comma_separated_ints]
    )
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    def get_answers(self):
        """Return user's answers as list"""
        return json.loads(self.answers) if self.answers else []
    
    def get_player_answers(self):
        """Return correct answers as list"""
        return json.loads(self.player_answers) if self.player_answers else []
    
    def get_correctness(self):
        """Return correctness flags as list of ints (1=correct, 0=incorrect)"""
        if self.correctly_answered:
            return [int(x) for x in self.correctly_answered.split(',')]
        return []

    @property
    def total_questions(self):
        return len(self.get_answers())
    
    @property
    def correct_count(self):
        return sum(self.get_correctness())
    
    @property
    def percentage_correct(self):
        if self.total_questions == 0:
            return 0
        return (self.correct_count / self.total_questions) * 100

    def clean(self):
        """Validate data consistency"""
        if self.answers and self.player_answers:
            answers = self.get_answers()
            player_answers = self.get_player_answers()
            if len(answers) != len(player_answers):
                raise ValidationError("Answers and player answers must be of equal length")

    def __str__(self):
        return f"Response {self.id} - Score: {self.score}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['score']),
            models.Index(fields=['passed']),
            models.Index(fields=['created_at']),
            models.Index(fields=['gender']),
        ]
        verbose_name = "Survey Response"
        verbose_name_plural = "Survey Responses"