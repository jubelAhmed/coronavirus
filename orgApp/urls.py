from django.urls import path


from . import views

app_name = "orgApplication"

urlpatterns = [
    path('', views.home, name='org'),
    path('<int:pk>',views.OrgDetailView,name='org-detail'),
    path('orgadmin/',views.orgnaziation_redirect,name='org-admin'),
    path("orgadmin/reg/", views.self_org, name='self_org'),
    path("orgadmin/orgprofile/", views.organizationProfile, name='org_profile'),
    path('orgadmin/orgprofile/<int:pk>',views.organizationProfile,name='org_profile_detail'),
    path('orgadmin/orgprofile/<int:pk>/edit/',views.edit_org, name='org_edit'),
    
    path("orgadmin/orgprofile/<int:pk>/orgprojectcreate/", views.org_project_create_view, name='org-project-create'),
    path("org-project/", views.org_project_view, name='org-project-list'),
    path("org-project/<int:pk>/edit", views.org_project_edit, name='org_project_view_edit'),
    path("org-project/<int:pk>", views.org_project_details, name='org_project_view_details'),
    path("org-project/public/<int:pk>", views.org_project_public_details, name='org_project_public_view_details'),
    path("org-project/<int:pk>/delete", views.org_project_delete_view, name='org_project_delete'),
   
    
    path("search/", views.search, name='search'),
    path('ajax/load-districts/', views.load_district, name='ajax_load_districts'),
    path('ajax/load-thanas/', views.load_thana, name='ajax_load_thana'),
    path('ajax/load-divisions/', views.load_thana, name='ajax_load_division'),
    path('ajax/get_org_profile_list/', views.get_org_profile_list, name='ajax_get_org_profile_list'),

    
]
