from allauth.account.decorators import verified_email_required as login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.conf import settings

from wypok.cache import mark_for_caching
from sections.models import Section
from sections.forms import SectionCreateForm, SectionUpdateForm, SectionDeleteForm


def home(request):
    if settings.DEFAULT_SECTION:
        return redirect('sections:detail', settings.DEFAULT_SECTION)
    return redirect('sections:listing')


def detail(request, section):
    section = get_object_or_404(Section, name=section)

    return render(request, 'sections/detail.html', dict(
        section = section,
    ))


def listing(request):
    sections = get_list_or_404(Section)

    return render(request, 'sections/listing.html', dict(
        sections = sections,
    ))


@login_required
def create(request):
    form = SectionCreateForm()

    if request.method == 'POST':
        form = SectionCreateForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.admin = request.user
            section.save()
            return redirect(section)

    return render(request, 'sections/create.html', dict(
        form = form,
    ))


@login_required
def update(request, section):
    section = get_object_or_404(Section, name=section)
    form = SectionUpdateForm(instance=section)

    if request.method == 'POST':
        form = SectionUpdateForm(request.POST, instance=section)
        if form.is_valid():
            section = form.save()
            section.save()
            return redirect(section)

    return render(request, 'sections/update.html', dict(
        section = section,
        form = form,
    ))


@login_required
def delete(request, section):
    section = get_object_or_404(Section, name=section)
    form = SectionDeleteForm(instance=section)

    if request.method == 'POST':
        form = SectionDeleteForm(request.POST, instance=section)
        if form.is_valid():
            section.delete()
            return redirect('sections:home')

    return render(request, 'sections/delete.html', dict(
        section = section,
        form = form,
    ))
