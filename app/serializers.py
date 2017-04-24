from . import models
from wmap2017 import settings
from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry, LineString, Point, Polygon


class UserMeSerializer(geo_serializers.GeoFeatureModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        geo_field = "last_location"
        fields = (
            "id", "username", "first_name", "last_name", "email", "is_superuser", "is_staff",
            "is_active", "date_joined", "last_login", "url")

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(reverse("rest:user-username", kwargs={"uid": obj.pk}))


class UserOtherSerializer(geo_serializers.GeoFeatureModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        geo_field = "last_location"
        fields = ("id", "username", "first_name", "last_name", "email", "url")

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(reverse("rest:user-username", kwargs={"uid": obj.pk}))
