from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import os

from .models import Position, Candidate, Voter, Vote
from .serializers import PositionSerializer, CandidateSerializer, VoterSerializer, VoteSerializer
from .ethereum_interface import add_position, add_candidate, cast_vote, get_candidate_votes

class PositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for positions.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to also add position to blockchain"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save to database
        self.perform_create(serializer)
        
        # Add to blockchain
        blockchain_result, success = add_position(
            serializer.validated_data['name'],
            private_key=os.environ.get('ADMIN_PRIVATE_KEY')
        )
        
        # Update position with blockchain status
        if success:
            position = serializer.instance
            position.blockchain_sync = True
            position.blockchain_tx_hash = blockchain_result.get('tx_hash')
            position.save()
        
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data['blockchain_result'] = blockchain_result
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class CandidateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for candidates.
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to also add candidate to blockchain"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save to database
        self.perform_create(serializer)
        
        # Add to blockchain
        position_id = serializer.validated_data['position'].id
        blockchain_result, success = add_candidate(
            serializer.validated_data['name'],
            position_id,
            private_key=os.environ.get('ADMIN_PRIVATE_KEY')
        )
        
        # Update candidate with blockchain status
        if success:
            candidate = serializer.instance
            candidate.blockchain_sync = True
            candidate.blockchain_tx_hash = blockchain_result.get('tx_hash')
            candidate.save()
        
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data['blockchain_result'] = blockchain_result
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['get'])
    def blockchain_votes(self, request, pk=None):
        """Get candidate vote count from blockchain"""
        candidate = self.get_object()
        votes = get_candidate_votes(candidate.id)
        
        if votes is not None:
            return Response({'votes': votes})
        else:
            return Response({'error': 'Failed to get vote count from blockchain'}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VoterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for voters.
    """
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer


class VoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for votes.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to also cast vote on blockchain"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get voter and candidate
        voter = serializer.validated_data['voter']
        candidate = serializer.validated_data['candidate']
        
        # Save to database
        self.perform_create(serializer)
        
        # Cast vote on blockchain
        blockchain_result, success = cast_vote(
            candidate_id=candidate.id,
            voter_address=voter.ethereum_address,
            private_key=request.data.get('private_key')  # Needs to be provided in request!
        )
        
        # Update vote with blockchain status
        if success:
            vote = serializer.instance
            vote.blockchain_sync = True
            vote.blockchain_tx_hash = blockchain_result.get('tx_hash')
            vote.save()
        
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data['blockchain_result'] = blockchain_result
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)