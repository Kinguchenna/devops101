
from django.shortcuts import render, HttpResponse
from .models import Logo, Blog, Service, ContactAddress


def default(request):
    logo = Logo.objects.all().order_by('-id').first() 

    try:
        recntPost = Blog.objects.all()[:2]  # Fetch the latest slider info
    except Blog.DoesNotExist:
        recntPost = None

    try:
        services = Service.objects.all()[:6]  # Fetch the latest slider info
    except Service.DoesNotExist:
        services = None

    try:
        contactaddress = ContactAddress.objects.all().order_by('-id').first() 
    except ContactAddress.DoesNotExist:
        contactaddress = None
    # image_slider = HomeImageSlider.objects.all()
    # about_one = AboutOne.objects.latest('id')


 
    return  {
        'logo' : logo,
        'recntPost' : recntPost,
        'services' : services,
        'contactaddress' : contactaddress,
        # 'image_slider' : image_slider,
        # 'about_one' : about_one,
        # 'cart_items' : cart_items,
        # 'cart' : cart,
        # 'item_count' : item_count,
    }


