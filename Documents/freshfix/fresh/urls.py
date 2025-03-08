from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home,editabout,delete_abouts,listAbout,edit_about,add_about,editslide,edit_slide,delete_slide,add_slider,listSlider,addSlider,delete_logo, listLogos,getLogo,add_logo,update_service,edit_service,delete_service,listServices,about,service,blog,blogDetails,serviceDetails,contact,privacy,dashboard,addServices,add_service
from userauths.views import register,login_view,logout_view, check_mail,reset_password
from .views import addTeam,sendToMail,edit_team,add_team,delete_team,listTeam,update_team,addUs,add_us,listUs,delete_us,edit_us,update_us
from .views import addtestimonials,save_testimonials, listTestimonials,delete_testimonials,edit_testimonials,update_testimonial
from .views import  addBlog,add_Blog,listBlog,delete_Blog,edit_Blog,update_Blog,add_about2
from .views import  addContactAddress, add_ContactAddress, listContactAddress, delete_ContactAddress, edit_ContactAddress, update_ContactAddress
from .views import  blogByCategory,add_about3,addCategory,add_category,listCategory,delete_Category,edit_Category,update_Category,add_blog
from .views import getContactImage,listContactImage,add_ContactImage,delete_ContactImage, sendComment,listComments,delete_comment
from .views import  addPrivacy,add_PrivacyPolicy,listPrivacyPolicy,delete_PrivacyPolicy,edit_PrivacyPolicy,update_PrivacyPolicy
from .views import listUser,delete_User,listCode,delete_Code,edit_user,update_user

app_name = "fresh"

urlpatterns = [

    path("check-mail", check_mail, name="check_mail"),
    path("list-user", listUser, name="listUser"),
    path("delete-user/<int:id>/", delete_User, name="delete_User"),
    path("edit-user/<int:id>/", edit_user, name="edit_user"),
    path("update-user", update_user, name="update_user"),
    

    path("list-code", listCode, name="listCode"),
    path("delete-code/<int:id>/", delete_Code, name="delete_Code"),

    


    path("add-policy", addPrivacy, name="addPrivacy"),
    path("save-policy", add_PrivacyPolicy, name="add_PrivacyPolicy"),
    path("list-policy", listPrivacyPolicy, name="listPrivacyPolicy"),
    path("delete-policy/<int:id>/", delete_PrivacyPolicy, name="delete_PrivacyPolicy"),
    path("edit-policy/<int:id>/", edit_PrivacyPolicy, name="edit_PrivacyPolicy"),
    path("update-policy", update_PrivacyPolicy, name="update_PrivacyPolicy"),


    path("add-contact-image", getContactImage, name="getContactImage"),
    path("save-contact-image", listContactImage, name="listContactImage"),
    path("list-contact-image", add_ContactImage, name="add_ContactImage"),
    path("delete-contact-image/<int:id>/", delete_ContactImage, name="delete_ContactImage"),



    path("add-contact-address", addContactAddress, name="addContactAddress"),
    path("save-contact-address", add_ContactAddress, name="add_ContactAddress"),
    path("list-contact-address", listContactAddress, name="listContactAddress"),
    path("delete-contact-address/<int:id>/", delete_ContactAddress, name="delete_ContactAddress"),
    path("edit-contact-address/<int:id>/", edit_ContactAddress, name="edit_ContactAddress"),
    path("update-contact-address", update_ContactAddress, name="update_ContactAddress"), 
    
    
    


    path("add-Blog", addBlog, name="addBlog"),
    path("add-Blog", add_Blog, name="add_Blog"),
    path("list-Blog", listBlog, name="listBlog"),
    path("delete-Blog/<int:id>/", delete_Blog, name="delete_Blog"),
    path("edit-Blog/<int:id>/", edit_Blog, name="edit_Blog"),
    path("update-Blog", update_Blog, name="update_Blog"),
    path("submit-Blog", add_blog, name="add_blog"),
    


    path("add-Category", addCategory, name="addCategory"),
    path("add-Category", add_category, name="add_category"),
    path("list-Category", listCategory, name="listCategory"),
    path("delete-Category/<int:id>/", delete_Category, name="delete_Category"),
    path("edit-Category/<int:id>/", edit_Category, name="edit_Category"),
    path("update-Category", update_Category, name="update_Category"),










    path("add-testimonials", addtestimonials, name="addtestimonials"),
    path("save_testimonials", save_testimonials, name="save_testimonials"),
    path("list-testimonials", listTestimonials, name="listTestimonials"),
    path("delete_testimonials/<int:id>/", delete_testimonials, name="delete_testimonials"),
    path("edit_testimonials/<int:id>/", edit_testimonials, name="edit_testimonials"),
    path("update-testimonial", update_testimonial, name="update_testimonial"),
    path('', home, name='home'),
    path('about', about, name='about'),
    path('service', service, name='service'),
    path('blog', blog, name='blog'),
    path('blog-detail/<slug:slug>/', blogDetails, name='blogDetails'),
    path('blog-category/<slug:slug>/', blogByCategory, name='blogByCategory'),
    path('password-reset/<str:email>/', reset_password, name='reset_password'),
    
    
    path('service-detail/<slug:slug>', serviceDetails, name='serviceDetails'),
    path('contact', contact, name='contact'),
    path('addTeam', addTeam, name='addTeam'),
    path('add_team', add_team, name='add_team'),
    path('privacy', privacy, name='privacy'),
     path("register", register, name="register"),
     path("login", login_view, name="login_view"),
     path("logout", logout_view, name="logout_view"),
     path("dashboard", dashboard, name="dashboard"),
     path("add_logo", add_logo, name="add_logo"),
     path("add_about", add_about, name="add_about"),
     path("add_about", add_about2, name="add_about2"),
     path("add_about_", add_about3, name="add_about3"),
     path("list-about", listAbout, name="listAbout"),
     path("update-about", editabout, name="editabout"),     
     path("edit-about/<int:id>/", edit_about, name="edit_about"),
     path("delete-about/<int:id>/", delete_abouts, name="delete_abouts"),     
     path("getLogo", getLogo, name="getLogo"),
     path("update-service", update_service, name="update_service"),
     path("update-team", update_team, name="update_team"),
     path("add-services", addServices, name="addServices"),
     path('add-service/', add_service, name='add_service'),
     path('add-slider/', add_slider, name='add_slider'),
     path('add-slider/', addSlider, name='addSlider'),
     path('list-service/', listServices, name='listServices'),
     path('list-team/', listTeam, name='listTeam'),
     path('list-logos/', listLogos, name='listLogos'),
     path('list-slide/', listSlider, name='listSlider'),
     path('delete-service/<int:id>/', delete_service, name='delete_service'),
     path('delete-team/<int:id>/', delete_team, name='delete_team'),
     path('delete-logo/<int:id>/', delete_logo, name='delete_logo'),
     path('edit-service/<int:id>/', edit_service, name='edit_service'),
     path('edit-team/<int:id>/', edit_team, name='edit_team'),
     path('edit-slide/<int:id>/', edit_slide, name='edit_slide'),
     path('update-slide', editslide, name='editslide'),
     path('delete-slide/<int:id>/', delete_slide, name='delete_slide'),
    path("addus", addUs, name="addUs"),
    path("add-us", add_us, name="add_us"),
    path("list-us", listUs, name="listUs"),
    path("delete-us/<int:id>/", delete_us, name="delete_us"),
    path("edit-us/<int:id>/", edit_us, name="edit_us"),
    path("update-us", update_us, name="update_us"),
    path("send-mail", sendToMail, name="sendToMail"),     
    path("send-comment", sendComment, name="sendComment"),     
    path("list-comment", listComments, name="listComments"),     
    path("delete_comment/<int:id>/", delete_comment, name="delete_comment"),     
    
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)