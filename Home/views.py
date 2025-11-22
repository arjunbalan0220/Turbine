from django.shortcuts import render
from .models import Accessories

# Create your views here.

def index(request):
    return render(request,"index.html")
def about(request):
    return render(request,"about.html")
def contact(request):
    return render(request,"contact.html")



#Accessories
def accessories(request):
    
    return render(request,"accessories.html")
def acc_jacket(request):
    dict_acc={
        'acc': Accessories.objects.all()
    }
    return render(request,"acc_jacket.html",dict_acc)
def acc_gloves(request):
    dict_acc={
        'acc': Accessories.objects.all()
    }
    return render(request,"acc_gloves.html",dict_acc)
def acc_pant(request):
    dict_acc={
        'acc': Accessories.objects.all()
    }
    return render(request,"acc_pant.html",dict_acc)
def acc_helmet(request):
    dict_acc={
        'acc': Accessories.objects.all()
    }
    return render(request,"acc_helmet.html",dict_acc)
def acc_knee(request):
    dict_acc={
        'acc': Accessories.objects.all()
    }
    return render(request,"acc_knee.html",dict_acc)
def acc_lag(request):
    dict_acc={
        'acc': Accessories.objects.all()
    }
    return render(request,"acc_lag.html",dict_acc)
def acc_boot(request):
    dict_acc={
        'acc': Accessories.objects.all()
    }
    return render(request,"acc_boot.html",dict_acc)
def acc_lock(request):
    dict_acc={
        'acc': Accessories.objects.all()
    }
    return render(request,"acc_lock.html",dict_acc)
def accessoryview(request):
    if request.method == 'POST':
        acc_id=request.POST.get('id')
        acc = Accessories.objects.filter(id=acc_id)
        return render(request,"accessoryview.html", {'acc': acc})
    
    return render(request,"accessoryview.html", {'acc': []})


