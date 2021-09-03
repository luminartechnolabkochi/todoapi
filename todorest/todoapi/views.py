from django.shortcuts import render
from rest_framework.views import APIView
from .models import Todo
from .seriaizers import TodoSerializer,UserCreationSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.authtoken.models import Token
#auth
from django.contrib.auth import authenticate,login,logout
from rest_framework import mixins
from rest_framework  import generics
from rest_framework import authentication,permissions
class Todos(APIView):

    def get(self,request):
        todos=Todo.objects.all()

        serializer=TodoSerializer(todos,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    #100=>
    #200=>success
    #300=>redirectional
    #400=>clinet errors
    #500=>server errors



class TodoDetails(APIView):
   def get_object(self,pk):
       try:
        return Todo.objects.get(id=pk)
       except Todo.DoesNotExist:
           raise Http404

   def get(self,request,**kwargs):
       todo=self.get_object(kwargs["pk"])
       serializer=TodoSerializer(todo)
       return Response(serializer.data)

   def put(self,request,**kwargs):

       todo=self.get_object(kwargs["pk"])
       serializer=TodoSerializer(todo,data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data,status=status.HTTP_200_OK)
       else:
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


   def delete(self,request,**kwargs):
        todo=self.get_object(kwargs["pk"])
        todo.delete()
        return Response({"msg":"deleted"})


class UserCreationView(APIView):

    def post(self,request):
        serilaizer=UserCreationSerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                token,created=Token.objects.get_or_create(user=user)
                return Response({"token":token.key})

            else:
                return Response({"msg":"invalid credentials"})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class TodoList(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin
               ):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def get(self,request,*args,**kwargs):
        print(request.user)
        return self.list( request, *args, **kwargs)



    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class TodoDetailView(generics.GenericAPIView,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin
               ):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)


    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)



"from rest_framework.autho"


