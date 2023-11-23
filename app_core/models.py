from django.db import models

class Question(models.Model):
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['order']

class Option(models.Model):
    OPTION_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('CUSTOM', 'Custom'),  # Indicates a custom option
    ]

    STATUS_CHOICES = [
        ('GREEN', 'Green'),
        ('AMBER', 'Amber'),
        ('RED', 'Red'),
    ]

    # question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    # text = models.CharField(max_length=200)  # "Yes" or "No"

    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_type = models.CharField(max_length=6, choices=OPTION_CHOICES)
    custom_text = models.CharField(max_length=200, blank=True, null=True)
   
    triggers_text_input = models.BooleanField(default=False)
    triggers_file_upload = models.BooleanField(default=False)
    triggers_date_picker = models.BooleanField(default=False)
    triggers_yes_dropdown = models.BooleanField(default=False)  # Triggers dropdown for "Yes"
    triggers_no_dropdown = models.BooleanField(default=False)  # Triggers dropdown for "No"
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='GREEN')

    mandatory = models.BooleanField(default=False, help_text='Mark this option as mandatory')


    def __str__(self):
        if self.option_type == 'CUSTOM':
            return self.custom_text
        return self.get_option_type_display()

class YesDropdownOption(models.Model):
    question = models.ForeignKey(Question, related_name='yes_dropdown_options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)

    def __str__(self):
        return self.option_text

class NoDropdownOption(models.Model):
    question = models.ForeignKey(Question, related_name='no_dropdown_options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)

    def __str__(self):
        return self.option_text




from django.db import models
from django.contrib.auth.models import User  # For future user linking

class Response(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # For future user linking
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.selected_option:
            return f"{self.question.text} - {self.selected_option.custom_text}"
        return f"{self.question.text} - File Uploaded"
