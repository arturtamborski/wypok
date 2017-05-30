from allauth.account.decorators import verified_email_required as login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.urls import reverse
from django.conf import settings

from wypok.cache import mark_for_caching
from wypok.utils.membership_required import membership_required
from wypok.utils.ownership_required import ownership_required
from sections.models import Section
from sections.forms import SectionCreateForm, SectionUpdateForm, SectionDeleteForm


def home(request):
    if settings.DEFAULT_SECTION:
        return redirect('sections:detail', settings.DEFAULT_SECTION)
    return redirect('sections:listing')


@ownership_required(Section, raise_exception=False, name='section')
def detail(request, section):
    return render(request, 'sections/detail.html', dict(
        section = section,
    ))


def listing(request):
    sections = get_list_or_404(Section)

    return render(request, 'sections/listing.html', dict(
        sections = sections,
    ))


@login_required
@membership_required('staff')
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
@membership_required('staff')
@ownership_required(Section, name='section')
def update(request, section):
    form = SectionUpdateForm(instance=section)

    if request.method == 'POST':
        form = SectionUpdateForm(request.POST, instance=section)
        if form.is_valid():
            section = form.save()
            return redirect(section)

    return render(request, 'sections/update.html', dict(
        section = section,
        form = form,
    ))


@login_required
@membership_required('staff')
@ownership_required(Section, name='section')
def delete(request, section):
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
