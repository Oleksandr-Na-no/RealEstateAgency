from django.db import models
from PIL import Image
import subprocess
import os
from django.conf import settings

# Create your models here.
class House(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    area = models.IntegerField()
    address = models.CharField(max_length=255)
    pevImage = models.ImageField(upload_to='default_image.png', blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address} - ${self.price}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # image_path = self.pevImage.path  # Adjust to your field name
        #має ранити С++ файл який проходиться по кожному пікселю і орбить його жовтішим
        # Запускаємо C++ програму

        image_path = os.path.join(settings.MEDIA_ROOT, self.pevImage.name)
 
        result = subprocess.run(
            ["realestate//ImageEditor//cmake-build-debug//ImageEditor.exe", "'"+image_path+"'"],
            capture_output=True, text=True
        )

        print("C++ Output:", result.stdout)


class Client(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incremented integer primary key
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    notes = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Realtor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    realtor = models.ForeignKey(Realtor, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    time = models.DateTimeField()
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Appointment on {self.time} - House: {self.house.id}, Client: {self.client.id}, Realtor: {self.realtor.id if self.realtor else 'N/A'}"
    

class Image(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='houseImages/') 

    def __str__(self):
        return f"Image for House ID: {self.house.id}"
