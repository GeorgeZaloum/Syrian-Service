"""
Serializers for problem reporting.
"""
from rest_framework import serializers
from .models import ProblemReport


class ProblemReportCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating problem reports."""
    
    class Meta:
        model = ProblemReport
        fields = ['input_type', 'problem_text', 'audio_file']
        extra_kwargs = {
            'problem_text': {'required': False},  # Not required if audio_file is provided
            'audio_file': {'required': False},  # Not required if problem_text is provided
        }
    
    def validate(self, data):
        """
        Validate that either problem_text or audio_file is provided.
        """
        input_type = data.get('input_type')
        problem_text = data.get('problem_text')
        audio_file = data.get('audio_file')
        
        if input_type == 'TEXT':
            if not problem_text or not problem_text.strip():
                raise serializers.ValidationError({
                    'problem_text': 'Problem text is required for text input type.'
                })
            # Clear audio_file if provided for TEXT type
            data['audio_file'] = None
            
        elif input_type == 'VOICE':
            if not audio_file:
                raise serializers.ValidationError({
                    'audio_file': 'Audio file is required for voice input type.'
                })
        else:
            raise serializers.ValidationError({
                'input_type': 'Invalid input type. Must be TEXT or VOICE.'
            })
        
        return data


class ProblemReportSerializer(serializers.ModelSerializer):
    """Serializer for retrieving problem reports."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = ProblemReport
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'input_type',
            'problem_text',
            'audio_file',
            'recommendations',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'recommendations', 'created_at', 'updated_at']


class ProblemReportListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing problem reports."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    recommendation_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ProblemReport
        fields = [
            'id',
            'user_email',
            'input_type',
            'problem_text',
            'recommendation_count',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_recommendation_count(self, obj):
        """Get the number of recommendations."""
        return len(obj.recommendations) if obj.recommendations else 0
