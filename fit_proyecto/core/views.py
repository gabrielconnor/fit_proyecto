# core/views.py (CORREGIDO)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Entrada, Corredor 
from django.db import IntegrityError # Añadimos esto para manejar errores de base de datos

# =========================================================================
# 1. LISTAR (READ) y CONTEXTO GLOBAL 
# =========================================================================

def entry_list(request):
    """
    Muestra la lista de entradas y provee la lista de corredores
    para el modal de Crear/Editar.
    """
    # Optimizamos la consulta para evitar múltiples viajes a la DB
    entries = Entrada.objects.all().select_related('corredor').order_by('-created_at')
    
    # 🟢 CORRECCIÓN CLAVE: Obtener todos los corredores para el <select> del modal.
    corredores = Corredor.objects.all()

    context = {
        'entradas': entries,
        'corredores': corredores,
        # 'error' se puede agregar aquí si una función POST (create/update) falló
    }
    
    # Renderizamos el único template unificado
    return render(request, 'entries/list.html', context)

# =========================================================================
# 2. CREAR (CREATE)
# =========================================================================

def entry_create(request):
    """
    Maneja la lógica POST del modal de creación.
    """
    if request.method == 'POST':
        try:
            corredor_id = request.POST['corredor']
            tipo = request.POST['tipo']
            monto_str = request.POST.get('monto') 
            factor_str = request.POST.get('factor') 

            corredor = get_object_or_404(Corredor, id=corredor_id)
            monto = int(monto_str) if monto_str else None
            factor = float(factor_str) if factor_str else None

            Entrada.objects.create(
                corredor=corredor,
                tipo=tipo,
                monto=monto,
                factor=factor,
                tipo_ingreso=True
            )
            # Redirigir al listado después de crear exitosamente
            return redirect('entry_list')
        
        except (ValueError, KeyError, IntegrityError) as e:

            error_msg = f"Error al crear: {e}. Inténtelo de nuevo."
            return redirect('entry_list') 

    # Si alguien intenta acceder por GET directamente, lo redirigimos a la lista
    return redirect('entry_list') 

# =========================================================================
# 3. ACTUALIZAR (UPDATE)
# =========================================================================

def entry_update(request, pk):
    """
    Maneja la lógica POST del modal de edición.
    """
    entry = get_object_or_404(Entrada, pk=pk)

    if request.method == 'POST':
        try:
            corredor_id = request.POST['corredor']
            entry.tipo = request.POST['tipo']
            monto_str = request.POST.get('monto') 
            factor_str = request.POST.get('factor') 

            entry.corredor = get_object_or_404(Corredor, id=corredor_id)
            entry.monto = int(monto_str) if monto_str else None
            entry.factor = float(factor_str) if factor_str else None
            
            entry.save() 
            
            # Redirigir al listado después de actualizar exitosamente
            return redirect('entry_list')
        
        except (ValueError, KeyError, IntegrityError) as e:
            # Si hay un error, redirigimos al listado con un mensaje
            error_msg = f"Error al actualizar la entrada #{pk}: {e}. Inténtelo de nuevo."
            return redirect('entry_list')

    # Si alguien intenta acceder por GET directamente, lo redirigimos a la lista
    return redirect('entry_list')


# =========================================================================
# 4. ELIMINAR (DELETE)
# =========================================================================

def entry_delete(request, pk):
    """
    Maneja la lógica POST del modal de eliminación.
    """
    entry = get_object_or_404(Entrada, pk=pk)

    if request.method == 'POST':
        entry.delete()
        # Redirigir al listado después de borrar
        return redirect('entry_list')
        
    # Si alguien intenta acceder por GET directamente, lo redirigimos a la lista
    return redirect('entry_list')