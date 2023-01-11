import random

from django.core.exceptions import ObjectDoesNotExist

from config.settings import SHORT_CUT_BASE_URL
from article.models import ShortCutUrlModels


def convert():
    encoding = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
               [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
               [str(i) for i in range(1, 10)]
    while True:
        new_link = ''.join(random.sample(encoding, 8))
        try:
            ShortCutUrlModels.objects.get(new_link=SHORT_CUT_BASE_URL+new_link)
        except ObjectDoesNotExist:
            return new_link