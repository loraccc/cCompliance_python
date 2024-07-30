# appSection/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Section
from appCategory.models import Category
from .forms import SectionForm

@login_required
def section_list(request):
    sections = Section.objects.all()
    return render(request, 'section_list.html', {'sections': sections})

@login_required
def section_create(request, pk=None):
    section = None
    if pk:
        section = get_object_or_404(Section, pk=pk)

    if request.method == "POST":
        section_form = SectionForm(request.POST, instance=section)
        if section_form.is_valid():
            section = section_form.save()
            return redirect('section_list')
    else:
        section_form = SectionForm(instance=section)

    return render(request, 'section_form.html', {'section_form': section_form, 'section': section})

@login_required
def section_update(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        section_form = SectionForm(request.POST, instance=section)
        if section_form.is_valid():
            section_form.save()
            return redirect('section_list')
    else:
        section_form = SectionForm(instance=section)

    return render(request, 'section_form.html', {'section_form': section_form, 'section': section})

@login_required
def section_delete(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section.delete()
        messages.success(request, "Section deleted successfully.")
        return redirect('section_list')
    return render(request, 'section_confirm_delete.html', {'section': section})

