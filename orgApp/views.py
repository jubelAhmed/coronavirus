from django.shortcuts import render

# Create your views here.
def test(request):
    return render(request,'index_main.html',{'nbar': 'home'})