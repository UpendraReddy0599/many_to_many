import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'many_to_many.settings')

import django
django.setup()

from django.db import transaction
from faker import Faker
from info.models import Teacher, Student

faker = Faker()

with transaction.atomic():
    for i in range(20):
        teacher_name = faker.name()
        teacher = Teacher.objects.create(name=teacher_name)
        
    for i in range(50): 
        student_name = faker.name()
        student = Student.objects.create(name=student_name)
        
    for teacher in Teacher.objects.all():
        students = Student.objects.order_by('?')[:10]
        teacher.students.add(*students) 
