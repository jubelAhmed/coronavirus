from django.db import models
from userApp.models import UserProfile
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import datetime


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Thana(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Category(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    title = models.CharField(max_length=255, verbose_name="Title")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


class Organisation(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    about = RichTextUploadingField()
    org_category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True,blank=True)
    division = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    thana = models.ForeignKey(Thana, on_delete=models.SET_NULL, null=True)
    postal_area = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    objects = models.QuerySet()
    
    def get_all_successful_projects(self):
        org_projects = self.org_projects.filter(status=True, end_date__lte=datetime.date.today()).order_by('end_date')
        return org_projects
    def get_all_running_projects(self):
        org_projects = self.org_projects.filter(status=True, end_date__gte=datetime.date.today()).order_by('end_date')
        return org_projects


    def __str__(self):
        return f"{self.name}"


class OrgDetail(models.Model):
    organisation = models.OneToOneField(Organisation, on_delete=models.CASCADE, related_name='org_detail')
    image = models.ImageField(upload_to='images/org/', null=True, blank=True)
    logo = models.ImageField(upload_to='images/logo/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    facebook_url = models.URLField(max_length=2000)
    twitter_url = models.URLField(max_length=2000,null=True, blank=True)
    youtube_url = models.URLField(max_length=2000,null=True, blank=True)
    website_url = models.URLField(max_length=2000,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.facebook_url}"


class OrgProject(models.Model):
    project_name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organisation, on_delete=models.CASCADE,related_name='org_projects')
    selected_area = models.CharField(max_length=255,null=True, blank=True)
    details = RichTextUploadingField()
    duration = models.DateTimeField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    project_image = models.ImageField(upload_to='images/org/project/', null=True, blank=True)
    budget = models.CharField(max_length=255,null=True, blank=True)
    status = models.BooleanField(verbose_name="status",default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        get_latest_by = "-created_date"
        ordering = ['-created_date']

 
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('orgApplication:org_project_view_details', args=[str(self.id)])
    
   
    def __str__(self):
        return self.project_name
