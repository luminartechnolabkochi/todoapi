
from django.urls import path
from .views import Todos,TodoDetails,UserCreationView,LoginView,TodoList,TodoDetailView
urlpatterns = [
  path("todos",TodoList.as_view()),
  path("todos/<int:pk>",TodoDetailView.as_view()),
  path("accounts/signup",UserCreationView.as_view()),
  path("accounts/signin",LoginView.as_view())
]
