from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm, RegisterForm, StudyTaskForm, SubjectForm
from .models import StudyTask, Subject


def home(request):
    return render(request, "home.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            email = form.cleaned_data["email"].strip()
            password = form.cleaned_data["password"]
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    subjects = Subject.objects.filter(user=request.user)
    tasks = StudyTask.objects.filter(user=request.user)

    total_subjects = subjects.count()
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    progress = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

    upcoming_tasks = tasks.filter(deadline__gte=date.today()).order_by("deadline", "created_at")[:5]
    recent_tasks = tasks.order_by("-created_at")[:5]

    subject_summary = []
    for subject in subjects:
        subject_tasks = tasks.filter(subject=subject)
        subject_total = subject_tasks.count()
        subject_completed = subject_tasks.filter(completed=True).count()
        subject_progress = round((subject_completed / subject_total) * 100) if subject_total else 0
        subject_summary.append(
            {
                "subject": subject,
                "task_count": subject_total,
                "completed_count": subject_completed,
                "progress": subject_progress,
            }
        )

    context = {
        "total_subjects": total_subjects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress": progress,
        "upcoming_tasks": upcoming_tasks,
        "recent_tasks": recent_tasks,
        "subject_summary": subject_summary,
    }
    return render(request, "planner/dashboard.html", context)


@login_required
def subject_list(request):
    subjects = Subject.objects.filter(user=request.user).prefetch_related("tasks")
    subject_data = []
    for subject in subjects:
        task_count = subject.tasks.filter(user=request.user).count()
        subject_data.append({"subject": subject, "task_count": task_count})
    return render(request, "planner/subjects.html", {"subjects": subject_data})


@login_required
def subject_add(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, "Subject added successfully.")
            return redirect("subjects")
    else:
        form = SubjectForm()
    return render(request, "planner/subject_form.html", {"form": form, "title": "Add Subject"})


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect("subjects")
    else:
        form = SubjectForm(instance=subject)
    return render(request, "planner/subject_form.html", {"form": form, "title": "Update Subject", "subject": subject})


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    subject.delete()
    messages.success(request, "Subject deleted successfully.")
    return redirect("subjects")


@login_required
def task_list(request):
    subjects = Subject.objects.filter(user=request.user)
    tasks = StudyTask.objects.filter(user=request.user).select_related("subject")

    search = request.GET.get("search", "").strip()
    subject_id = request.GET.get("subject")
    priority = request.GET.get("priority")
    status = request.GET.get("status")
    sort = request.GET.get("sort", "deadline")

    if search:
        tasks = tasks.filter(title__icontains=search)
    if subject_id:
        tasks = tasks.filter(subject_id=subject_id)
    if priority:
        tasks = tasks.filter(priority=priority)
    if status == "completed":
        tasks = tasks.filter(completed=True)
    elif status == "pending":
        tasks = tasks.filter(completed=False)

    if sort == "priority":
        priority_order = Case(
            When(priority="HIGH", then=Value(3)),
            When(priority="MEDIUM", then=Value(2)),
            When(priority="LOW", then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
        tasks = tasks.order_by(priority_order.desc(), "deadline")
    elif sort == "created":
        tasks = tasks.order_by("-created_at")
    else:
        tasks = tasks.order_by("deadline", "created_at")

    context = {
        "tasks": tasks,
        "subjects": subjects,
        "search": search,
        "selected_subject": subject_id,
        "selected_priority": priority,
        "selected_status": status,
        "selected_sort": sort,
    }
    return render(request, "planner/tasks.html", context)


@login_required
def task_add(request):
    if request.method == "POST":
        form = StudyTaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully.")
            return redirect("tasks")
    else:
        form = StudyTaskForm(user=request.user)
    return render(request, "planner/task_form.html", {"form": form, "title": "Add Task"})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(StudyTask, pk=pk, user=request.user)
    return render(request, "planner/task_detail.html", {"task": task})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(StudyTask, pk=pk, user=request.user)
    if request.method == "POST":
        form = StudyTaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect("tasks")
    else:
        form = StudyTaskForm(user=request.user, instance=task)
    return render(request, "planner/task_form.html", {"form": form, "title": "Update Task", "task": task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(StudyTask, pk=pk, user=request.user)
    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect("tasks")


@login_required
def task_complete(request, pk):
    task = get_object_or_404(StudyTask, pk=pk, user=request.user)
    task.completed = True
    task.save(update_fields=["completed", "updated_at"])
    messages.success(request, "Task completed.")
    return redirect("tasks")


@login_required
def task_pending(request, pk):
    task = get_object_or_404(StudyTask, pk=pk, user=request.user)
    task.completed = False
    task.save(update_fields=["completed", "updated_at"])
    messages.success(request, "Task marked as pending.")
    return redirect("tasks")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    total_subjects = Subject.objects.filter(user=request.user).count()
    total_tasks = StudyTask.objects.filter(user=request.user).count()
    completed_tasks = StudyTask.objects.filter(user=request.user, completed=True).count()
    completed_percentage = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

    context = {
        "form": form,
        "total_subjects": total_subjects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress": completed_percentage,
    }
    return render(request, "planner/profile.html", context)


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
