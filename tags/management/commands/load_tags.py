from typing import Any

from django.core.management import BaseCommand
from tags.models import Tag

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        Tag.objects.create(content='내과')
        Tag.objects.create(content='외과')
        Tag.objects.create(content='흉부외과')
        Tag.objects.create(content='안과')
        Tag.objects.create(content='정형외과')
        Tag.objects.create(content='신경외과')
        Tag.objects.create(content='산부인과')
        Tag.objects.create(content='성형외과')
        Tag.objects.create(content='피부과')
        Tag.objects.create(content='이비인후과')
        Tag.objects.create(content='치과')
        Tag.objects.create(content='재활의학과')
        Tag.objects.create(content='정신건강의학과')
        Tag.objects.create(content='비뇨기과')
        Tag.objects.create(content='신경과')
        Tag.objects.create(content='소아청소년과')
        Tag.objects.create(content='마취통증의학과')