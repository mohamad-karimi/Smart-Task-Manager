from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.all()

    tasks = sorted(
        tasks,
        key=lambda task: (
            task.completed,
            -task.priority_score(),
            task.deadline or "9999-12-31",
        ),
    )

    return render(
        request,
        "tasks/task_list.html",
        {"tasks": tasks},
    )


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("task_list")

    else:
        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {"form": form},
    )


def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)

    task.completed = not task.completed
    task.save()

    return redirect("task_list")


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    task.delete()

    return redirect("task_list")
