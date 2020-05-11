from django import forms
from orgApp import models
from django.utils.translation import ugettext_lazy as _


class CategoryMainRegForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = '__all__'


class OrganisationMainRegForm(forms.ModelForm):
    # org_details = forms.ModelChoiceField(orgDetail.objects.all())
    class Meta:
        model = models.Organisation
        fields = ('name', 'about', 'division', 'district', 'thana', 'phone', 'email')
        labels = {
            'name': _('সংস্থার নাম'),
            'about': _('সংস্থার উদ্দেশ্য ও কাজ'),
            'division': _('বিভাগ'),
            'district': _('জেলা'),
            'thana': _('থানা'),
            'phone': _('মোবাইল নাম্বার'),
            'email': _('ইমেইল'),

        }


class OrgDetailMainRegForm(forms.ModelForm):
    class Meta:
        model = models.OrgDetail
        fields = ('image', 'logo', 'facebook_url', 'website_url', 'youtube_url')
        labels = {
            'image': _('সংস্থার গ্রপ ছবি'),
            'logo': _('লগো'),
            'facebook_url': _('ফেসবুক পেজ লিংক'),
            'website_url': _('ওয়েবসাইট লিংক'),
            'youtube_url': _('ইউটিউব লিংক'),

        }


from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime
from coresite import settings
from django.forms.fields import DateField
# from bootstrap_datepicker.widgets import DatePicker

class OrgProjectMainRegForm(forms.ModelForm):
    
    start_date = DateField(input_formats=settings.DATE_INPUT_FORMATS,widget=AdminDateWidget())
    end_date = DateField(input_formats=settings.DATE_INPUT_FORMATS,widget=AdminDateWidget())

    class Meta:
        model = models.OrgProject
        fields = ('project_name', 'selected_area', 'details', 'start_date', 'end_date','project_image', 'budget')
        
        help_texts = {
            'project_name': _('আপনার প্রজেক্টের নাম প্রয়োজনের উপর ভিত্তি করে লিখুন'),
            'selected_area': _('আরামবাগ, মোহাম্মদপুর, ধানমন্ডি '),
            'budget': _('২০০০০'),
        }
        labels = {
            'project_name': _('প্রজেক্টের নাম'),
            'selected_area': _('আপনার প্রস্তাবিত এলাকার নাম বা ব্যাক্তির নাম '),
            'details': _('প্রজেক্টের বিস্তারিত বর্ণনা'),
            'start_date': _('সংগ্রহের শুরুর তারিখ'),
            'end_date': _('সংগ্রহের শেষ তারিখ'),
            'project_image': _('প্রস্থাবিত ছবি'),
            'budget': _('প্রয়োজনীয় প্ররিমান টাকা'),

        }
        
        # extra code 
    # def __init__(self, *args, **kwargs):
    #     super(AdminDateWidget, self).__init__(*args, **kwargs)
    #     self.input_formats = ('%m/%d/%Y',)
      # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'textinputclass'}),
        # }
    # def save(self, commit=True):
    #     instance = super().save(commit)
    #     # set Car reverse foreign key from the Person model
    #     instance.org_details_set.add(self.cleaned_data['org_details'])
    #     return instance
    
        

"""
If we need any extra features in form we will create a class which will extends those class accordingly...
"""
