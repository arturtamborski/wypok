from . import models


def sections(request):
    sections = models.Section.objects.all()
    return {'sections': sections}
