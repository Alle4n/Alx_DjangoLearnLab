from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Report


# VIEW REPORTS
@permission_required('accounts.can_view', raise_exception=True)
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'reports/list.html', {'reports': reports})


# CREATE REPORT
@permission_required('accounts.can_create', raise_exception=True)
def create_report(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        Report.objects.create(title=title, content=content)
        return redirect('report_list')
    return render(request, 'reports/create.html')


# EDIT REPORT
@permission_required('accounts.can_edit', raise_exception=True)
def edit_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        report.title = request.POST.get("title")
        report.content = request.POST.get("content")
        report.save()
        return redirect('report_list')

    return render(request, 'reports/edit.html', {'report': report})


# DELETE REPORT
@permission_required('accounts.can_delete', raise_exception=True)
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    return redirect('report_list')
