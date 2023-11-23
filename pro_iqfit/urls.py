# urls.py
from django.contrib import admin
from django.urls import path, include
from app_core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("unicorn/", include("django_unicorn.urls")),
    
    path('', views.display_questions_view, name='display_questions'),
    path('load-inputs/<int:question_id>/<int:option_id>/', views.load_additional_inputs, name='load_additional_inputs'),
    path('validate-input/<int:option_id>/', views.validate_input, name='validate_input'),
    path('quiz/', views.submit_quiz, name='submit_quiz'),
    path('thankyou/', views.thankyou, name='thank_you'),
    path('load-questions/', views.load_questions_page, name='load_questions_page'),
    # path('update-response/<int:question_id>/', views.update_response, name='update_response'),


]
