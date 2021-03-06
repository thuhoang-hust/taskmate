from django.shortcuts import render, redirect
# from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

context = {
    'index_text': "Welcome to Index Page",
    'welcome_text': "Welcome to Todolist Page",
    'contact_text': "Welcome to Contact Us Page",
    'about_text': "Welcome to About Us Page"
}


@login_required
def todolist(request):
    if request.method == "POST":
        task_form = TaskForm(request.POST or None)
        if task_form.is_valid():
            task_form.save(commit=False).manage = request.user
            task_form.save()

        messages.success(request, ("New Task Added!"))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(manage=request.user)
        paginator = Paginator(all_tasks, 10)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)

        return render(request, 'todolist.html', {'all_tasks_key': all_tasks})


@login_required
def delete_task(request, task_id):
    task_obj = TaskList.objects.get(pk=task_id)
    if task_obj.manage == request.user:
        task_obj.delete()
        messages.success(request, ("Task Deleted!"))
    else:
        messages.error(request, ("Restricted!"))

    return redirect('todolist')


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task_obj = TaskList.objects.get(pk=task_id)
        task_form = TaskForm(request.POST or None, instance=task_obj)
        if task_form.is_valid():
            task_form.save()

        messages.success(request, ("Task Edited!"))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj_key': task_obj})


@login_required
def complete_task(request, task_id):
    task_obj = TaskList.objects.get(pk=task_id)
    if task_obj.manage == request.user:
        task_obj.done = True
        task_obj.save()
    else:
        messages.error(request, ("Restricted!"))
    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task_obj = TaskList.objects.get(pk=task_id)
    if task_obj.manage == request.user:
        task_obj.done = False
        task_obj.save()
    else:
        messages.error(request, ("Restricted!"))

    return redirect('todolist')


def index(request):
    return render(request, 'index.html', context)


def contact(request):
    return render(request, 'contact.html', context)


def about(request):
    return render(request, 'about.html', context)
