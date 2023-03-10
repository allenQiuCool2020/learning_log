from django.urls import path
from .import views
from django.contrib.auth.views import LoginView
urlpatterns = [
	path('index/', views.index, name="index"),
	path('topics/', views.topics, name="topics"),
	path('topic/<str:topic_id>', views.topic, name='topic'),
	path('new_topic/', views.new_topic, name = 'new_topic'),
	path('new_entry/<str:topic_id>', views.new_entry, name='new_entry'),
	path('edit_entry/<str:entry_id>',views.edit_entry, name='edit_entry'),
	path('login/', LoginView.as_view(), name='registration/login'),
	path('logout/', views.logout_view, name='logout'),
	path('register/', views.register, name='register')
]