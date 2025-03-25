from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta raíz apunta a index
    path('agregar/', views.agregar_maquina, name='agregar_maquina'),
    path('index/', views.index, name='index'),  # Ruta adicional para /index/
    path('lista_maquinas/', views.lista_maquinas, name='lista_maquinas'),
    path('editar/<int:pk>/', views.editar_maquina, name='editar_maquina'),
    path('eliminar/<int:pk>/', views.eliminar_maquina, name='eliminar_maquina'),
    path('complementos/', views.lista_complementos, name='lista_complementos'),
    path('maquinas-disponibles/', views.listar_maquinas_disponibles, name='listar_maquinas_disponibles'),
    path('operaciones-detalles/', views.listar_operaciones_detalles, name='listar_operaciones_detalles'),
    path('estadisticas-maquinas/', views.estadisticas_maquinas_estado, name='estadisticas_maquinas_estado'),
    path('tiempo-promedio-operacion/', views.tiempo_promedio_operacion, name='tiempo_promedio_operacion'),
    path('maquinas-por-kilometraje/', views.maquinas_por_kilometraje, name='maquinas_por_kilometraje'),
    # CRUD Maquina
    path('lista-maquinas/', views.lista_maquinas, name='lista_maquinas'),
    path('agregar/', views.agregar_maquina, name='agregar_maquina'),
    path('editar-maquina/<int:pk>/', views.editar_maquina, name='editar_maquina'),
    path('eliminar-maquina/<int:pk>/', views.eliminar_maquina, name='eliminar_maquina'),
    # CRUD Complemento
    path('complementos/', views.lista_complementos, name='lista_complementos'),
    path('agregar-complemento/', views.agregar_complemento, name='agregar_complemento'),
    path('editar-complemento/<int:pk>/', views.editar_complemento, name='editar_complemento'),
    path('eliminar-complemento/<int:pk>/', views.eliminar_complemento, name='eliminar_complemento'),
    # CRUD Operacion
    path('operaciones/', views.lista_operaciones, name='lista_operaciones'),
    path('agregar-operacion/', views.agregar_operacion, name='agregar_operacion'),
    path('editar-operacion/<int:pk>/', views.editar_operacion, name='editar_operacion'),
    path('eliminar-operacion/<int:pk>/', views.eliminar_operacion, name='eliminar_operacion'),
    # CRUD Trabajador
    path('trabajadores/', views.lista_trabajadores, name='lista_trabajadores'),
    path('agregar-trabajador/', views.agregar_trabajador, name='agregar_trabajador'),
    path('editar-trabajador/<int:pk>/', views.editar_trabajador, name='editar_trabajador'),
    path('eliminar-trabajador/<int:pk>/', views.eliminar_trabajador, name='eliminar_trabajador'),
    # Vistas adicionales
    path('maquinas-disponibles/', views.listar_maquinas_disponibles, name='listar_maquinas_disponibles'),
    path('operaciones-detalles/', views.listar_operaciones_detalles, name='listar_operaciones_detalles'),
    path('estadisticas-maquinas/', views.estadisticas_maquinas_estado, name='estadisticas_maquinas_estado'),
    path('tiempo-promedio-operacion/', views.tiempo_promedio_operacion, name='tiempo_promedio_operacion'),
    path('maquinas-por-kilometraje/', views.maquinas_por_kilometraje, name='maquinas_por_kilometraje'),
    # Nuevas rutas para login y registro
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/trabajador/', views.dashboard_trabajador, name='dashboard_trabajador'),
    path('dashboard/operador/', views.dashboard_operador, name='dashboard_operador'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
]