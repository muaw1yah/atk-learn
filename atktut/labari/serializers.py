from rest_framework import serializers
from .models import Labari

class LabariSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Labari
        fields = '__all__'