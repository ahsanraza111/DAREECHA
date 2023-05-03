from django.db import models
from django.contrib.auth.models import User
from datetime import date
import uuid

from baham.constants import COLORS, TOWNS
from baham.enum_types import VehicleType, UserType, VehicleStatus




# Custom Validators

def validate_colors(value):  
    return value.upper() in COLORS




# Create your models here.

class UserProfile(models.Model):
    voided = models.BooleanField(default=False, null=False, blank=False)
    date_created = models.DateField(default=date.today, null=False, blank=False)
    date_updated = models.DateField()
    date_voided =  models.DateField()
    created_by = models.CharField(max_length = 50,null=False, blank=False, editable=False)
    updated_by = models.CharField(max_length=50)
    voided_by = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    type = models.CharField(max_length=10, choices=[(t.name, t.value) for t in UserType])
    primary_contacts = models.CharField(max_length=20, null=False, blank=False)
    alternate_contacts = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=255)
    address_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    address_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    landmark = models.CharField(max_length=255, null=False)
    town = models.CharField(max_length=50, null=False, choices=[(c, c) for c in TOWNS])
    active = models.BooleanField(default=True, editable=False)
    date_deactivated = models.DateTimeField(editable=False, null=True)
    bio = models.TextField()
   

    def delete(self, *args, **kwargs):
        if self.user.is_staff == True:
            super().delete(*args, **kwargs) 

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"
    


class VehicleModel(models.Model):
    voided = models.BooleanField(default=False, null=False, blank=False)
    date_created = models.DateField(default=date.today, null=False, blank=False)
    date_updated = models.DateField()
    date_voided =  models.DateField()
    created_by = models.CharField(max_length = 50,null=False, blank=False, editable=False)
    updated_by = models.CharField(max_length=50)
    voided_by = models.CharField(max_length=50)
    model_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    vendor = models.CharField(max_length=20, null=False, blank=False)
    model = models.CharField(max_length=50, null=False, blank=False, default='Unknown')
    type = models.CharField(max_length=50, choices=[(t.name, t.value) for t in VehicleType], help_text="Select the vehicle chassis type")
    capacity = models.PositiveSmallIntegerField(null=False, default=2);
    

    class Meta:
        db_table = 'baham_vehicle_model'

    def __str__(self):
        return f"{self.vendor} {self.model}"



class Vehicle(models.Model):
    voided = models.BooleanField(default=False, null=False, blank=False)
    date_created = models.DateField(default=date.today, null=False, blank=False)
    date_updated = models.DateField()
    date_voided =  models.DateField()
    created_by = models.CharField(max_length = 50,null=False, blank=False, editable=False)
    updated_by = models.CharField(max_length=50)
    voided_by = models.CharField(max_length=50)
    vehicle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    registration_number = models.CharField(max_length=10, unique=True, null=False, blank=False,
                                           help_text="Unique registration/license plate no. of the vehicle.")
    color = models.CharField(max_length=50, default='white', validators=[validate_colors])
    model = models.ForeignKey(VehicleModel, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[(t.name, t.value) for t in VehicleStatus])
    picture1 = models.ImageField(upload_to='pictures', null=True)
    picture2 = models.ImageField(upload_to='pictures', null=True)
    
    def delete(self, *args, **kwargs):
        if self.owner.user.is_staff == True:
            super().delete(*args, **kwargs) 
    
    def __str__(self):
        return f" {self.model.vendor} {self.model.model} {self.color}"




class Contracts(models.Model):
    voided = models.BooleanField(default=False, null=False, blank=False)
    date_created = models.DateField(default=date.today, null=False, blank=False)
    date_updated = models.DateField()
    date_voided =  models.DateField()
    created_by = models.CharField(max_length = 50,null=False, blank=False, editable=False)
    updated_by = models.CharField(max_length=50)
    voided_by = models.CharField(max_length=50)
    contract_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    vehicle = models.ForeignKey(Vehicle, null=False, on_delete=models.CASCADE)
    companion = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE)
    effective_start_date = models.DateField(null=False)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    fuel_share = models.PositiveSmallIntegerField(help_text="Percentage of fuel cost")
    maintenance_share = models.PositiveSmallIntegerField(help_text="Percentage of maintenance share")
    schedule = models.CharField(max_length=255, null=False)
    

    def delete(self, *args, **kwargs):
        if self.companion.user.is_staff == True:
            super().delete(*args, **kwargs) 