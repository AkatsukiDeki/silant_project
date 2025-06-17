from rest_framework import serializers
from core.models import Vehicle, Maintenance, Complaint, Directory

class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    technique_model = DirectorySerializer()
    engine_model = DirectorySerializer()
    transmission_model = DirectorySerializer()
    driving_bridge_model = DirectorySerializer()
    controlled_bridge_model = DirectorySerializer()

    class Meta:
        model = Vehicle
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    type = DirectorySerializer()
    service_company = serializers.StringRelatedField()
    vehicle = serializers.StringRelatedField()

    class Meta:
        model = Maintenance
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    failure_node = DirectorySerializer()
    recovery_method = DirectorySerializer()
    service_company = serializers.StringRelatedField()
    vehicle = serializers.StringRelatedField()

    class Meta:
        model = Complaint
        fields = '__all__'