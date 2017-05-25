from sections.models import Section


def sections(request):
    return dict(
        sections = Section.objects.all(),
    )
