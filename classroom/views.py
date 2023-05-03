from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Classroom, Student
from .serializers import ClassroomSerializer, StudentSerializer

# Create your views here.


class ClassroomList(generics.ListCreateAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        queryset = Classroom.objects.all().prefetch_related("students")
        student_capacity = self.request.query_params.get("student_capacity", None)
        if student_capacity is not None:
            queryset = queryset.filter(
                student_capacity=student_capacity
            ).prefetch_related("students")
        return queryset


class ClassroomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all().prefetch_related("classrooms")
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ClassRoomStudentsAPIView(APIView):
    def get(self, request, pk):
        classroom = get_object_or_404(Classroom, pk=pk)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data)

    def post(self, request, pk):
        classroom = get_object_or_404(Classroom, pk=pk)
        student = get_object_or_404(Student, pk=request.data["student_id"])
        classroom.students.add(student)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data)

    def delete(self, request, pk):
        classroom = get_object_or_404(Classroom, pk=pk)
        student = get_object_or_404(Student, pk=request.data["student_id"])
        classroom.students.remove(student)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data)
