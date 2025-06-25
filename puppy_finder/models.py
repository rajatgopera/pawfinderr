from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='user_uploads/', blank=True)
    
    def __str__(self):
        return self.username

class Puppy(models.Model):
    LOST = 'LOST'
    FOUND = 'FOUND'
    REUNITED = 'REUNITED'
    
    STATUS_CHOICES = [
        (LOST, 'Lost'),
        (FOUND, 'Found'),
        (REUNITED, 'Reunited'),
    ]
    
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(30)]
    )
    size = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    last_seen_location = models.CharField(max_length=255)
    last_seen_date = models.DateField(default=timezone.now)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=LOST)
    image = models.ImageField(upload_to='puppy_images/')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    # Additional fields as per user request
    distinctive_features = models.TextField(blank=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    additional_notes = models.TextField(blank=True)
    has_microchip = models.BooleanField(default=False)
    has_collar = models.BooleanField(default=False)
    microchip_number = models.CharField(max_length=50, blank=True)
    collar_description = models.CharField(max_length=200, blank=True)
    
    # 3D model fields
    model_3d = models.FileField(upload_to='3d_models/', blank=True, null=True)
    model_texture = models.ImageField(upload_to='3d_textures/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    puppy = models.ForeignKey(Puppy, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

class Reunion(models.Model):
    puppy = models.ForeignKey(Puppy, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='reunions_as_owner', on_delete=models.CASCADE)
    finder = models.ForeignKey(CustomUser, related_name='reunions_as_finder', on_delete=models.CASCADE, null=True, blank=True)
    reunion_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Reunion for {self.puppy.name} on {self.reunion_date}"
