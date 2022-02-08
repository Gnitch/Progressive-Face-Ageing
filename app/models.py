from django.db import models
from django.contrib.auth.models import User

class Family(models.Model):
    father = models.CharField(max_length=150)
    mother = models.CharField(max_length=150)
    sibling = models.CharField(max_length=150, blank=True)  
    guardian = models.CharField(max_length=150, blank=True)
    contact1 = models.IntegerField()
    contact2 = models.IntegerField(blank=True)

class Missing(models.Model):
    choices_state = [
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),        
        ('GA', 'Goa'),        
        ('GJ', 'Gujarat'),        
        ('HR', 'Haryana'),        
        ('HP', 'Himachal Pradesh'),        
        ('JK', 'Jammu and Kashmir'),        
        ('JH', 'Jharkhand'),        
        ('KA', 'Karnataka'),        
        ('KL', 'Kerala'),        
        ('MP', 'Madhya Pradesh'),        
        ('MH', 'Maharashtra'),        
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),        
        ('MZ', 'Mizoram'),        
        ('NL', 'Nagaland'),        
        ('OD', 'Odisha'),        
        ('PB', 'Punjab'),        
        ('RJ', 'Rajasthan'),        
        ('SK', 'Sikkim'),  
        ('TN', 'Tamil Nadu'),  
        ('TG', 'Telangana'),  
        ('TR', 'Tripura'),  
        ('UT', 'Uttarakhand'),  
        ('UP', 'Uttar Pradesh'),  
        ('WB', 'West Bengal'),  
        ('AN', 'Andaman and Nicobar Islands'),  
        ('CH', 'Chandigarh'),  
        ('DN', 'Dadra and Nagar Haveli'),
        ('PY', 'Puducherry'),
        ('LD', 'Lakshadweep'),
        ('DL', 'Delhi'),
        ('DD', 'Daman and Diu')
    ]     
    choices_gender = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('none','Prefer Not To Say')
    ]             
    gender = models.CharField(choices=choices_gender, default='none', max_length=25)
    state = models.CharField(choices=choices_state, default='DL', max_length=30)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    weight = models.FloatField(blank=True)
    height = models.FloatField(blank=True)
    city = models.CharField(max_length=50)
    dob = models.DateField()
    adhar = models.IntegerField(blank=True)
    last_sighted = models.DateField()
    status = models.BooleanField(default=False)
    img_person = models.ImageField(upload_to="missing-people/", default="media/missing-people/park.JPG")
    family = models.ForeignKey(Family,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname + " " + self.lastname

    def get_absolute_url(self):
        return reverse('app:userView',args=[str(self.id)])

