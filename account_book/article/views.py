import random

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.settings import SHORT_CUT_BASE_URL
from .models import ArticleModels, ShortCutUrlModels
from users.permissions_util import *
from .serializers import *
from .short_cut_util import convert


class ArticleAPI(ListCreateAPIView):
    queryset = ArticleModels.objects.all()
    serializer_class = ArticleSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(writer=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(writer=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ArticleDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = ArticleModels.objects.all()
    serializer_class = ArticleSerializers
    permission_classes = [IsOwnerOrReadOnly]


class ActionViewSet(viewsets.GenericViewSet):
    queryset = ArticleModels.objects.all()
    serializer_class = ArticleSerializers
    permission_classes = [IsOwnerOrReadOnly]

    @action(methods=['POST'], detail=True)
    def copy(self, request, pk):
        queryset = self.queryset.get(id=pk)
        copy_queryset = ArticleModels(
            writer=queryset.writer,
            use_money=queryset.use_money,
            content=queryset.content,
            spending_date=queryset.spending_date
        )
        serializer = self.get_serializer(instance=copy_queryset, many=False)
        copy_queryset.save()
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=True)
    def shot_url(self, request, pk):
        url = f"/api/article/{pk}"
        try:
            short_cut = ShortCutUrlModels.objects.get(make_user=request.user, link=url)
            if not short_cut.check_is_using_time():
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            new_link = SHORT_CUT_BASE_URL + convert()
            short_cut = ShortCutUrlModels.objects.create(
                make_user=request.user,
                link=url,
                new_link=new_link
            )
        serializer = ShortCutUrlSerializers(instance=short_cut, many=False)
        return Response(data=serializer.data)


@api_view(('GET',))
def origin_redirect(request, new_link):
    try:
        short_cut = ShortCutUrlModels.objects.get(new_link__contains=new_link,)
        if not short_cut.check_is_using_time():
            data = {
                'results': {
                    'mag': "해당 URL은 만료되었습니다.",
                    'code': 'E3010'
                }
            }
            r_status = status.HTTP_301_MOVED_PERMANENTLY
        else:
            data = ShortCutUrlSerializers(instance=short_cut,many=False)
            r_status = status.HTTP_200_OK
        return Response(data=data, status=r_status)
    except ObjectDoesNotExist:
        data = {
            'results': {
                'mag': "해당 URL은 존재하지 않습니다.",
                'code': 'E4040'
            }
        }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
