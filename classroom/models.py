from django.db import models
from django.utils.text import slugify


class Student(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    age = models.IntegerField()
    admission_number = models.IntegerField(unique=True)
    is_qualified = models.BooleanField(default=False)
    average_score = models.FloatField(blank=True, null=True)
    username = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.first_name

    def get_grade(self):
        if self.average_score is not None:
            if self.average_score >= 80:
                return "A"
            elif self.average_score >= 60:
                return "B"
            elif self.average_score >= 40:
                return "C"
            else:
                return "D"

    def save(self, *args, **kwargs):
        self.username = slugify(self.first_name + " " + self.last_name)
        super().save(*args, **kwargs)


class Classroom(models.Model):
    name = models.CharField(max_length=120)
    student_capacity = models.IntegerField(default=0)
    students = models.ManyToManyField(Student, blank=True, related_name="classrooms")

    def __str__(self):
        return self.name
