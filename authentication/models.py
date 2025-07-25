from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid


class NonDeletableUser(User):
    """Proxy model to prevent deletion of admin users"""
    
    class Meta:
        proxy = True
    
    def delete(self, *args, **kwargs):
        # Prevent deletion of superusers and admin users
        if self.is_superuser or (hasattr(self, 'memberprofile') and self.memberprofile.is_super_admin):
            raise ValidationError("👑 This admin user cannot be deleted for system security.")
        return super().delete(*args, **kwargs)


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    email = models.EmailField()
    token = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid.uuid4())
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Email verification for {self.user.username} - {self.email}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid.uuid4())
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=1)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Password reset token for {self.user.username}"


class GoogleAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='google_auth')
    google_id = models.CharField(max_length=200, unique=True)
    google_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Google auth for {self.user.username}"
