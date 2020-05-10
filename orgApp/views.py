from django.contrib import messages
from django.shortcuts import render
from .models import *
from django.http import HttpRequest, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, reverse
from orgApp import forms
from userApp.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .filters import OrganisationFilter
from django.urls import reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect
import datetime
from django.views.generic.edit import DeleteView



# Create your views here.

def home(request):
    
    total_org_list = Organisation.objects.filter(status=True).count()
    divisions = City.objects.all().order_by('name')
    districts = District.objects.all().order_by('name')
    thanas = Thana.objects.all().order_by('name')
    all_org_page_obj = None
    context = {}
    if total_org_list > 0:
        all_org = Organisation.objects.filter(status=True).order_by('name')
        paginator = Paginator(all_org, 10) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        all_org_page_obj = paginator.get_page(page_number)
    else:
        all_org = False
    
    total_org_project_list = OrgProject.objects.filter(status=True,end_date__gte=datetime.date.today()).count()
    all_running_projects = None
    if total_org_project_list > 0:
        all_running_projects = OrgProject.objects.filter(status=True,end_date__gte=datetime.date.today()).order_by('end_date')
    
    context = {
        'organisation_list': all_org_page_obj,
        'all_running_projects': all_running_projects,
        'divisions': divisions,
        'districts': districts,
        'thanas': thanas,
        'nbar': 'home',
    }
    return render(request, 'index_main.html', context)


def OrgDetailView(request,pk):
    
    all_org = Organisation.objects.filter(status=True).get(pk=pk)
   
    context = {
        'organisation': all_org,  
        'pk': all_org.pk,  
    }
    return render(request, 'orgApp/org_details.html', context)

def search(request):
    org_list = Organisation.objects.filter(status=True)
    
    org_filter = OrganisationFilter(request.GET, queryset=org_list)
    
    return render(request, 'orgApp/org_list.html', {'organisation_list': org_filter})
 
#  organization admin panel
 
@login_required
def orgnaziation_redirect(request):
    user = request.user
    org_count= Organisation.objects.filter(owner=user).count()
    
    if org_count > 0:
        request.session['org_have'] = True
        org = Organisation.objects.filter(owner=user)[:1].get()
        context = {
        'organisation': org,
        'profile_have':True,
        'org_have': request.session.get('org_have'),
        'nbar':'org',
  
        }
        return render(request, 'orgApp/org_profile.html', context)
        
    else:
        request.session['org_have'] = False
        return HttpResponseRedirect(reverse("orgApplication:self_org"))

@login_required
def get_org_profile_list(request):
    user = request.user
    org_count= Organisation.objects.filter(owner=user).count()
    
    if org_count > 0:
        request.session['org_have'] = True
        org = Organisation.objects.filter(owner=user)
        context = {
        'organisation_list': org,
        'nbar':'org',        
        
        }
        return render(request, 'orgApp/org_menu_list.html', context)
    else:
        return render(request, 'orgApp/org_menu_list.html', context = {
        'organisation_list': False,
        'nbar':'org',        
        
        })
    
@login_required
def organizationProfile(request,pk):
    user = request.user
    total_org_list = Organisation.objects.all().count()
    context  ={}
    profile_have = False
    if total_org_list > 0:
        org= Organisation.objects.filter(owner=user).get(pk=pk)
        profile_have = True
        context = {
            'profile_have':profile_have,
            'organisation':org,
            'nbar':'org',
            'profile_bar':'org_details',
        }
    else: 
        context = {
            'profile_have':profile_have,
        }
    
    return render(request, 'orgApp/org_profile.html',context=context)
    

@login_required
def self_org(request: HttpRequest):
    logged_in_user = request.user
    # user = UserProfile.objects.all()[:1].get()
    queryset = Organisation.objects.filter()
    # new = True if queryset.count() == 0 else None
    new = True
    context = {'queryset': queryset, 'errorMsg': None, 'new': new,'nbar':'org'}

    # check for request type
    context['nbar'] = 'org'
    if request.method == 'GET':
        if new:
            form = forms.OrganisationMainRegForm()
            org_detail_form = forms.OrgDetailMainRegForm()

            context['orgForm'] = form
            context['org_detail_form'] = org_detail_form
        return render(request, 'orgApp/selfOrg.html', context)
    elif request.method == 'POST':
        if new:
            form = forms.OrganisationMainRegForm(request.POST,request.FILES)
            orgForm = forms.OrgDetailMainRegForm(request.POST, request.FILES)
            if form.is_valid() and orgForm.is_valid():
                new_org = form.save(commit = False)
                new_org.owner = logged_in_user
                new_org = form.save(commit = True)
                details = orgForm.save(commit=False)
                details.organisation = new_org
                details.save()
                messages.add_message(request, messages.SUCCESS, "রেজিস্ট্রেশন করার জন্যে আপনাকে ধন্যবাদ")
                messages.add_message(request, messages.SUCCESS, "আপানার প্রতিষ্ঠান আমাদের এডমিন গ্রুপ যাচাই করবে, আপনার সকল তথ্য সঠিক হলে আমরা অনুমোদন দিব, আপনাকে কিছুক্ষন অপেক্ষা করতে হবে")
                return HttpResponseRedirect(reverse("orgApplication:self_org"))
        # context['errorMsg'] = 'Not new user'
        return render(request, 'orgApp/selfOrg.html', context)



@login_required
def edit_org(request,pk):
    logged_in_user = request.user
    org = get_object_or_404(Organisation, pk=pk)
    org_details = org.org_detail
  
    if request.method == 'POST':
        form = forms.OrganisationMainRegForm(request.POST,request.FILES,instance=org)
        orgForm = forms.OrgDetailMainRegForm(request.POST, request.FILES,instance=org_details)
        if form.is_valid() and orgForm.is_valid():
            new_org = form.save(commit = False)
            new_org.owner = logged_in_user
            new_org = form.save(commit = True)
            details = orgForm.save(commit=False)
            details.organisation = new_org
            details.save()
            return HttpResponseRedirect(reverse("orgApplication:org"))
    else:
        org_form = forms.OrganisationMainRegForm(instance=org)
        org_detail_form = forms.OrgDetailMainRegForm(instance=org_details)
    
    context={
            'orgForm':org_form,
             'org_detail_form':org_detail_form,
             'nbar':'org',
             'profile_bar':'org_edit',
             'organisation':org,
             }
    
    return render(request,'orgApp/org_edit.html',context=context)


def load_city(request):
    city = City.objects.all().order_by('name')
    return render(request, 'orgApp/city_dropdown_list_options.html', {'divisions': city})

def load_district(request):
    division_id = request.GET.get('city')
    
    districts = District.objects.filter(city=division_id).order_by('name')
    return render(request, 'orgApp/district_dropdown_list_options.html', {'districts': districts})

def load_thana(request):
    district_id = request.GET.get('district')
    
    thana = Thana.objects.filter(district=district_id).order_by('name')

    return render(request, 'orgApp/thana_dropdown_list_options.html', {'thana': thana})

@login_required
def org_project_create_view(request,pk):
    template_name = "orgApp/org_project_create.html"
    org = get_object_or_404(Organisation,pk=pk)
    project_main_form = forms.OrgProjectMainRegForm(request.POST or None, request.FILES or None )   
    
    if request.method == 'POST':
        if project_main_form.is_valid():
            start_date = project_main_form.cleaned_data['start_date']
            end_date = project_main_form.cleaned_data['end_date']
            project_name = project_main_form.cleaned_data['project_name']
            selected_area = project_main_form.cleaned_data['selected_area']
            details = project_main_form.cleaned_data['details']
            project_image = project_main_form.cleaned_data['project_image']
            budget = project_main_form.cleaned_data['budget']
            OrgProject.objects.create(start_date=start_date,end_date=end_date,project_name=project_name,selected_area=selected_area,details=details,organization=org,budget=budget,project_image=project_image)
            messages.add_message(request, messages.SUCCESS, "Project added successfully!!")
            return HttpResponseRedirect(reverse("orgApplication:org_profile_detail" ,kwargs={'pk': pk}))
        else:
            messages.add_message(request, messages.ERROR, "Please correct the errors!!")
    
    context = {'form': project_main_form,'organisation':org,"profile_bar":'org_project'}
    return render(request, template_name, context)



def org_project_view(request):
  
    total_org_project_list = OrgProject.objects.filter(status=True,end_date__gte=datetime.date.today()).count()
    all_running_projects = None
    if total_org_project_list > 0:
        all_running_projects = OrgProject.objects.filter(status=True,end_date__gte=datetime.date.today()).order_by('end_date')
    
    context = {
        'all_running_projects': all_running_projects,
        'nbar': 'home',
    }
    return render(request, 'index_main.html', context)
     
@login_required
def org_project_edit(request,pk):
    template_name = "orgApp/org_project_edit.html"
    org_project = get_object_or_404(OrgProject,pk=pk)
    org = get_object_or_404(Organisation,pk=org_project.organization.pk)
    
    project_main_form = forms.OrgProjectMainRegForm(request.POST or None, request.FILES or None,instance=org_project )   
    
    if request.method == 'POST':
        if project_main_form.is_valid():
            start_date = project_main_form.cleaned_data['start_date']
            end_date = project_main_form.cleaned_data['end_date']
            project_form = project_main_form.save(commit = False)
            project_form.start_date = start_date
            project_form.end_date = end_date
            project_form.organization = org
            project_form.save()
            
            messages.add_message(request, messages.SUCCESS, "Project added successfully!!")
            return HttpResponseRedirect(reverse("orgApplication:org_profile_detail" ,kwargs={'pk': org_project.organization.pk  }))
        else:
            messages.add_message(request, messages.ERROR, "Please correct the errors!!")
    
    context = {'form': project_main_form,'organisation':org,'organisation_project':org_project,"profile_bar":'org_project'}
    return render(request, template_name, context)


def org_project_delete_view(request, pk): 
  
    context ={} 
  
    # fetch the object related to passed id 
    org_project = get_object_or_404(OrgProject, pk = pk) 
    print(pk)
  
    if request.method =="POST": 
       
        org_project.delete() 
       
        return HttpResponseRedirect(reverse("orgApplication:org_profile_detail" ,kwargs={'pk': org_project.organization.pk  }))
  
    return render(request, "delete_view.html", context) 
      
    
    # print(total_org_project_list)
    # return HttpResponse('hello word')
    # divisions = City.objects.all().order_by('name')
    # districts = District.objects.all().order_by('name')
    # thanas = Thana.objects.all().order_by('name')
    # all_org_page_obj = None
    # context = {}
    # if total_org_list > 0:
    #     all_org = Organisation.objects.filter(status=True).order_by('name')
    #     paginator = Paginator(all_org, 10) # Show 25 contacts per page.
    #     page_number = request.GET.get('page')
    #     all_org_page_obj = paginator.get_page(page_number)
    # else:
    #     all_org = False
    
    # context = {
    #     'organisation_list': all_org_page_obj,
    #     'divisions': divisions,
    #     'districts': districts,
    #     'thanas': thanas,
    #     'nbar': 'home',
    # }
    # return render(request, 'index_main.html', context)


# some dump code
   
# division = request.GET.get('division',None)
# district = request.GET.get('district',None)
# thana = request.GET.get('thana',None)

# if division or district or thana:
#     print(division) 
#     print(district) 
#     print(thana) 
# # print(division)