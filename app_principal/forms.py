from django import forms
from .models import Profesional, Plan, Especialidades, CrearTurno
from django.core.exceptions import ValidationError


class AfiliarseForm(forms.Form):
    nombre_completo = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre Completo'}),label='', required= True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='',required= True)
    telefono = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Teléfono', 'class': 'tel'}),label='', required=True)   
    plan = forms.ChoiceField(choices=Plan.plan_select, widget=forms.Select(attrs={'class': 'select','placeholder' : "Elige un Plan" } ),label='', required=True)
    
class LoginMedico(forms.Form):
    matricula = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Matrícula'}),required=True)
    contrasena = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), required=True)
    
    def clean_matricula(self):
        if self.cleaned_data ['matricula'] != int:
            raise ValidationError("la Matrícula debe ser numérica")
        
        return self.cleaned_data ['matricula']           

         
class AltaAfiliado(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}), label='', required= True)
    apellido = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}), label='', required= True)
    dni = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'DNI', 'class': 'tel'}),label='', required=True) 
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}),  label='',required= True)
    numeroAfiliado = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Número de Afiliado'}), label='', required= True)          
    plan = forms.ChoiceField(choices=Plan.plan_select, widget=forms.Select(attrs={'class': 'select', 'placeholder': 'Elige un Plan'}), label='', required=True)

#Debe haber al menos un formulario asociado a un modelo.

class AltaProfesionalModelForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = '__all__'
        widgets = {
            'matricula': forms.NumberInput(attrs={'placeholder': 'Matrícula', 'class': 'mi-clase'}),
            'cuit': forms.NumberInput(attrs={'placeholder': 'CUIT', 'class': 'mi-clase'}),
            'especialidad': forms.Select(attrs={'placeholder': 'Especialidad', 'class': 'mi-clase'}),
        }# NO FUNCIONA EL WIDGET

    def clean_cuit(self):
        cuit = self.cleaned_data.get('cuit')  

        
        cuit = cuit.strip()

        if not cuit.isdigit():
            raise forms.ValidationError("El CUIT debe contener solo dígitos.")

        if len(cuit) != 11:
            raise forms.ValidationError("El CUIT debe tener 11 dígitos.")
        
        return cuit  

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidades
        fields = '__all__'
      
class CrearTurnoForm(forms.ModelForm):
    class Meta:
        model = CrearTurno  
        fields = ['fecha', 'hora', 'profesional'] 
  
