from rest_framework import serializers
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user']  # чтобы клиент не передавал

    def create(self, validated_data):
        return Habit(**validated_data)