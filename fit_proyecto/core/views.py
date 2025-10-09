from django.shortcuts import render, redirect, get_object_or_404
from .models import Entrada, Corredor 
from django.db import IntegrityError 

# =========================================================================
# 1. LISTAR (READ) y CONTEXTO GLOBAL 
# =========================================================================

def entry_list(request):
    entries = Entrada.objects.all().select_related('corredor').order_by('-created_at')
    corredores = Corredor.objects.all()

    context = {
        'entradas': entries,
        'corredores': corredores,
    }
    
    return render(request, 'entries/list.html', context)

# =========================================================================
# 2. CREAR (CREATE)
# =========================================================================

def entry_create(request):
    if request.method == 'POST':
        try:
            corredor_id = request.POST['corredor']
            tipo = request.POST['tipo']
            divisa = request.POST['divisa']  # <--- NUEVO
            monto_str = request.POST.get('monto') 
            factor_str = request.POST.get('factor') 

            corredor = get_object_or_404(Corredor, id=corredor_id)
            monto = int(monto_str) if monto_str else None
            factor = float(factor_str) if factor_str else None

            Entrada.objects.create(
                corredor=corredor,
                tipo=tipo,
                divisa=divisa,  # <--- NUEVO
                monto=monto,
                factor=factor,
                tipo_ingreso=True
            )
            return redirect('entry_list')
        
        except (ValueError, KeyError, IntegrityError) as e:
            # error_msg = f"Error al crear: {e}. Inténtelo de nuevo." # Dejamos la redirección simple sin pasar mensaje
            return redirect('entry_list') 

    return redirect('entry_list') 

# =========================================================================
# 3. ACTUALIZAR (UPDATE)
# =========================================================================

def entry_update(request, pk):
    entry = get_object_or_404(Entrada, pk=pk)

    if request.method == 'POST':
        try:
            corredor_id = request.POST['corredor']
            entry.tipo = request.POST['tipo']
            entry.divisa = request.POST['divisa'] # <--- NUEVO
            monto_str = request.POST.get('monto') 
            factor_str = request.POST.get('factor') 

            entry.corredor = get_object_or_404(Corredor, id=corredor_id)
            entry.monto = int(monto_str) if monto_str else None
            entry.factor = float(factor_str) if factor_str else None
            
            entry.save() 
            
            return redirect('entry_list')
        
        except (ValueError, KeyError, IntegrityError) as e:
            # error_msg = f"Error al actualizar la entrada #{pk}: {e}. Inténtelo de nuevo." # Dejamos la redirección simple sin pasar mensaje
            return redirect('entry_list')

    return redirect('entry_list')


# =========================================================================
# 4. ELIMINAR (DELETE)
# =========================================================================

def entry_delete(request, pk):
    entry = get_object_or_404(Entrada, pk=pk)

    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list')
        
    return redirect('entry_list')