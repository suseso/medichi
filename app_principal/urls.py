
from django.urls import path,re_path
from app_principal import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import TurnoDetalleView, TurnoActualizarView, TurnoEliminarView, TurnoCrearView, TurnoQuitarAfiliadoView

urlpatterns = [
    path("", views.index, name="index"),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app_principal/login.html'),name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path("afiliarse", views.afiliarse, name="afiliarse"),
    path("contactos", views.contactos, name="contactos"),
    re_path(r'pacientes/historico/(?P<year>[0-9]{4})/$', views.pacientes_historico, name='pacientes_historico'),
    
    path("inicio-administracion", views.inicio_administracion, name="inicio-administracion"),
    path("alta-afiliado", views.alta_afiliado, name="alta-afiliado"),
    path("alta-especialidad", views.alta_especialidad, name="alta-especialidad"),
    path('alta-profesional', views.ProfesionalCreateView.as_view(), name="alta_profesional"),
    path('listado-especialidades', views.listado_especialidades, name='listado_especialidades'),
    path('listado-afiliados', views.listado_afiliados, name='listado_afiliados'),
    path('listado-profesionales', views.ProfesionalListView.as_view(), name="listado_profesionales"),
    
    path('registrar-turno/', login_required(TurnoCrearView.as_view()), name='registrar_turno'),
    path('seleccionar-turno/', login_required(TurnoActualizarView.as_view()), name='seleccionar_turno_afiliado'),
    path('listado-turnos/', views.listado_turnos, name='listado_turnos'),
    path('turnos/<int:pk>/', login_required(TurnoDetalleView.as_view()), name='turno_detalle'),
    path('turnos/<int:pk>/editar/', login_required(TurnoActualizarView.as_view()), name='turno_actualizar'),
    path('turnos/<int:pk>/eliminar/', login_required(TurnoEliminarView.as_view()), name='turno_eliminar'),
    path('turnos/quitar-afiliado/<int:pk>/', login_required(TurnoQuitarAfiliadoView.as_view()), name='quitar_afiliado'),
    ]
