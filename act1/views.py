from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from functools import wraps
from .models import Maquina, Complemento, Operacion, Trabajador, Rol
from .forms import MaquinaForm, ComplementoForm, OperacionForm, TrabajadorForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Constantes para roles
ROLES = {
    'ADMIN': 'Administrador',
    'OPERADOR': 'Operador',
    'TRABAJADOR': 'Trabajador'
}

# Decorador personalizado para administradores
def admin_required(view_func):
    """Restringe el acceso a vistas solo para usuarios con rol Administrador."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        trabajador = getattr(request.user, 'trabajador', None)
        if not trabajador or trabajador.rol.nombre != ROLES['ADMIN']:
            messages.error(request, 'No tienes permisos para realizar esta acción.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Vista para el index
def index(request):
    """Renderiza la página principal del sistema sin requerir autenticación."""
    return render(request, 'index.html')

# --- Vistas de autenticación ---
def login_view(request):
    """Maneja el inicio de sesión de los usuarios con autenticación."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso!')
            return redirect('dashboard')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html')

def logout_view(request):
    """Cierra lasessions del usuario y redirige al login."""
    logout(request)
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('index')

def registro_view(request):
    """Registra nuevos usuarios como trabajadores sin PIN ni selección de rol."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            rol_trabajador, _ = Rol.objects.get_or_create(
                nombre=ROLES['TRABAJADOR'],
                defaults={'descripcion': 'Rol básico para trabajadores'}
            )
            Trabajador.objects.create(
                usuario=user,
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                cedula=form.cleaned_data['cedula'],
                telefono=form.cleaned_data['telefono'],
                rol=rol_trabajador
            )
            login(request, user)  # Inicia sesión automáticamente
            messages.success(request, '¡Registro exitoso! Bienvenido(a).')
            return redirect('dashboard')
        else:
            print(form.errors)  # Depurar errores en la consola
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

# --- Dashboard ---
@login_required
def dashboard(request):
    """Redirige al dashboard correspondiente según el rol del usuario."""
    trabajador = getattr(request.user, 'trabajador', None)
    if not trabajador or not trabajador.rol:
        messages.error(request, 'No se encontró un rol asociado a tu cuenta.')
        return redirect('index')
    
    if trabajador.rol.nombre == ROLES['TRABAJADOR']:
        return redirect('dashboard_trabajador')
    elif trabajador.rol.nombre == ROLES['OPERADOR']:
        return redirect('dashboard_operador')
    elif trabajador.rol.nombre == ROLES['ADMIN']:
        return redirect('dashboard_admin')
    messages.error(request, 'Rol no reconocido.')
    return redirect('index')

@login_required
def dashboard_trabajador(request):
    """Dashboard para usuarios con rol Trabajador con operaciones personales."""
    trabajador = getattr(request.user, 'trabajador', None)
    if not trabajador or trabajador.rol.nombre != ROLES['TRABAJADOR']:
        messages.error(request, 'No tienes permisos para acceder a este dashboard.')
        return redirect('dashboard')

    maquinas = Maquina.objects.all()
    operaciones = Operacion.objects.filter(trabajador=trabajador).select_related('maquina')
    
    context = {
        'maquinas': maquinas,
        'operaciones': operaciones,
        'trabajador': trabajador
    }
    return render(request, 'dashboard_trabajador.html', context)

@login_required
def dashboard_operador(request):
    """Dashboard para Operadores con estadísticas de máquinas y operaciones."""
    trabajador = getattr(request.user, 'trabajador', None)
    if not trabajador or trabajador.rol.nombre != ROLES['OPERADOR']:
        messages.error(request, 'No tienes permisos para acceder a este dashboard.')
        return redirect('dashboard')

    tiempo_promedio = Operacion.objects.values('tipo_operacion').annotate(tiempo_promedio=Avg('tiempo_operacion'))
    maquinas_por_km = Maquina.objects.all().order_by('-kilometraje')
    estadisticas_estado = Maquina.objects.values('estado_maquina').annotate(cantidad=Count('id'))

    context = {
        'tiempo_promedio': tiempo_promedio,
        'maquinas_por_km': maquinas_por_km,
        'estadisticas_estado': estadisticas_estado,
        'trabajador': trabajador
    }
    return render(request, 'dashboard_operador.html', context)

@login_required
@admin_required
def dashboard_admin(request):
    """Dashboard para Administradores con acceso completo a datos."""
    trabajador = request.user.trabajador
    maquinas = Maquina.objects.all()
    complementos = Complemento.objects.all()
    operaciones = Operacion.objects.select_related('maquina', 'trabajador').all()
    trabajadores = Trabajador.objects.select_related('rol').all()

    # Lista para almacenar operaciones con tiempo formateado
    operaciones_con_tiempo = []
    for operacion in operaciones:
        if operacion.tiempo_operacion:
            horas = int(operacion.tiempo_operacion)  # Parte entera (horas)
            minutos = int((operacion.tiempo_operacion - horas) * 60)  # Parte decimal convertida a minutos
            tiempo_formateado = f"{horas}h {minutos}m"
        else:
            tiempo_formateado = "No calculado"
        operaciones_con_tiempo.append({
            'operacion': operacion,
            'tiempo_formateado': tiempo_formateado
        })

    context = {
        'maquinas': maquinas,
        'complementos': complementos,
        'operaciones_con_tiempo': operaciones_con_tiempo,  # Nueva clave con tiempo formateado
        'trabajadores': trabajadores,
        'trabajador': trabajador
    }
    return render(request, 'dashboard_admin.html', context)

# --- CRUD para Maquina ---
@login_required
def lista_maquinas(request):
    """Lista todas las máquinas con paginación."""
    maquinas = Maquina.objects.all()
    paginator = Paginator(maquinas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'lista_maquinas.html', {'page_obj': page_obj})

@login_required
@admin_required
def agregar_maquina(request):
    """Agrega una nueva máquina al sistema."""
    if request.method == 'POST':
        form = MaquinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Máquina agregada correctamente.')
            return redirect('lista_maquinas')
        messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = MaquinaForm()
    return render(request, 'agregar_maquina.html', {'form': form})

@login_required
@admin_required
def editar_maquina(request, pk):
    """Edita una máquina existente."""
    maquina = get_object_or_404(Maquina, pk=pk)
    if request.method == 'POST':
        form = MaquinaForm(request.POST, instance=maquina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Máquina actualizada correctamente.')
            return redirect('lista_maquinas')
        messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = MaquinaForm(instance=maquina)
    return render(request, 'editar_maquina.html', {'form': form})

@login_required
@admin_required
def eliminar_maquina(request, pk):
    """Elimina una máquina del sistema."""
    maquina = get_object_or_404(Maquina, pk=pk)
    if request.method == 'POST':
        maquina.delete()
        messages.success(request, 'Máquina eliminada correctamente.')
        return redirect('lista_maquinas')
    return render(request, 'eliminar_maquina.html', {'maquina': maquina})

# --- CRUD para Complemento ---
@login_required
def lista_complementos(request):
    """Lista todos los complementos con paginación."""
    complementos = Complemento.objects.all()
    paginator = Paginator(complementos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'lista_complementos.html', {'page_obj': page_obj})

@login_required
@admin_required
def agregar_complemento(request):
    """Agrega un nuevo complemento al sistema."""
    if request.method == 'POST':
        form = ComplementoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complemento agregado correctamente.')
            return redirect('lista_complementos')
        messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ComplementoForm()
    return render(request, 'agregar_complemento.html', {'form': form})

@login_required
@admin_required
def editar_complemento(request, pk):
    """Edita un complemento existente."""
    complemento = get_object_or_404(Complemento, pk=pk)
    if request.method == 'POST':
        form = ComplementoForm(request.POST, instance=complemento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complemento actualizado correctamente.')
            return redirect('lista_complementos')
        messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ComplementoForm(instance=complemento)
    return render(request, 'editar_complemento.html', {'form': form})

@login_required
@admin_required
def eliminar_complemento(request, pk):
    """Elimina un complemento del sistema."""
    complemento = get_object_or_404(Complemento, pk=pk)
    if request.method == 'POST':
        complemento.delete()
        messages.success(request, 'Complemento eliminado correctamente.')
        return redirect('lista_complementos')
    return render(request, 'eliminar_complemento.html', {'complemento': complemento})

# --- CRUD para Operacion ---
@login_required
def lista_operaciones(request):
    """Lista todas las operaciones con paginación."""
    operaciones = Operacion.objects.select_related('maquina', 'trabajador').all()
    paginator = Paginator(operaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'lista_operaciones.html', {'page_obj': page_obj})

@login_required
def agregar_operacion(request):
    """Agrega una nueva operación al sistema."""
    if request.method == 'POST':
        form = OperacionForm(request.POST)
        if form.is_valid():
            operacion = form.save(commit=False)
            fecha_entrada = form.cleaned_data['fecha_entrada']
            fecha_salida = form.cleaned_data['fecha_salida']
            if fecha_entrada and fecha_salida and fecha_salida > fecha_entrada:
                diferencia = fecha_salida - fecha_entrada
                operacion.tiempo_operacion = diferencia.total_seconds() / 3600  # Guardar en horas decimales
            else:
                operacion.tiempo_operacion = None
            operacion.save()
            messages.success(request, 'Operación agregada correctamente.')
            return redirect('lista_operaciones')
        messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = OperacionForm()
    return render(request, 'agregar_operacion.html', {'form': form})

@login_required
@admin_required
def editar_operacion(request, pk):
    """Edita una operación existente."""
    operacion = get_object_or_404(Operacion, pk=pk)
    if request.method == 'POST':
        form = OperacionForm(request.POST, instance=operacion)
        if form.is_valid():
            operacion = form.save(commit=False)
            fecha_entrada = form.cleaned_data['fecha_entrada']
            fecha_salida = form.cleaned_data['fecha_salida']
            if fecha_entrada and fecha_salida and fecha_salida > fecha_entrada:
                diferencia = fecha_salida - fecha_entrada
                operacion.tiempo_operacion = diferencia.total_seconds() / 3600  # Guardar en horas decimales
            else:
                operacion.tiempo_operacion = None
            operacion.save()
            messages.success(request, 'Operación actualizada correctamente.')
            return redirect('lista_operaciones')
        messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = OperacionForm(instance=operacion)
    return render(request, 'editar_operacion.html', {'form': form})

@login_required
@admin_required
def eliminar_operacion(request, pk):
    """Elimina una operación del sistema."""
    operacion = get_object_or_404(Operacion, pk=pk)
    if request.method == 'POST':
        operacion.delete()
        messages.success(request, 'Operación eliminada correctamente.')
        return redirect('lista_operaciones')
    return render(request, 'eliminar_operacion.html', {'operacion': operacion})

# --- CRUD para Trabajador ---
@login_required
@admin_required
def lista_trabajadores(request):
    """Lista todos los trabajadores con paginación."""
    trabajadores = Trabajador.objects.select_related('rol').all()
    paginator = Paginator(trabajadores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'lista_trabajadores.html', {'page_obj': page_obj})

@login_required
@admin_required
def agregar_trabajador(request):
    """Agrega un nuevo trabajador al sistema con rol asignado."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            rol_trabajador, _ = Rol.objects.get_or_create(
                nombre=ROLES['TRABAJADOR'],
                defaults={'descripcion': 'Rol básico para trabajadores'}
            )
            Trabajador.objects.create(
                usuario=user,
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                cedula=form.cleaned_data['cedula'],
                telefono=form.cleaned_data['telefono'],
                rol=rol_trabajador
            )
            messages.success(request, 'Trabajador agregado correctamente.')
            return redirect('dashboard_admin')  # Redirige al dashboard en lugar de lista_trabajadores
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            # Imprimir errores para depuración
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'agregar_trabajador.html', {'form': form})

@login_required
@admin_required
def editar_trabajador(request, pk):
    """Edita un trabajador existente, incluyendo la asignación de PIN y contraseña."""
    trabajador = get_object_or_404(Trabajador, pk=pk)
    
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, instance=trabajador)
        if form.is_valid():
            trabajador = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                trabajador.usuario.set_password(password)
                trabajador.usuario.save()
            trabajador.save()
            messages.success(request, 'Trabajador actualizado correctamente.')
            return redirect('lista_trabajadores')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = TrabajadorForm(instance=trabajador)
    return render(request, 'editar_trabajador.html', {'form': form})

@login_required
@admin_required
def eliminar_trabajador(request, pk):
    """Elimina un trabajador del sistema."""
    trabajador = get_object_or_404(Trabajador, pk=pk)
    if request.method == 'POST':
        trabajador.delete()
        messages.success(request, 'Trabajador eliminado correctamente.')
        return redirect('lista_trabajadores')
    return render(request, 'eliminar_trabajador.html', {'trabajador': trabajador})

# --- Vistas adicionales ---
@login_required
def listar_maquinas_disponibles(request):
    """Lista máquinas disponibles con paginación."""
    maquinas = Maquina.objects.filter(disponibilidad='SÍ')
    paginator = Paginator(maquinas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_maquinas_disponibles.html', {'page_obj': page_obj})

@login_required
def listar_operaciones_detalles(request):
    """Lista operaciones con detalles y paginación."""
    operaciones = Operacion.objects.select_related('maquina', 'trabajador').all()
    paginator = Paginator(operaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_operaciones_detalles.html', {'page_obj': page_obj})

@login_required
def estadisticas_maquinas_estado(request):
    """Muestra estadísticas de máquinas por estado para Operadores y Administradores."""
    trabajador = getattr(request.user, 'trabajador', None)
    if not trabajador or trabajador.rol.nombre not in [ROLES['OPERADOR'], ROLES['ADMIN']]:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('dashboard')

    estadisticas = Maquina.objects.values('estado_maquina').annotate(cantidad=Count('id'))
    return render(request, 'estadisticas_maquinas_estado.html', {'estadisticas': estadisticas})

@login_required
def tiempo_promedio_operacion(request):
    """Muestra el tiempo promedio de operaciones para Operadores y Administradores."""
    trabajador = getattr(request.user, 'trabajador', None)
    if not trabajador or trabajador.rol.nombre not in [ROLES['OPERADOR'], ROLES['ADMIN']]:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('dashboard')

    promedios = Operacion.objects.values('tipo_operacion').annotate(tiempo_promedio=Avg('tiempo_operacion'))
    return render(request, 'tiempo_promedio_operacion.html', {'promedios': promedios})

@login_required
def maquinas_por_kilometraje(request):
    """Lista máquinas ordenadas por kilometraje con paginación."""
    trabajador = getattr(request.user, 'trabajador', None)
    if not trabajador or trabajador.rol.nombre not in [ROLES['OPERADOR'], ROLES['ADMIN']]:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('dashboard')

    maquinas = Maquina.objects.all().order_by('-kilometraje')
    paginator = Paginator(maquinas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'maquinas_por_kilometraje.html', {'page_obj': page_obj})