from rest_framework import serializers
from .models import ArticleModels,ShortCutUrlModels


class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = ArticleModels
        fields = ['id','writer','use_money','content','spending_date']
        extra_kwargs = {
            'id' : {'read_only':True},
            'writer': {'read_only': True},
            'content': {'required': False}
        }


class ShortCutUrlSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShortCutUrlModels
        fields = ['link','new_link']






