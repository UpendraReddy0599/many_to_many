import jwt
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Teacher, Student

SECRET_KEY = 'key123'

def generate_jwt_token(data):
    expiration = datetime.utcnow() + timedelta(hours=1)
    data['exp'] = expiration
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')

def home(request):
    teachers = Teacher.objects.all()
    students = Student.objects.all()
    return render(request, 'home.html', {'teachers': teachers, 'students': students})

def get_students_or_teachers(request):
    selected_id = request.GET.get('id')
    selected_type = request.GET.get('type')
    
    if selected_type == 'teacher':
        teacher = Teacher.objects.get(pk=selected_id)
        students = teacher.students.all()
        data = [{'id': student.id, 'name': student.name} for student in students]
    else:
        student = Student.objects.get(pk=selected_id)
        teachers = student.teacher_set.all()
        data = [{'id': teacher.id, 'name': teacher.name} for teacher in teachers]
    
    return JsonResponse({'data': data})

def generate_certificate(request):
    teacher_id = request.GET.get('teacher_id')
    student_id = request.GET.get('student_id')
    
    teacher = Teacher.objects.get(pk=teacher_id)
    student = Student.objects.get(pk=student_id)
    
    certificate_text = f"""
    Certificate of Completion
    
    This is to certify that {student.name}
    has successfully completed the course under the guidance of
    {teacher.name}.
    
    Date: {str(datetime.now())}
    """

    token_data = {'student_name': student.name, 'teacher_name': teacher.name}
    jwt_token = generate_jwt_token(token_data)
    
    return render(request, 'certificate.html', {'certificate_text': certificate_text, 'jwt_token': jwt_token})

def verify_certificate(request):
    token = request.GET.get('token')
    
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        student_name = decoded_data['student_name']
        teacher_name = decoded_data['teacher_name']
        return JsonResponse({'message': f'Certificate verified for {student_name} under {teacher_name}.'})
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired.'})
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token.'})
