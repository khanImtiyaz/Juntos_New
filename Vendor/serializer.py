from rest_framework import serializers
from Juntos.models import *
from .models import *


class SubCategorySerializer(serializers.ModelSerializer):
	"""docstring for SubCategorySerializer"""
	
	class Meta:
		"""docstring for meta"""
		model = SubCategory
		fields = "__all__"
