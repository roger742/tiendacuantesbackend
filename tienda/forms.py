from django import forms
from .models import Cliente, Rol, Vendedor
from django.contrib.auth.forms import UserCreationForm

# Crear un formulario de cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'aPaterno', 'aMaterno', 'telefono', 'correo', 'usuario', 'password', 'rol']
    
    # Asegúrate de que el campo de rol se muestre como un select
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), empty_label="Selecciona un rol")

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['nombre', 'aPaterno', 'aMaterno', 'telefono', 'correo', 'usuario', 'password', 'rol']
    
    # Asegúrate de que el campo de rol se muestre como un select
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), empty_label="Selecciona un rol")