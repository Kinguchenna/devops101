from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Service,Logo, SliderSection, AboutSection,Team,WhyChoose,BeforeAfter,Book,Testimonial,Message
from .models import Blog, BlogImage, Category, ContactAddress,ContactImage, Comments,PrivacyPolicy
from django.utils.text import slugify
from django.shortcuts import redirect, get_object_or_404
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.timezone import now
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator
from userauths.models import User, ResetCode, Profiles



import logging

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):

    try:
        slider = SliderSection.objects.latest('created_at')  # Fetch the latest slider info
    except SliderSection.DoesNotExist:
        slider = None

    try:
        about = AboutSection.objects.latest('created_at')  # Fetch the latest slider info
    except AboutSection.DoesNotExist:
        about = None

    try:
        services = Service.objects.all().order_by('-created_at')[:2]  
    except Service.DoesNotExist:
        services = None

    try:
        teams = Team.objects.all().order_by('-created_at')[:4]  
    except Team.DoesNotExist:
        teams = None

    try:
        us = WhyChoose.objects.all().order_by('-created_at')[:4]  
    except WhyChoose.DoesNotExist:
        us = None

    try:
        testimonial = Testimonial.objects.all().order_by('-created_at')[:4]  
    except Testimonial.DoesNotExist:
        testimonial = None

    try:
        blogs = Blog.objects.all().order_by('-created_at')[:3]  
    except Blog.DoesNotExist:
        blogs = None

    try:
        contactImage = ContactImage.objects.latest('created_at') 
    except ContactImage.DoesNotExist:
        contactImage = None

    try:
        users = User.objects.all() 
    except User.DoesNotExist:
        users = None

    # print('all users users', users)

    content = {
        'slider': slider,
        'about': about,
        'services': services,
        'teams': teams,
        'us': us,
        'testimonial': testimonial,
        'blogs': blogs,
        'contactImage': contactImage,
    }

    return render(request, 'frontpages/index.html', content)




def about(request):

    return render(request, 'frontpages/about.html')


def service(request):

    try:
        services = Service.objects.all().order_by('-created_at')  
    except Service.DoesNotExist:
        services = None

    blogs = Blog.objects.all()
    tags = Category.objects.all().order_by('-created_at')[:3]
    categories = Category.objects.all().order_by('-created_at')[:5]
    recentPosts = Blog.objects.all().order_by('-created_at')[:5]

    content = {
        'services': services,
        'blogs': blogs,
        'tags': tags,
        'categories': categories,
        'recentPosts': recentPosts,
    }

    return render(request, 'frontpages/service.html', content)


def blog(request):
    # Get all blogs, tags, categories, and recent posts
    blogs = Blog.objects.all()
    tags = Category.objects.all().order_by('-created_at')[:3]
    categories = Category.objects.all().order_by('-created_at')[:5]
    recentPosts = Blog.objects.all().order_by('-created_at')[:5]

    # Paginate the blog list, show 5 blogs per page
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Retrieve the comments for each blog post
    comments = Comments.objects.filter(post__in=blogs) 
    # Pre-calculate the number of comments for each blog
    comments_count =  comments.count() 

    content = {
        'blogs': blogs,
        'tags': tags,
        'comments': comments,
        'comments_count': comments_count,
        'page_obj': page_obj,
        'categories': categories,
        'recentPosts': recentPosts,
    }

    return render(request, 'frontpages/blog.html', content)
def blogDetails(request, slug):

    blog = Blog.objects.get(slug=slug)
    blogs = Blog.objects.all()
    tags = Category.objects.all().order_by('-created_at')[:3]
    categories = Category.objects.all().order_by('-created_at')[:5]
    recentPosts = Blog.objects.all().order_by('-created_at')[:5]
    comments = Comments.objects.filter(post=blog.id)
    comments_count = comments.count()

    content = {
        'blog': blog, 
        'comments': comments, 
        'comments_count': comments_count, 
        'blogs': blogs,
        'tags': tags,
        'categories': categories,
        'recentPosts': recentPosts,
    }

    return render(request, 'frontpages/blog-details.html', content)


from django.shortcuts import render, get_object_or_404
from .models import Blog, Category

def blogByCategory(request, slug):
    # Try to get the category using slug, or return 404 if not found
    category = get_object_or_404(Category, slug=slug)
    
    # Retrieve blogs belonging to the selected category
    blogbycategory = Blog.objects.filter(category=category)
    
    # Optionally, you can also retrieve other useful information
    blogs = Blog.objects.all()  # All blogs, you may want to limit this or add pagination
    tags = Category.objects.all().order_by('-created_at')[:3]  # Latest 3 categories
    categories = Category.objects.all().order_by('-created_at')[:5]  # Latest 5 categories
    recentPosts = Blog.objects.all().order_by('-created_at')[:5]  # Latest 5 blogs

        # Paginate the blog list
    paginator = Paginator(blogbycategory, 5)  # Show 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

        # Retrieve the comments for each blog post
    comments = Comments.objects.filter(post__in=blogs)  # Filter comments for all blogs at once
    comments_count = comments.count()

    # Pass everything to the template context
    content = {
        'blogbycategory': blogbycategory,
        'page_obj': page_obj,
        'blogs': blogs,
        'tags': tags,
        'comments': comments,
        'comments_count': comments_count,
        'categories': categories,
        'recentPosts': recentPosts,
    }

    return render(request, 'frontpages/blogbycategory.html', content)



def serviceDetails(request, slug):
    service = Service.objects.get(slug=slug)
    services = Service.objects.all()

    return render(request, 'frontpages/service-details.html', {'service': service, 'services': services})

def contact(request):

    return render(request, 'frontpages/contact.html')


def privacy(request):

    try:
        privacy = PrivacyPolicy.objects.latest('created_at')
    except PrivacyPolicy.DoesNotExist:
        privacy = None

    content = {
        'privacy': privacy
    }

    return render(request, 'frontpages/privacy.html', content)



def dashboard(request):

    return render(request, 'backpages/index.html')





def addSlider(request):

    return render(request, 'backpages/addslider.html')

def delete_slide(request, id):
    if id:  # Ensure it's a POST request for safety
        slide = get_object_or_404(SliderSection, id=id)
        slide.delete()

        # Get all slides after deletion
        slides = SliderSection.objects.all()
        content = {
            'slides': slides
        }

        # Add a success message to inform the user
        messages.success(request, 'Slide has been successfully deleted.')

        # Render the sliders page with the updated content
        return render(request, 'backpages/sliders.html', content)
    
    # If not a POST request, redirect back to the sliders page
    slides = SliderSection.objects.all()
    content = {
        'slides': slides
    }
    messages.error(request, 'Invalid request method.')
    return render(request, 'backpages/sliders.html', content)



def generate_unique_slug(name):
    slug = slugify(name)
    unique_slug = slug
    counter = 1
    while Service.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{counter}'
        counter += 1
    return unique_slug

def generate_unique_cslug(name):
    slug = slugify(name)
    unique_slug = slug
    counter = 1
    while Category.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{counter}'
        counter += 1
    return unique_slug


def generate_unique_bslug(name):
    slug = slugify(name)
    unique_slug = slug
    counter = 1
    while Blog.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{counter}'
        counter += 1
    return unique_slug



def addServices(request):
    categories = Category.objects.all()
    content = {
        'categories':categories
    }

    return render(request, 'backpages/add_service.html', content)

@csrf_exempt
def add_service(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category = request.POST.get('category')
            price = request.POST.get('price')
            compare_price = request.POST.get('compare_price')
            description = request.POST.get('description')

            if not name or not category or not price or not description:
                return JsonResponse({'message': 'All fields are required.'}, status=400)
            
                        # Validate and retrieve category
            category = get_object_or_404(Category, id=category)
            
            slug = generate_unique_slug(name)

            IMAGE_SIZE = (330, 317)
            image = (
                resize_image(request.FILES.get('image'), IMAGE_SIZE) 
                if 'image' in request.FILES else None
            )

            # Save to database
            service = Service.objects.create(
                name=name,
                slug=slug,
                category=category,
                price=float(price),
                compare_price=float(compare_price) if compare_price else None,
                description=description,
                image=image,
            )

            # Handle images if provided
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for img in images:
                    service.images.create(file=img)  # Assuming a related Image model

            return JsonResponse({'message': 'Service added successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)



def addTeam(request):

    return render(request, 'backpages/add_team.html')

@csrf_exempt
def add_team(request):
    if request.method == 'POST':
        try:
            
            name = request.POST.get('name')
            job = request.POST.get('job')
            phone = request.POST.get('phone')
            link1 = request.POST.get('link1')
            link2 = request.POST.get('link2')
            link3 = request.POST.get('link3')
            link4 = request.POST.get('link4')

            if not name or not job or not phone:
                return JsonResponse({'message': 'All fields are required.'}, status=400)
            
            slug = generate_unique_slug(name)

            IMAGE_SIZE = (182, 182)
            image = (
                resize_image(request.FILES.get('image'), IMAGE_SIZE) 
                if 'image' in request.FILES else None
            )

            # Save to database
            team = Team.objects.create(
                name=name,
                slug=slug,
                job=job,
                phone=phone,
                link1=link1,
                link2=link2,
                link3=link3,
                link4=link4,
                image=image,
            )

            team.save()

            return JsonResponse({'message': 'Team added successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

def listTeam(request):

    teams = Team.objects.all()

    content = {
        'teams': teams
    }

    return render(request, 'backpages/team.html', content)


def delete_team(request, id):
    if id:  # Ensure it's a POST request for safety
        team = get_object_or_404(Team, id=id)
        team.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    return render(request, 'backpages/team.html')
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def edit_team(request, id):
    if id:  # Ensure it's a POST request for safety
        team = get_object_or_404(Team, id=id)

        content = {
            'team':team
        }
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    return render(request, 'backpages/editteam.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def update_team(request):
    if request.method == 'POST':
        try:
            # Retrieve the service data from POST
            name = request.POST.get('name')
            job = request.POST.get('job')
            phone = request.POST.get('phone')
            link1 = request.POST.get('link1')
            link2 = request.POST.get('link2')
            link3 = request.POST.get('link3')
            link4 = request.POST.get('link4')
            teamId = request.POST.get('teamId')
            # Ensure all fields are provided
            if not name or not teamId or not job or not phone:
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Fetch the existing service using the serviceId
            team = Team.objects.get(id=teamId)  # Assuming 'id' is the primary key

            # Generate a unique slug (optional, if the name changes)
            slug = generate_unique_slug(name)

            # Update the service object with the new values
            team.name = name
            team.job = job
            team.phone = phone
            team.link1 = link1
            team.link2 = link2
            team.link3 = link3
            team.link4 = link4

            # Save the updated service

            IMAGE_SIZE = (182, 182)
            if 'image' in request.FILES:
                team.image = resize_image(request.FILES.get('image'), IMAGE_SIZE)


            team.save()

            return JsonResponse({'message': 'Team updated successfully!'}, status=200)

        except Service.DoesNotExist:
            return JsonResponse({'message': 'Team not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)

# WHY CHOOSE US

def addUs(request):

    return render(request, 'backpages/add_us.html')

@csrf_exempt
def add_us(request):
    if request.method == 'POST':
        try:
            header = request.POST.get('header')
            paragraph = request.POST.get('paragraph')
            headerone = request.POST.get('headerone')
            headertwo = request.POST.get('headertwo')
            headerthree = request.POST.get('headerthree')
            paragraphone = request.POST.get('paragraphone')
            paragraphtwo = request.POST.get('paragraphtwo')
            paragraphthree = request.POST.get('paragraphthree')


            if not header or not paragraph or not headerone:
                return JsonResponse({'message': 'All fields are required.'}, status=400)
            

            IMAGE_SIZE = (657, 625)
            imageone = (
                resize_image(request.FILES.get('imageone'), IMAGE_SIZE) 
                if 'imageone' in request.FILES else None
            )

            IMAGE_TWO_SIZE = (331, 321)
            imagetwo = (
                resize_image(request.FILES.get('imagetwo'), IMAGE_TWO_SIZE) 
                if 'imagetwo' in request.FILES else None
            )

            # Save to database
            us = WhyChoose.objects.create(
                header=header,
                paragraph=paragraph,
                headerone=headerone,
                headertwo=headertwo,
                headerthree=headerthree,
                paragraphone=paragraphone,
                paragraphtwo=paragraphtwo,
                paragraphthree=paragraphthree,
                imageone=imageone,
                imagetwo=imagetwo,
            )

            us.save()

            return JsonResponse({'message': 'added successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

def listUs(request):

    us = WhyChoose.objects.all()

    content = {
        'us': us
    }

    return render(request, 'backpages/us.html', content)


def delete_us(request, id):
    if id:  # Ensure it's a POST request for safety
        us = get_object_or_404(WhyChoose, id=id)
        us.delete()

    us = WhyChoose.objects.all()

    content = {
        'us': us
    }
    return render(request, 'backpages/us.html', content)

def edit_us(request, id):
    if id:  # Ensure it's a POST request for safety
        us = get_object_or_404(WhyChoose, id=id)

        content = {
            'us':us
        }
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    return render(request, 'backpages/editus.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def update_us(request):
    if request.method == 'POST':
        try:
            # Retrieve the service data from POST
            header = request.POST.get('header')
            usId = request.POST.get('usId')
            paragraph = request.POST.get('paragraph')
            headerone = request.POST.get('headerone')
            headertwo = request.POST.get('headertwo')
            headerthree = request.POST.get('headerthree')
            paragraphone = request.POST.get('paragraphone')
            paragraphtwo = request.POST.get('paragraphtwo')
            paragraphthree = request.POST.get('paragraphthree')
            # Ensure all fields are provided
            if not header or not usId or not paragraph:
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Fetch the existing service using the serviceId
            us = WhyChoose.objects.get(id=usId)  # Assuming 'id' is the primary key 
            # Update the service object with the new values
            us.header = header
            us.paragraph = paragraph
            us.headerone = headerone
            us.headertwo = headertwo
            us.headerthree = headerthree
            us.paragraphone = paragraphone
            us.paragraphtwo = paragraphtwo
            us.paragraphthree = paragraphthree

            # Save the updated service

            IMAGE_SIZE = (657, 625)
            if 'imageone' in request.FILES:
                us.imageone = resize_image(request.FILES.get('imageone'), IMAGE_SIZE)

            IMAGE_TWO_SIZE = (331, 321)
            if 'imagetwo' in request.FILES:
                us.imagetwo = resize_image(request.FILES.get('imagetwo'), IMAGE_TWO_SIZE)

            us.save()

            return JsonResponse({'message': 'updated successfully!'}, status=200)

        except WhyChoose.DoesNotExist:
            return JsonResponse({'message': 'not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)



# TESTIMONIALS

def addtestimonials(request):

    return render(request, 'backpages/addtestimonials.html')

@csrf_exempt
def save_testimonials(request):
    if request.method == 'POST':
        try:            
            name = request.POST.get('name')
            title = request.POST.get('title')
            paragraph = request.POST.get('paragraph')

            if not name or not paragraph or not title:
                return JsonResponse({'message': 'All fields are required.'}, status=400)            

            IMAGE_SIZE = (90, 90)
            image = (
                resize_image(request.FILES.get('image'), IMAGE_SIZE) 
                if 'image' in request.FILES else None
            )

            # Save to database
            testimonial = Testimonial.objects.create(
                name=name,
                title=title,
                paragraph=paragraph,
                image=image,
            )

            testimonial.save()

            return JsonResponse({'message': 'added successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

def listTestimonials(request):

    testimonials = Testimonial.objects.all()

    content = {
        'testimonials': testimonials
    }

    return render(request, 'backpages/testimonials.html', content)


def delete_testimonials(request, id):
    if id:  # Ensure it's a POST request for safety
        testimonial = get_object_or_404(Testimonial, id=id)
        testimonial.delete()

    testimonials = Testimonial.objects.all()

    content = {
        'testimonials': testimonials
    }
    return render(request, 'backpages/testimonials.html', content)

def edit_testimonials(request, id):
    if id:  # Ensure it's a POST request for safety
        testimonial = get_object_or_404(Testimonial, id=id)

        content = {
            'testimonial':testimonial
        }
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    return render(request, 'backpages/edittestimonial.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def update_testimonial(request):
    if request.method == 'POST':
        try:
            # Retrieve the service data from POST
            name = request.POST.get('name')
            title = request.POST.get('title')
            paragraph = request.POST.get('paragraph')
            testimonialId = request.POST.get('testimonialId')
            # Ensure all fields are provided
            if not name or not paragraph or not title:
                return JsonResponse({'message': 'All fields are required.'}, status=400)            

            IMAGE_SIZE = (90, 90)
            image = (
                resize_image(request.FILES.get('image'), IMAGE_SIZE) 
                if 'image' in request.FILES else None
            )

            # Fetch the existing service using the serviceId
            testimonial = Testimonial.objects.get(id=testimonialId)  # Assuming 'id' is the primary key 
            # Update the service object with the new values
            testimonial.name = name
            testimonial.paragraph = paragraph
            testimonial.title = title
            # Save the updated service
            testimonial.image = image

            testimonial.save()

            return JsonResponse({'message': 'updated successfully!'}, status=200)

        except Testimonial.DoesNotExist:
            return JsonResponse({'message': 'not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


# Helper function for resizing images
# def resize_image(file, target_size):
#     image = Image.open(file)
#     # Convert the image to 'RGB' if it's not already in that mode
#     if image.mode in ('RGBA', 'P'):
#         image = image.convert('RGB')
#     image = image.resize(target_size, Image.Resampling.LANCZOS)
#     img_io = BytesIO()
#     image.save(img_io, format='JPEG')
#     img_io.seek(0)
#     return InMemoryUploadedFile(
#         img_io, None, file.name.split('.')[0] + '.jpg', 'image/jpeg', img_io.tell(), None
#     )


def listSlider(request):

    slides = SliderSection.objects.all()

    content = {
        'slides': slides
    }

    return render(request, 'backpages/sliders.html', content)



def edit_slide(request, id):
    if id:  # Ensure it's a POST request for safety
        slide = get_object_or_404(SliderSection, id=id)

        content = {
            'slide':slide
        }
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    return render(request, 'backpages/editslide.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# def resize_image(file, size=(828, 256)):target_size
def resize_image(file, target_size):
    image = Image.open(file)

    # Check if the image has transparency (RGBA, P mode)
    if image.mode in ('RGBA', 'P'):
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        # Preserve transparency, save as PNG (or another format that supports transparency)
        img_io = BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)
        return InMemoryUploadedFile(
            img_io, None, file.name.split('.')[0] + '.png', 'image/png', img_io.tell(), None
        )
    else:
        # Convert to RGB and save as JPEG for non-transparent images
        image = image.convert('RGB')
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        img_io = BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        return InMemoryUploadedFile(
            img_io, None, file.name.split('.')[0] + '.jpg', 'image/jpeg', img_io.tell(), None
        )

@csrf_exempt
def add_slider(request):
    if request.method == 'POST':
        try:
            # Get form data
            sub_title = request.POST.get('subTitle')
            title = request.POST.get('title')
            paragraph = request.POST.get('paragraph')
            btntext = request.POST.get('btnText')
            contact_number = request.POST.get('contactNumber')
            contact_link = request.POST.get('contactLink')

            # Validate required fields
            if not all([sub_title, title, paragraph, btntext]):
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Helper function for resizing images

            # Define target sizes for images
            BACKGROUND_IMAGE_SIZE = (1920, 906)  # Example size for background image
            SLIDER_IMAGE_SIZE = (1394, 1446)      # Example size for slider image

            # Process images if provided
            background_image = (
                resize_image(request.FILES.get('background_image'), BACKGROUND_IMAGE_SIZE) 
                if 'background_image' in request.FILES else None
            )
            slider_image = (
                resize_image(request.FILES.get('slider_image'), SLIDER_IMAGE_SIZE) 
                if 'slider_image' in request.FILES else None
            )

            # Create SliderSection entry
            slide = SliderSection.objects.create(
                sub_title=sub_title,
                title=title,
                paragraph=paragraph,
                btntext=btntext,
                contact_number=contact_number,
                contact_link=contact_link,
                background_image=background_image,
                slider_image=slider_image,
                created_at=now()
            )

            return JsonResponse({'message': 'Slider added successfully!', 'id': slide.id}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    # return JsonResponse({'message': 'Invalid request method.'}, status=405)
    return render(request, 'backpages/addslider.html')


@csrf_exempt
def editslide(request):
    if request.method == 'POST':
        try:
            # Get form data
            logger.error('updating slide')
            slide_id = request.POST.get('slideId')
            sub_title = request.POST.get('subTitle')
            title = request.POST.get('title')
            paragraph = request.POST.get('paragraph')
            btn_text = request.POST.get('btnText')
            contact_number = request.POST.get('contactNumber', '')
            contact_link = request.POST.get('contactLink', '')

            # Validate required fields
            if not all([sub_title, title, paragraph, btn_text, slide_id]):
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            slide = SliderSection.objects.get(id=slide_id)

            # Define target sizes for images
            BACKGROUND_IMAGE_SIZE = (1920, 906)
            SLIDER_IMAGE_SIZE = (1394, 1446)

            background_image = (
                resize_image(request.FILES.get('background_image'), BACKGROUND_IMAGE_SIZE)
                if 'background_image' in request.FILES else slide.background_image
            )

            slider_image = (
                resize_image(request.FILES.get('slider_image'), SLIDER_IMAGE_SIZE)
                if 'slider_image' in request.FILES else slide.slider_image
            )

            # Update slide information
            slide.sub_title = sub_title
            slide.title = title
            slide.paragraph = paragraph
            slide.btntext = btn_text
            slide.contact_number = contact_number
            slide.contact_link = contact_link
            slide.background_image = background_image
            slide.slider_image = slider_image
            slide.save()

            return JsonResponse({'message': 'Slider updated successfully!', 'title': slide.title}, status=200)

        except SliderSection.DoesNotExist:
            return JsonResponse({'message': 'Slider not found.'}, status=404)
        except Exception as e:
            logger.error(f'Error updating slide: {e}')
            return JsonResponse({'message': 'An unexpected error occurred.'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


def listAbout(request):
    abouts = AboutSection.objects.all()

    content = {
        'abouts': abouts
    }
    return render(request, 'backpages/abouts.html', content)


def edit_about(request, id):
    if id:  # Ensure it's a POST request for safety
        about = get_object_or_404(AboutSection, id=id)

        content = {
            'about':about
        }
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    return render(request, 'backpages/editabout.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def add_about(request):
    if request.method == 'POST':
        try:
            # Get form data
            sub_title = request.POST.get('subTitle')
            title = request.POST.get('title')
            paragraph = request.POST.get('paragraph')
            btntext = request.POST.get('btnText')
            list_one = request.POST.get('list_one')
            list_two = request.POST.get('list_two')
            list_three = request.POST.get('list_three')
            name = request.POST.get('name')
            job = request.POST.get('job')

            # Validate required fields
            if not all([sub_title, title, paragraph, btntext]):
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Helper function for resizing images

            # Define target sizes for images
            BACKGROUND_IMAGE_SIZE = (573, 573)  # Example size for background image
            SLIDER_IMAGE_SIZE = (161, 102)      # Example size for slider image
            PROFILEIMAGE_SIZE = (48, 48)      # Example size for slider image

            # Process images if provided
            background_image = (
                resize_image(request.FILES.get('background_image'), BACKGROUND_IMAGE_SIZE) 
                if 'background_image' in request.FILES else None
            )
            slider_image = (
                resize_image(request.FILES.get('slider_image'), SLIDER_IMAGE_SIZE) 
                if 'slider_image' in request.FILES else None
            )

            profile = (
                resize_image(request.FILES.get('profile_image'), PROFILEIMAGE_SIZE) 
                if 'profile_image' in request.FILES else None
            )

            # Create SliderSection entry
            about = AboutSection.objects.create(
                sub_title=sub_title,
                title=title,
                paragraph=paragraph,
                btntext=btntext,
                list_one = list_one,
                list_two = list_two,
                list_three = list_three,
                name = name,
                job = job,
                background_image=background_image,
                slider_image=slider_image,
                profile=profile,
                created_at=now()
            )

            return JsonResponse({'message': 'About added successfully!', 'title': about.title}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    # return JsonResponse({'message': 'Invalid request method.'}, status=405)
    return render(request, 'backpages/addabout.html')


@csrf_exempt
def editabout(request):
    if request.method == 'POST':
        try:
            # Get form data
            sub_title = request.POST.get('subTitle')
            title = request.POST.get('title')
            paragraph = request.POST.get('paragraph')
            btntext = request.POST.get('btnText')
            list_one = request.POST.get('list_one')
            list_two = request.POST.get('list_two')
            list_three = request.POST.get('list_three')
            name = request.POST.get('name')
            job = request.POST.get('job')
            aboutId = request.POST.get('aboutId')

            # Validate required fields
            if not all([sub_title, title, paragraph, btntext, aboutId]):
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Process images if provided
            about = AboutSection.objects.get(id=aboutId)

           # Define target sizes for images
            BACKGROUND_IMAGE_SIZE = (573, 573)  # Example size for background image
            SLIDER_IMAGE_SIZE = (161, 102)      # Example size for slider image
            PROFILEIMAGE_SIZE = (48, 48)      # Example size for slider image

            # # Process images if provided
            # background_image = (
            #     resize_image(request.FILES.get('background_image'), BACKGROUND_IMAGE_SIZE) 
            #     if 'background_image' in request.FILES else None
            # )
            # slider_image = (
            #     resize_image(request.FILES.get('slider_image'), SLIDER_IMAGE_SIZE) 
            #     if 'slider_image' in request.FILES else None
            # )

            # profile = (
            #     resize_image(request.FILES.get('profile_image'), PROFILEIMAGE_SIZE) 
            #     if 'profile_image' in request.FILES else None
            # )

                   # Process images if provided, otherwise retain the existing images
            if 'background_image' in request.FILES:
                about.background_image = resize_image(request.FILES.get('background_image'), BACKGROUND_IMAGE_SIZE)

            if 'slider_image' in request.FILES:
                about.slider_image = resize_image(request.FILES.get('slider_image'), SLIDER_IMAGE_SIZE)

            if 'profile_image' in request.FILES:
                about.profile = resize_image(request.FILES.get('profile_image'), PROFILEIMAGE_SIZE)

            # Update slide information
            about.sub_title = sub_title
            about.title = title
            about.paragraph = paragraph
            about.btntext = btntext
            about.list_one = list_one
            about.list_two = list_two
            about.list_three = list_three
            about.name = name
            about.job = job
            # about.background_image = background_image
            # about.slider_image = slider_image
            # about.profile = profile
            about.created_at = now()

            # Save the changes
            about.save()

            return JsonResponse({'message': 'Slider updated successfully!', 'title': about.title}, status=200)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)



def delete_abouts(request, id):
    if id:  # Ensure it's a POST request for safety
        about = get_object_or_404(AboutSection, id=id)
        about.delete()

        # Get all slides after deletion
        abouts = AboutSection.objects.all()
        content = {
            'abouts': abouts
        }

        # Add a success message to inform the user
        messages.success(request, 'Slide has been successfully deleted.')

        # Render the sliders page with the updated content
        return render(request, 'backpages/abouts.html', content)
    
    # If not a POST request, redirect back to the sliders page
    abouts = AboutSection.objects.all()
    content = {
        'abouts': abouts
    }
    messages.error(request, 'Invalid request method.')
    return render(request, 'backpages/abouts.html', content)


@csrf_exempt
def update_service(request):
    if request.method == 'POST':
        try:
            # Retrieve the service data from POST
            name = request.POST.get('name')
            serviceId = request.POST.get('serviceId')
            category = request.POST.get('category')
            price = request.POST.get('price')
            compare_price = request.POST.get('compare_price')
            description = request.POST.get('description')

            # Ensure all fields are provided
            if not name or not serviceId or not category or not price or not description:
                return JsonResponse({'message': 'All fields are required.'}, status=400)
            
            category = get_object_or_404(Category, id=category)

            # Fetch the existing service using the serviceId
            service = Service.objects.get(id=serviceId)  # Assuming 'id' is the primary key

            # Generate a unique slug (optional, if the name changes)
            slug = generate_unique_slug(name)

            # Update the service object with the new values
            service.name = name
            service.slug = slug
            service.category = category
            service.price = float(price)
            service.compare_price = float(compare_price) if compare_price else None
            service.description = description

            # Save the updated service

            IMAGE_SIZE = (330, 317)
            if 'image' in request.FILES:
                service.image = resize_image(request.FILES.get('image'), IMAGE_SIZE)


            # if 'image' in request.FILES:
            #     image_file = request.FILES.get('image')  # Access the image file
                
            #     # Open the image using PIL
            #     image = Image.open(image_file)
                
            #     # Resize the image (Adjust the size as needed)
            #     image = image.resize((870, 386), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS instead of Image.ANTIALIAS
                
            #     # Save the resized image into a BytesIO object
            #     img_io = BytesIO()
            #     image.save(img_io, format='JPEG')  # Save as JPEG (or another format as needed)
            #     img_io.seek(0)

            #     # Create an InMemoryUploadedFile object for the resized image
            #     img_name = image_file.name.split('.')[0]  # Use original image name (without extension)
            #     image_file_resized = InMemoryUploadedFile(
            #         img_io, None, img_name + '.jpg', 'image/jpeg', img_io.tell(), None
            #     )

                # Assign the resized image to the service's image field (assuming you have an Image field for this)
            
            service.save()

            # Handle images if provided (Optional)
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for img in images:
                    # Open the image using PIL
                    image = Image.open(img)

                    # Resize the image (You can adjust the size as needed, here it resizes to 800x800)
                    image = image.resize((870, 386), Image.Resampling.LANCZOS)

                    # Save the image into a BytesIO object
                    img_io = BytesIO()
                    image.save(img_io, format='JPEG')  # Save as JPEG (or another format as needed)
                    img_io.seek(0)

                    # Create an InMemoryUploadedFile object
                    img_name = img.name.split('.')[0]  # Just using the original name as the file name
                    image_file = InMemoryUploadedFile(img_io, None, img_name, 'image/jpeg', img_io.tell(), None)

                    # Assuming a related Image model
                    service.images.create(file=image_file)

            return JsonResponse({'message': 'Service updated successfully!'}, status=200)

        except Service.DoesNotExist:
            return JsonResponse({'message': 'Service not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


def getLogo(request):

    return render(request, 'backpages/addlogo.html')


def listLogos(request):

    logos = Logo.objects.all()

    content = {
        'logos': logos
    }

    return render(request, 'backpages/logos.html', content)




@csrf_exempt
def add_logo(request):
    if request.method == 'POST':
        try:
            if 'image' in request.FILES:

                LOGO_IMAGE_SIZE = (828, 256)      # Example size for slider image

                # Process images if provided
                image_file_resized = (
                    resize_image(request.FILES.get('image'), LOGO_IMAGE_SIZE) 
                    if 'image' in request.FILES else None
                )

                # Save the resized image to the Logo model
                logo = Logo.objects.create(logo=image_file_resized, created_at=now())

            return JsonResponse({'message': 'Logo updated successfully!'}, status=200)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)



def listServices(request):

    services = Service.objects.all()

    content = {
        'services': services
    }

    return render(request, 'backpages/service.html', content)


def delete_service(request, id):
    if id:  # Ensure it's a POST request for safety
        service = get_object_or_404(Service, id=id)
        service.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    services = Service.objects.all()

    content = {
        'services': services
    }

    return render(request, 'backpages/service.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def delete_logo(request, id):
    if id:  # Ensure it's a POST request for safety
        logo = get_object_or_404(Logo, id=id)
        logo.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    logos = Logo.objects.all()

    content = {
        'logos': logos
    }
    return render(request, 'backpages/logos.html',content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def edit_service(request, id):
    if id:  # Ensure it's a POST request for safety
        service = get_object_or_404(Service, id=id)
        categories = Category.objects.all()

        content = {
            'service':service,
            'categories':categories,
        }
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    
    

    return render(request, 'backpages/editservice.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})











# Comments for Blog 

@csrf_exempt
def sendComment(request):
    if request.method == 'POST':
        try:
            # Get form data
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            website = request.POST.get('website')
            comment = request.POST.get('comment')
            post_id = request.POST.get('post_id')  # Ensure 'post_id' is correct

            # Validate required fields
            if not post_id:
                return JsonResponse({'message': 'Post ID is required.'}, status=400)

            post = get_object_or_404(Blog, id=post_id)

            # Validate required fields
            if not all([fname, lname, comment, email]):
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Create comment entry
            comment = Comments.objects.create(
                fname=fname,
                lname=lname,
                email=email,
                website=website,
                comment=comment,
                post=post,
            )

            comment.save()

            return JsonResponse({'message': 'Comment sent successfully!', 'title': comment.fname}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)



def listComments(request):

    comments = Comments.objects.all()

    content = {
        'comments': comments
    }

    return render(request, 'backpages/comments.html', content)


def delete_comment(request, id):
    if id:  # Ensure it's a POST request for safety
        comment = get_object_or_404(Comments, id=id)
        comment.delete()

        # Get all slides after deletion
        comments = Comments.objects.all()
        content = {
            'comments': comments
        }

        # Add a success message to inform the user
        messages.success(request, 'Slide has been successfully deleted.')

        # Render the sliders page with the updated content
        return render(request, 'backpages/comments.html', content)
    
    # If not a POST request, redirect back to the sliders page
    comments = Comments.objects.all()
    content = {
        'comments': comments
    }
    messages.error(request, 'Invalid request method.')
    return render(request, 'backpages/comments.html', content)



@csrf_exempt
def sendToMail(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            service = request.POST.get('service')
            message = request.POST.get('message') 

            # Validate required fields
            if not all([name, email, service, message]):
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Helper function for resizing images

            # Create SliderSection entry
            message_contact = Message.objects.create(
                name=name,
                email=email,
                service=service,
                message=message, 
            )
            message_contact.save()

            send_veri_email(name, email, service, message)

            return JsonResponse({'message': 'Message sent successfully!', 'title': message_contact.name}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    # return JsonResponse({'message': 'Invalid request method.'}, status=405)
    return render(request, 'backpages/addabout.html')






def send_mail2(request):
    try:
        if request.method == 'POST':            
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            service = request.POST.get('service')
            message = request.POST.get('message') 

                        # Save the data to the Logo model
            message_contact = Message(
                name=name,
                email=email,
                service=service,
                message=message, 
            )

            message_contact.save()

            send_veri_email(name, email, service, message)

            messages.success(request, 'created successfully!')
            # return render(request, "ainhub/contact.html")
            return JsonResponse({"status": 'Message Sent Successfully!'})


    except Exception as e:
        
        context = {
           'error': str(e)
        }
        # return render(request, "ainhub/error.html", context)
        messages.error(request, f'Error: {str(e)}')
        # return render(request, "ainhub/error.html", context)
        return JsonResponse({"status": f'Error: {str(e)}'})
    
 

def send_veri_email(name, email, service, message):
    context = {
        'name': name,
        'email': email,
        'service': service,
        'message': message,
        }
    html_content = render_to_string('email/sendverification.html', context )
    text_content = strip_tags(html_content)

    from_email = 'info@ainhub.com'  # Replace with your email address
    to_emails = [email, 'info@ainhub.com']  # Replace with the user's email addresses
    cc_emails = ['cc_email1@example.com', 'cc_email2@example.com']  # Replace with the CC email addresses
    bcc_emails = ['bcc_email@example.com']  # Replace with the BCC email addresses
        # Send the email
    msg = EmailMultiAlternatives(
        subject='Welcome',
        body=text_content,
        from_email=from_email,
        to=to_emails,
        # cc=cc_emails,
        # bcc=bcc_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# Blog 

def addBlog(request):

    categories = Category.objects.all()
    content = {
        'categories':categories
    }

    return render(request, 'backpages/add_blog.html', content)

@csrf_exempt
def add_Blog(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            slug = request.POST.get('slug')
            category_name = request.POST.get('category')
            description = request.POST.get('description')

            # Validate required fields
            if not name or not category_name or not description:
                return JsonResponse({'message': 'Name, category, and description are required.'}, status=400)

            # Validate and retrieve category
            category = get_object_or_404(Category, id=category_name)

            # Generate slug if not provided
            slug = slug or generate_unique_bslug(name)

            # Handle image resizing
            image = (
                resize_image(request.FILES['image'], (869, 386)) 
                if 'image' in request.FILES else None
            )

            # Create the blog
            blog = Blog.objects.create(
                name=name,
                slug=slug,
                category=category.name,
                description=description,
                image=image,
            )

            # Handle additional blog images
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for img in images:
                    blog.images.create(file=img)

            return JsonResponse({'message': 'Blog added successfully!'}, status=201)

        except Category.DoesNotExist:
            return JsonResponse({'message': 'Category not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


@csrf_exempt
def add_blog(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            slug = request.POST.get('slug')
            category_id = request.POST.get('category')  # Get the category ID
            description = request.POST.get('description')

            # Validate required fields
            if not name or not category_id or not description:
                return JsonResponse({'message': 'Name, category, and description are required.'}, status=400)

            # Validate and retrieve category
            category = get_object_or_404(Category, id=category_id)

            # Generate slug if not provided
            slug = slug or generate_unique_bslug(name)

            # Handle image resizing
            image = (
                resize_image(request.FILES['image'], (856, 628)) 
                if 'image' in request.FILES else None
            )

            # Create the blog
            blog = Blog.objects.create(
                name=name,
                slug=slug,
                category=category,  # Assign the Category instance
                description=description,
                image=image,
            )

            # Handle additional blog images
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for img in images:
                    blog.images.create(file=img)

            return JsonResponse({'message': 'Blog added successfully!'}, status=201)

        except Category.DoesNotExist:
            return JsonResponse({'message': 'Category not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


def listBlog(request):

    blogs = Blog.objects.all()

    content = {
        'blogs': blogs
    }

    return render(request, 'backpages/blog.html', content)


def delete_Blog(request, id):
    if id:  # Ensure it's a POST request for safety
        blog = get_object_or_404(Blog, id=id)
        blog.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})


    blogs = Blog.objects.all()

    content = {
        'blogs': blogs
    }
    return render(request, 'backpages/blog.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def edit_Blog(request, id):
    if id:  # Ensure it's a POST request for safety
        blog = get_object_or_404(Blog, id=id)
        categories = Category.objects.all()

        content = {
            'blog':blog,
            'categories':categories
        }
    return render(request, 'backpages/editblog.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def update_Blog(request):
    if request.method == 'POST':
        try:
            # Retrieve the service data from POST
            blogId = request.POST.get('blogId')
            name = request.POST.get('name')
            slug = request.POST.get('slug')  # This is unnecessary unless you want to update the slug manually
            category_id = request.POST.get('category')
            description = request.POST.get('description')

            # Ensure all fields are provided
            if not name or not blogId or not category_id or not description:
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Fetch the existing service using the serviceId
            blog = Blog.objects.get(id=blogId)  # Assuming 'id' is the primary key

            category = get_object_or_404(Category, id=category_id)

            # Generate a unique slug (optional, if the name changes)
            slug = generate_unique_slug(name)

            # Update the service object with the new values
            blog.name = name
            blog.slug = slug
            blog.category = category  
            blog.description = description

            # Save the updated service
            IMAGE_SIZE = (856, 628)
            if 'image' in request.FILES:
                blog.image = resize_image(request.FILES.get('image'), IMAGE_SIZE)

            blog.save()

            # Handle additional images if provided (Optional)
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for img in images:
                    # Open the image using PIL
                    image = Image.open(img)

                    # Resize the image (You can adjust the size as needed, here it resizes to 424x249)
                    image = image.resize((424, 249), Image.Resampling.LANCZOS)

                    # Save the image into a BytesIO object
                    img_io = BytesIO()
                    image.save(img_io, format='JPEG')  # Save as JPEG (or another format as needed)
                    img_io.seek(0)

                    # Create an InMemoryUploadedFile object
                    img_name = img.name.split('.')[0]  # Just using the original name as the file name
                    image_file = InMemoryUploadedFile(img_io, None, img_name, 'image/jpeg', img_io.tell(), None)

                    # Assuming a related Image model (e.g., BlogImage) exists
                    blog.images.create(file=image_file)

            return JsonResponse({'message': 'Blog updated successfully!'}, status=200)

        except Blog.DoesNotExist:
            return JsonResponse({'message': 'Blog not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


# Category 

def addCategory(request):

    return render(request, 'backpages/add_category.html')

def add_about2(request):
    pass

def add_category(request):
    pass


@csrf_exempt
def add_about3(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name') 
  
            # Validate required fields
            if not name:
                return JsonResponse({'message': 'All fields not are required.'}, status=400)

 
            slug = generate_unique_cslug(name)
            # Create SliderSection entry
            category = Category.objects.create(
                name=name,
                slug=slug,  
            )

            return JsonResponse({'message': 'Category added successfully!', 'title': category.slug}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)




def listCategory(request):

    categories = Category.objects.all()

    content = {
        'categories': categories
    }

    return render(request, 'backpages/category.html', content)


def delete_Category(request, id):
    if id:  # Ensure it's a POST request for safety
        category = get_object_or_404(Category, id=id)
        category.delete()

    categories = Category.objects.all()

    content = {
        'categories': categories
    }
    return render(request, 'backpages/category.html', content)



def edit_Category(request, id):
    if id:  # Ensure it's a POST request for safety
        category = get_object_or_404(Category, id=id)

        content = {
            'category':category
        }
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    return render(request, 'backpages/editcategory.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def update_Category(request):
    if request.method == 'POST':
        try:
            # Retrieve the service data from POST
            categoryId = request.POST.get('categoryId')
            name = request.POST.get('name')
            slug = request.POST.get('slug')

            # Ensure all fields are provided
            if not name:
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Fetch the existing service using the serviceId
            category = Category.objects.get(id=categoryId)  # Assuming 'id' is the primary key

            # Generate a unique slug (optional, if the name changes)
            slug = generate_unique_slug(name)

            # Update the service object with the new values
            category.name = name
            category.slug = slug

            # Save the updated   

            category.save() 

            return JsonResponse({'message': 'Category updated successfully!'}, status=200)

        except Category.DoesNotExist:
            return JsonResponse({'message': 'Category not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)







# Contact & address 

def addContactAddress(request):

    address = ContactAddress.objects.all()
    content = {
        'address':address
    }

    return render(request, 'backpages/addcontact_address.html', content)

from django.http import JsonResponse 

import json

@csrf_exempt
def add_ContactAddress(request):
    if request.method == 'POST':
        try:
            # Parse the POST data
            # data = json.loads(request.body)
            emailone = request.POST.get('emailone')
            emailtwo = request.POST.get('emailtwo')
            phoneone = request.POST.get('phoneone')
            phonetwo = request.POST.get('phonetwo')
            addressone = request.POST.get('addressone')
            addresstwo = request.POST.get('addresstwo')
            workday = request.POST.get('workday')
            worktime = request.POST.get('worktime')
            socialtext = request.POST.get('socialtext')
            facebook = request.POST.get('facebook')
            twitter = request.POST.get('twitter')
            whatsapp = request.POST.get('whatsapp')
            instagram = request.POST.get('instagram')
            linkedin = request.POST.get('linkedin')
            footertext = request.POST.get('footertext')

            # Validate required fields
            if not emailone or not phoneone:
                return JsonResponse({'message': 'Email and phoneone are required fields.'}, status=400)

            # Create the ContactAddress object
            contact_address = ContactAddress.objects.create(
                emailone=emailone,
                emailtwo=emailtwo,
                phoneone=phoneone,
                phonetwo=phonetwo,
                addressone=addressone,
                addresstwo=addresstwo,
                workday=workday,
                worktime=worktime,
                socialtext=socialtext,
                facebook=facebook,
                twitter=twitter,
                whatsapp=whatsapp,
                instagram=instagram,
                linkedin=linkedin,
                footertext=footertext
            )

            return JsonResponse({'message': 'ContactAddress added successfully!'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method. Only POST requests are allowed.'}, status=405)


def listContactAddress(request):
    # Fetch all ContactAddress objects
    contact_addresses = ContactAddress.objects.all()

    # Pass the data to the template
    content = {
        'contact_addresses': contact_addresses
    }

    # Render the appropriate template
    return render(request, 'backpages/contact_address.html', content)



def delete_ContactAddress(request, id):
    if id:  # Ensure it's a POST request for safety
        contact = get_object_or_404(ContactAddress, id=id)
        contact.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})


    contact_addresses = ContactAddress.objects.all()

    content = {
        'contact_addresses': contact_addresses
    }
    return render(request, 'backpages/contact_address.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def edit_ContactAddress(request, id):
    if id:  # Ensure it's a POST request for safety
        contact = get_object_or_404(ContactAddress, id=id)

        content = {
            'contact':contact
        }
    return render(request, 'backpages/editcontact.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def update_ContactAddress(request):
    if request.method == 'POST':
        try:
            # Retrieve the contact ID from POST data
            contact_id = request.POST.get('contactId')
            if not contact_id:
                return JsonResponse({'message': 'Contact ID is required.'}, status=400)

            # Load JSON data from the request body
            # data = json.loads(request.body)

            # Retrieve fields from the request data
            emailone = request.POST.get('emailone')
            emailtwo = request.POST.get('emailtwo')
            phoneone = request.POST.get('phoneone')
            phonetwo = request.POST.get('phonetwo')
            addressone = request.POST.get('addressone')
            addresstwo = request.POST.get('addresstwo')
            workday = request.POST.get('workday')
            worktime = request.POST.get('worktime')
            socialtext = request.POST.get('socialtext')
            facebook = request.POST.get('facebook')
            twitter = request.POST.get('twitter')
            whatsapp = request.POST.get('whatsapp')
            instagram = request.POST.get('instagram')
            linkedin = request.POST.get('linkedin')
            footertext = request.POST.get('footertext')

            # Validate required fields
            if not emailone or not phoneone:
                return JsonResponse({'message': 'emailone and phoneone are required fields.'}, status=400)

            # Fetch the existing ContactAddress using the ID
            contact = ContactAddress.objects.get(id=contact_id)

            # Update the ContactAddress object with new values
            contact.emailone = emailone
            contact.emailtwo = emailtwo
            contact.phoneone = phoneone
            contact.phonetwo = phonetwo
            contact.addressone = addressone
            contact.addresstwo = addresstwo
            contact.workday = workday
            contact.worktime = worktime
            contact.socialtext = socialtext
            contact.facebook = facebook
            contact.twitter = twitter
            contact.whatsapp = whatsapp
            contact.instagram = instagram
            contact.linkedin = linkedin
            contact.footertext = footertext

            # Save the updated ContactAddress
            contact.save()

            return JsonResponse({'message': 'ContactAddress updated successfully!'}, status=200)

        except ContactAddress.DoesNotExist:
            return JsonResponse({'message': 'ContactAddress not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)





def getContactImage(request):

    return render(request, 'backpages/addcontactimage.html')


def listContactImage(request):

    contact = ContactImage.objects.all()

    content = {
        'contact': contact
    }

    return render(request, 'backpages/contactimage.html', content)




@csrf_exempt
def add_ContactImage(request):
    if request.method == 'POST':
        try:
            if 'image' in request.FILES:

                LOGO_IMAGE_SIZE = (454, 790)      # Example size for slider image

                # Process images if provided
                image_file_resized = (
                    resize_image(request.FILES.get('image'), LOGO_IMAGE_SIZE) 
                    if 'image' in request.FILES else None
                )

                # Save the resized image to the Logo model
                contactIMage = ContactImage.objects.create(image=image_file_resized, created_at=now())

            return JsonResponse({'message': 'ContactImage updated successfully!'}, status=200)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)

def delete_ContactImage(request, id):
    if id:  # Ensure it's a POST request for safety
        contact = get_object_or_404(ContactImage, id=id)
        contact.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})
    contact = ContactImage.objects.all()

    content = {
        'contact': contact
    }

    return render(request, 'backpages/contactimage.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})




# Privacy and Policy 

def addPrivacy(request):

    privacy = PrivacyPolicy.objects.all()
    content = {
        'privacy':privacy
    }

    return render(request, 'backpages/add_privacy.html', content)

@csrf_exempt
def add_PrivacyPolicy(request):
    if request.method == 'POST':
        try:
            description = request.POST.get('description')

            # Validate required fields
            if not description:
                return JsonResponse({'message': 'Description is required.'}, status=400)

            # Create the blog
            privacy = PrivacyPolicy.objects.create(
                description=description,
            )

            return JsonResponse({'message': 'Privacy and Policy added successfully!'}, status=201)

        except PrivacyPolicy.DoesNotExist:
            return JsonResponse({'message': 'Privacy and Policy not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)



def listPrivacyPolicy(request):

    privacy = PrivacyPolicy.objects.all()

    content = {
        'privacy': privacy
    }

    return render(request, 'backpages/privacy.html', content)


def delete_PrivacyPolicy(request, id):
    if id:  # Ensure it's a POST request for safety
        privacy = get_object_or_404(PrivacyPolicy, id=id)
        privacy.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})


    privacy = PrivacyPolicy.objects.all()

    content = {
        'privacy': privacy
    }
    return render(request, 'backpages/privacy.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def edit_PrivacyPolicy(request, id):
    if id:  # Ensure it's a POST request for safety
        privacy = get_object_or_404(PrivacyPolicy, id=id)

        content = {
            'privacy':privacy,
        }
    return render(request, 'backpages/editprivacy.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def update_PrivacyPolicy(request):
    if request.method == 'POST':
        try:
            # Retrieve the service data from POST
            privacyId = request.POST.get('privacyId') 
            description = request.POST.get('description')

            # Ensure all fields are provided
            if not  privacyId  or not description:
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Fetch the existing service using the serviceId
            privacy = PrivacyPolicy.objects.get(id=privacyId)  # Assuming 'id' is the primary key 

            # Update the service object with the new values
            privacy.description = description



            privacy.save()

            return JsonResponse({'message': 'Privacy and Policy updated successfully!'}, status=200)

        except PrivacyPolicy.DoesNotExist:
            return JsonResponse({'message': 'Privacy and Policy not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)







# Users

def listUser(request):

    users = User.objects.all()

    content = {
        'users': users
    }

    return render(request, 'backpages/users.html', content)


def delete_User(request, id):
    if id:  # Ensure it's a POST request for safety
        user = get_object_or_404(User, id=id)
        user.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})


    users = User.objects.all()

    content = {
        'users': users
    }
    return render(request, 'backpages/users.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# Profile

def addUser(request):

    users = User.objects.all()
    content = {
        'users':users
    }

    return render(request, 'backpages/add_users.html', content)

@csrf_exempt
def add_PrivacyPolicy(request):
    if request.method == 'POST':
        try:
            description = request.POST.get('description')

            # Validate required fields
            if not description:
                return JsonResponse({'message': 'Description is required.'}, status=400)

            # Create the blog
            privacy = PrivacyPolicy.objects.create(
                description=description,
            )

            return JsonResponse({'message': 'Privacy and Policy added successfully!'}, status=201)

        except PrivacyPolicy.DoesNotExist:
            return JsonResponse({'message': 'Privacy and Policy not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)



def listPrivacyPolicy(request):

    privacy = PrivacyPolicy.objects.all()

    content = {
        'privacy': privacy
    }

    return render(request, 'backpages/privacy.html', content)


def delete_PrivacyPolicy(request, id):
    if id:  # Ensure it's a POST request for safety
        privacy = get_object_or_404(PrivacyPolicy, id=id)
        privacy.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})


    privacy = PrivacyPolicy.objects.all()

    content = {
        'privacy': privacy
    }
    return render(request, 'backpages/privacy.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def edit_PrivacyPolicy(request, id):
    if id:  # Ensure it's a POST request for safety
        privacy = get_object_or_404(PrivacyPolicy, id=id)

        content = {
            'privacy':privacy,
        }
    return render(request, 'backpages/editprivacy.html', content)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def update_PrivacyPolicy(request):
    if request.method == 'POST':
        try:
            # Retrieve the service data from POST
            privacyId = request.POST.get('privacyId') 
            description = request.POST.get('description')

            # Ensure all fields are provided
            if not  privacyId  or not description:
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            # Fetch the existing service using the serviceId
            privacy = PrivacyPolicy.objects.get(id=privacyId)  # Assuming 'id' is the primary key 

            # Update the service object with the new values
            privacy.description = description



            privacy.save()

            return JsonResponse({'message': 'Privacy and Policy updated successfully!'}, status=200)

        except PrivacyPolicy.DoesNotExist:
            return JsonResponse({'message': 'Privacy and Policy not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)




# Reset Cdoe

def listCode(request):

    codes = ResetCode.objects.all()

    content = {
        'codes': codes
    }

    return render(request, 'backpages/codes.html', content)


def delete_Code(request, id):
    if id:  # Ensure it's a POST request for safety
        code = get_object_or_404(ResetCode, id=id)
        code.delete()
        # return JsonResponse({'success': True, 'message': 'Service deleted successfully.'})


    codes = ResetCode.objects.all()

    content = {
        'codes': codes
    }
    return render(request, 'backpages/codes.html', content)
    # return JsonResponse({'success': codes, 'message': 'Invalid request method.'})



def edit_user(request, id):
    if id:  # Ensure it's a POST request for safety
        user = get_object_or_404(User, id=id)

        # Fetch the user's profile (assuming there's a one-to-one relationship between User and Profile)
        try:
            profile = user.profile  # Access the related profile
        except AttributeError:
            profile = None  # Handle case where profile doesn't exist

        content = {
            'user':user,
            'profile':profile
        }
    return render(request, 'backpages/edituser.html', content)



def update_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        user = get_object_or_404(User, id=user_id)

        # Fetch or create the profile
        profile, created = Profiles.objects.get_or_create(user=user)

        # Update profile fields
        profile.account_type = request.POST.get('account_type', profile.account_type)
        profile.address = request.POST.get('address', profile.address)

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        return JsonResponse({'status': 'User updated successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
