from django.db import models

from django.utils.text import slugify
from django.utils.timezone import now


class ContactAddress(models.Model):
    emailone = models.CharField(max_length=255)
    emailtwo = models.CharField(max_length=255)
    phoneone = models.CharField(max_length=255)
    phonetwo = models.CharField(max_length=255)
    addressone = models.CharField(max_length=255)
    addresstwo = models.CharField(max_length=255)
    workday = models.CharField(max_length=255)
    worktime = models.CharField(max_length=255)
    socialtext = models.TextField(null=True, blank=True, default="socialtext")
    facebook = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    footertext = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time

    def __str__(self):
        return self.emailone
    

class Team(models.Model):
    name = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    link1 = models.CharField(max_length=255)
    link2 = models.CharField(max_length=255)
    link3 = models.CharField(max_length=255)
    link4 = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    image = models.ImageField(upload_to='service/', null=True)
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time

    def __str__(self):
        return self.name
    
class BeforeAfter(models.Model):
    before = models.ImageField(upload_to='service/', null=True)
    after = models.ImageField(upload_to='service/', null=True)
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time

    def __str__(self):
        return self.created_at
    
class WhyChoose(models.Model):
    header = models.CharField(max_length=255, null=True)
    paragraph = models.CharField(max_length=255, null=True)
    headerone = models.CharField(max_length=255)
    headertwo = models.CharField(max_length=255)
    headerthree = models.CharField(max_length=255)
    paragraphone = models.CharField(max_length=255)
    paragraphtwo = models.CharField(max_length=255)
    paragraphthree = models.CharField(max_length=255)
    imageone = models.ImageField(upload_to='service/', null=True)
    imagetwo = models.ImageField(upload_to='service/', null=True)
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time

    def __str__(self):
        return self.name
    
class Book(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    paragraph = models.CharField(max_length=255)
    image = models.ImageField(upload_to='service/', null=True)
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time

    def __str__(self):
        return self.name
    

class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True)
    subject = models.CharField(max_length=255) 
    service = models.CharField(max_length=255) 
    message = models.CharField(max_length=255) 
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services', null=True)
    image = models.ImageField(upload_to='service/', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time

    def __str__(self):
        return self.name

class Image(models.Model):
    service = models.ForeignKey(Service, related_name='images', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='services/')
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time



class PrivacyPolicy(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.created_at



class Blog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')
    image = models.ImageField(upload_to='blogs/featured/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, related_name='images', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='blogs/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blog.name} - Image {self.id}"
    
class Comments(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blogs', null=True)
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time

    def __str__(self):
        return self.fname

class Logo(models.Model):
    logo = models.ImageField(upload_to='logo/')
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time



class ContactImage(models.Model):
    image = models.ImageField(upload_to='image/')
    created_at = models.DateTimeField(default=now, editable=False)  # Automatically sets to the current date and time



class SliderSection(models.Model):
    sub_title = models.CharField(max_length=255, help_text="Short subtitle for the slider")
    title = models.CharField(max_length=255, help_text="Main title for the slider")
    paragraph = models.TextField(help_text="Description paragraph for the slider")
    btntext = models.TextField(help_text="Button text for the slider")
    contact_number = models.CharField(max_length=20, help_text="Contact number to display")
    contact_link = models.URLField(help_text="Link for the 'Describe More' button")
    background_image = models.ImageField(upload_to='slider/backgrounds/', help_text="Background image")
    slider_image = models.ImageField(upload_to='slider/images/', help_text="Main image for the slider")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class AboutSection(models.Model):
    sub_title = models.CharField(max_length=255, help_text="Short subtitle for the slider")
    title = models.CharField(max_length=255, help_text="Main title for the slider")
    paragraph = models.TextField(help_text="Description paragraph for the slider")
    btntext = models.TextField(help_text="Button text for the slider")
    list_one = models.CharField(max_length=20, help_text="Contact number to display")
    list_two = models.CharField(max_length=20, help_text="Contact number to display")
    list_three = models.CharField(max_length=20, help_text="Contact number to display")
    name = models.CharField(max_length=20, help_text="Contact number to display", null=True)
    job = models.CharField(max_length=20, help_text="Contact number to display", null=True)
    background_image = models.ImageField(upload_to='slider/backgrounds/', help_text="Background image")
    slider_image = models.ImageField(upload_to='slider/images/', help_text="Main image for the slider")
    profile = models.ImageField(upload_to='slider/images/', help_text="Main image for the slider")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title