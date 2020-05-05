from django.shortcuts import render
from .models import *
from django.http import HttpRequest, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, reverse
from orgApp import forms
from userApp.models import UserProfile
from .models import Organisation,City,District,Thana,OrgDetail,OrgProject
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .filters import OrganisationFilter
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect


# Create your views here.

def home(request):
    
    total_org_list = Organisation.objects.filter(status=True).count()
    divisions = City.objects.all().order_by('name')
    districts = District.objects.all().order_by('name')
    thanas = Thana.objects.all().order_by('name')
    context  ={}
    if total_org_list > 0:
        all_org = Organisation.objects.filter(status=True).order_by('name')
        paginator = Paginator(all_org, 10) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        all_org_page_obj = paginator.get_page(page_number)
    else:
        all_org = False
    
    context = {
        'organisation_list': all_org_page_obj,
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
        org= Organisation.objects.filter(owner=user,status=True).get(pk=pk)
        profile_have = True
        context = {
            'profile_have':profile_have,
            'organisation':org,
            'nbar':'org',
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
                return HttpResponseRedirect(reverse("orgApplication:org"))
        # context['errorMsg'] = 'Not new user'
        return render(request, 'orgApp/selfOrg.html', context)



@login_required
def edit_org(request,pk):
    logged_in_user = request.user
    org = get_object_or_404(Organisation, pk=pk)
    org_details = org.org_detail
    print(org)
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
            return HttpResponsePermanentRedirect(reverse("orgApplication:org"))
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

            
    

    # # user = UserProfile.objects.all()[:1].get()
    # queryset = Organisation.objects.filter()
    # # new = True if queryset.count() == 0 else None
    # new = True
    # context = {'queryset': queryset, 'errorMsg': None, 'new': new}

    # check for request type
   

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
    print(thana)
    return render(request, 'orgApp/thana_dropdown_list_options.html', {'thana': thana})


# some dump code
   
# division = request.GET.get('division',None)
# district = request.GET.get('district',None)
# thana = request.GET.get('thana',None)

# if division or district or thana:
#     print(division) 
#     print(district) 
#     print(thana) 
# # print(division)