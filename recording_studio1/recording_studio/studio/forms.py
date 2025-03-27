from django import forms
from .models import Artist, Producer, Client, Manager, Project, User

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'genre']

class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = ['name', 'albums_produced']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email']

class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['name', 'email']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['album_image', 'name', 'end_date', 'current_status', 'performer']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'role']  
    
class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=100)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)