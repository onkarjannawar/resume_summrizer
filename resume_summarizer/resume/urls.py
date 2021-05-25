from django.urls import path
from .import views

app_name="fileapp"
urlpatterns = [
    
    path("",views.resume_view),
    path("upload",views.send_files,name="uploads"),
    path("home",views.return_home_view),
    path("show",views.show_view)
    ]