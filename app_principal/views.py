from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta
from .forms import CrearTurnoForm, AfiliarseForm, AltaAfiliado, EspecialidadForm
from .models import Afiliado, Profesional,Plan, Especialidades, CrearTurno
from django.db import IntegrityError
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views import View


def index(request):
    return render(
        request,
        "app_principal/index.html",
    )


def contactos(request):
    return render(
        request,
        "app_principal/contactos.html",
    )


def afiliarse(request):
    if request.method == 'POST':
        afiliarse = AfiliarseForm(request.POST)
        
        if afiliarse.is_valid():

            messages.success(request, 'Datos enviados con éxito.')
            
            return redirect(reverse("index"))
    else:
        afiliarse = AfiliarseForm()
    
    context = {
        'afiliarse_form': afiliarse
    }

    return render(request, "app_principal/afiliarse.html", context)


@login_required
def inicio_administracion(request):  # punto del tp
    # Esta data en el futuro vendrá de la base de datos
    listado = [
    "Lucas Romualdo",
    "Betiana Quiroga",
        
    ]

    context = {
        "nombre_doctor": "gonzalo cardozo",
        "fecha": datetime.now(),
        "genero": 'Masculino',
        "listado_pacientes": listado,
        "cant_pacientes": len(listado),
    }
    return render(request, "app_principal/inicio-administracion.html", context)


@login_required
def pacientes_historico(request,year):
    return HttpResponse(f'<h1>Historico de Pacientes del año: {year}</h1>')


@login_required
def alta_afiliado(request):
    context = {}

    if request.method == "POST":
        alta_afiliado_form = AltaAfiliado(request.POST)

        if alta_afiliado_form.is_valid():         
            nombre = alta_afiliado_form.cleaned_data['nombre']
            apellido = alta_afiliado_form.cleaned_data['apellido']
            email = alta_afiliado_form.cleaned_data['email']
            dni = alta_afiliado_form.cleaned_data['dni']
            numeroAfiliado = alta_afiliado_form.cleaned_data['numeroAfiliado']
            plan_pk = alta_afiliado_form.cleaned_data['plan']

            try:                
                plan = Plan.objects.get(pk=plan_pk)
                nuevo_afiliado = Afiliado(
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    dni=dni,
                    numeroAfiliado=numeroAfiliado,
                    plan=plan,
                )
                nuevo_afiliado.save()

                messages.info(request, "Afiliado dado de alta correctamente")
                return redirect(reverse("listado_afiliados"))

            except Plan.DoesNotExist:
                messages.error(request, "El Plan seleccionado no es válido.")
            except IntegrityError as ie:
                messages.error(request, "Ocurrió un error al intentar dar de alta al paciente")
                return redirect(reverse("index"))

    else:
        alta_afiliado_form = AltaAfiliado()

    context['alta_afiliado_form'] = alta_afiliado_form
    return render(request, 'app_principal/alta-afiliado.html', context)


@login_required
def listado_afiliados(request):
    listado = Afiliado.objects.all().order_by('dni')
    context = {

        'listado_afiliados': listado,
        'cant_afiliados': len(listado),
    }

    return render(request, 'app_principal/listado-afiliados.html', context)


class ProfesionalCreateView(LoginRequiredMixin,CreateView):
    model = Profesional
    template_name = 'app_principal/alta-profesional.html'
    success_url = 'listado-profesionales'
    fields = '__all__'
    
    

class ProfesionalListView(ListView):
    model = Profesional
    context_object_name = 'listado_profesionales'
    template_name = 'app_principal/listado-profesionales.html'
    ordering = ['cuit']


@login_required
def alta_especialidad(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_especialidades')  
    else:
        form = EspecialidadForm()
    return render(request, 'app_principal/alta-especialidad.html', {'form': form})


def listado_especialidades(request):
    listado = Especialidades.objects.all()
    context = {

        'listado_especialidades': listado,
        'cant_especialidades': len(listado),
    }

    return render(request, 'app_principal/listado-especialidades.html', context)

@login_required
def listado_turnos(request):
    especialidades = Especialidades.objects.all()
    profesionales = Profesional.objects.all()
    especialidad_id = request.GET.get('especialidad')
    profesional_id = request.GET.get('profesional')
    fecha = request.GET.get('fecha')
    turnos = CrearTurno.objects.all()

    if especialidad_id:
        turnos = turnos.filter(especialidades__id=especialidad_id)

    if profesional_id:
        turnos = turnos.filter(profesional_id=profesional_id)

    if fecha:
        turnos = turnos.filter(fecha=fecha)

    turnos = turnos.order_by('fecha', 'hora')
    return render(request, 'app_principal/listado-turnos.html', {'turnos': turnos, 'especialidades': especialidades, 'profesionales': profesionales})


'''
def registrar_turno_medico(request):
    if request.method == 'POST':
        form = CrearTurnoForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            profesional = form.cleaned_data['profesional']  
            especialidades = profesional.especialidades.all(
            hora_fin = datetime.combine(fecha, hora) + timedelta(hours=5)         
            intervalo = timedelta(minutes=20)
            hora_actual = datetime.combine(fecha, hora)
            
            while hora_actual < hora_fin:
                nuevo_turno = CrearTurno(
                    fecha=hora_actual.date(),
                    hora=hora_actual.time(),
                    profesional=profesional,
                    disponible=True  
                )
                nuevo_turno.save()
                nuevo_turno.especialidades.set(especialidades) 

                hora_actual += intervalo
            
            messages.success(request, 'Los turnos se han creado correctamente.')
            return redirect('listado_turnos')
    else:
        form = CrearTurnoForm()

    return render(request, 'app_principal/registrar-turno.html', {'form': form})



def seleccionar_turno_afiliado(request):
    if request.method == 'POST':
        form = CrearTurnoForm(request.POST)
        if form.is_valid():
            turno_id = request.POST.get('turno_id')
            afiliado_id = request.POST.get(f'afiliado_{turno_id}')
            
            turno_seleccionado = CrearTurno.objects.get(id=turno_id)
            
            if turno_seleccionado.disponible:
                # Asigna el afiliado al turno
                turno_seleccionado.afiliado_id = afiliado_id
                turno_seleccionado.disponible = False
                turno_seleccionado.save()
                
                messages.success(request, 'Afiliado asignado al turno exitosamente.')
            else:
                
                messages.error(request, 'El turno seleccionado ya ha sido asignado.')
            
            return redirect('listado_turnos')
    else:
        form = CrearTurnoForm()
    # Resto de la lógica para obtener turnos y afiliados
    turnos = CrearTurno.objects.filter(disponible=True)
    afiliados = Afiliado.objects.all()
    return render(request, 'app_principal/seleccionar-turno.html', {'form': form, 'turnos': turnos, 'afiliados': afiliados})
'''

class TurnoCrearView(CreateView, LoginRequiredMixin):
    model = CrearTurno
    template_name = 'app_principal/registrar-turno.html'
    form_class = CrearTurnoForm 

    def form_valid(self, form):
        fecha = form.cleaned_data['fecha']
        hora = form.cleaned_data['hora']
        profesional = form.cleaned_data['profesional']
        especialidades = profesional.especialidades.all()
        hora_fin = datetime.combine(fecha, hora) + timedelta(hours=3)
        intervalo = timedelta(minutes=20)
        hora_actual = datetime.combine(fecha, hora)

        while hora_actual < hora_fin:
            nuevo_turno = CrearTurno(
                fecha=hora_actual.date(),
                hora=hora_actual.time(),
                profesional=profesional,
                disponible=True
            )
            nuevo_turno.save()
            nuevo_turno.especialidades.set(especialidades) 
            hora_actual += intervalo

        messages.success(self.request, 'Los turnos se han creado correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('listado_turnos')



class TurnoDetalleView(DetailView, LoginRequiredMixin):
    model = CrearTurno
    template_name = 'app_principal/turno_detalle.html'


class TurnoActualizarView(View, LoginRequiredMixin):
    template_name = 'app_principal/seleccionar-turno.html'
    form_class = CrearTurnoForm

    def get(self, request, *args, **kwargs):
        turnos = CrearTurno.objects.order_by('fecha', 'hora')
        afiliados = Afiliado.objects.all()
        context = {'turnos': turnos, 'afiliados': afiliados}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        turno_id = request.POST.get('turno_id')
        afiliado_id = request.POST.get(f'afiliado_{turno_id}')

        if turno_id and afiliado_id:
            turno = CrearTurno.objects.get(pk=turno_id)
            afiliado = Afiliado.objects.get(pk=afiliado_id)
            turno.afiliado = afiliado
            turno.disponible = False
            turno.save()

            messages.success(request, 'Turno asignado correctamente.')

        return redirect('seleccionar_turno_afiliado')

class TurnoQuitarAfiliadoView(View,LoginRequiredMixin ):
    def get(self, request, pk):
        turno = get_object_or_404(CrearTurno, pk=pk)
        turno.afiliado = None
        turno.disponible = True
        turno.save()
        return redirect('seleccionar_turno_afiliado')   


class TurnoEliminarView(DeleteView, LoginRequiredMixin):
    model = CrearTurno
    template_name = 'app_principal/turno_confirmar_eliminar.html'
    success_url = reverse_lazy('seleccionar_turno_afiliado')  