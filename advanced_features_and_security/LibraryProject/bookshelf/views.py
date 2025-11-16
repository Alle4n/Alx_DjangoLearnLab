from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from accounts.models import Report  # adjust import if Report is in accounts/models.py


# -------------------------------
# Book Views (required by checker)
# -------------------------------
@login_required
def book_list(request):
    books = Book.objects.all()  # context variable "books"
    return render(request, "bookshelf/book_list.html", {"books": books})


# -------------------------------
# Report Views with Permissions
# -------------------------------
@permission_required('accounts.can_view', raise_exception=True)
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'reports/list.html', {'reports': reports})


@permission_required('accounts.can_create', raise_exception=True)
def create_report(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        Report.objects.create(title=title, content=content)
        return redirect('report_list')
    return render(request, 'reports/create.html')


@permission_required('accounts.can_edit', raise_exception=True)
def edit_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        report.title = request.POST.get("title")
        report.content = request.POST.get("content")
        report.save()
        return redirect('report_list')

    return render(request, 'reports/edit.html', {'report': report})


@permission_required('accounts.can_delete', raise_exception=True)
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    return redirect('report_list')