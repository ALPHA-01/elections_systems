from django.db import models

class Position(models.Model):
    """
    Model representing an election position.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    # Blockchain related fields
    blockchain_sync = models.BooleanField(default=False)
    blockchain_tx_hash = models.CharField(max_length=100, blank=True, null=True)
    blockchain_id = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Candidate(models.Model):
    """
    Model representing a candidate for a position.
    """
    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='candidates/', blank=True, null=True)
    # Blockchain related fields
    blockchain_sync = models.BooleanField(default=False)
    blockchain_tx_hash = models.CharField(max_length=100, blank=True, null=True)
    blockchain_id = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.position.name}"

class Voter(models.Model):
    """
    Model representing a voter.
    """
    name = models.CharField(max_length=100)
    ethereum_address = models.CharField(max_length=42, unique=True)  # Ethereum address of the voter
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Vote(models.Model):
    """
    Model representing a vote cast by a voter.
    """
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='received_votes')
    timestamp = models.DateTimeField(auto_now_add=True)
    # Blockchain related fields
    blockchain_sync = models.BooleanField(default=False)
    blockchain_tx_hash = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        unique_together = ('voter', 'candidate')
        
    def __str__(self):
        return f"{self.voter.name} voted for {self.candidate.name}"