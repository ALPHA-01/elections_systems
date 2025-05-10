from django.urls import path, include
from rest_framework.routers import DefaultRouter

from voting_main.ethereum_interface import candidate_count_view
from .views import PositionViewSet, CandidateViewSet, VoterViewSet, VoteViewSet

router = DefaultRouter()
router.register('positions', PositionViewSet)
router.register('candidates', CandidateViewSet)
router.register('voters', VoterViewSet)
router.register('votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('candidates/count/', candidate_count_view, name='candidate-count'),
]
