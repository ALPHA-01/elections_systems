from rest_framework import serializers
from .models import Position, Candidate, Voter, Vote

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'description', 'active', 'blockchain_sync', 'blockchain_tx_hash', 'blockchain_id']
        read_only_fields = ['blockchain_sync', 'blockchain_tx_hash', 'blockchain_id']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'position', 'bio', 'photo', 'blockchain_sync', 'blockchain_tx_hash', 'blockchain_id']
        read_only_fields = ['blockchain_sync', 'blockchain_tx_hash', 'blockchain_id']

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id', 'name', 'ethereum_address', 'email', 'is_active']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'voter', 'candidate', 'timestamp', 'blockchain_sync', 'blockchain_tx_hash']
        read_only_fields = ['timestamp', 'blockchain_sync', 'blockchain_tx_hash']