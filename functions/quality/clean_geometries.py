"""Detecta y corrige geometrías inválidas en la capa activa"""

from qgis.core import (QgsProject, QgsVectorLayer, QgsFeature, 
                       QgsGeometry, QgsWkbTypes, QgsMessageLog, Qgis)
import processing

def ejecutar(iface, params=None):
    """
    Valida y repara geometrías inválidas en la capa activa
    
    Args:
        iface: Interfaz de QGIS
        params: Parámetros opcionales
    
    Returns:
        dict: Estado y mensaje del resultado
    """
    capa = iface.activeLayer()
    
    if not capa or capa.type() != 0:
        return {
            "status": "warning",
            "mensaje": "Seleccione una capa vectorial para validar"
        }
    
    # Verificar que la capa es editable
    if capa.isEditable():
        return {
            "status": "warning",
            "mensaje": "La capa está en modo edición. Guarde o cancele los cambios primero."
        }
    
    try:
        # Contadores
        total_entidades = capa.featureCount()
        geometrias_invalidas = []
        geometrias_vacias = []
        geometrias_reparadas = 0
        
        # Analizar geometrías
        for entidad in capa.getFeatures():
            geom = entidad.geometry()
            
            if geom.isEmpty():
                geometrias_vacias.append(entidad.id())
            elif not geom.isValid():
                geometrias_invalidas.append(entidad.id())
        
        # Si no hay problemas
        if not geometrias_invalidas and not geometrias_vacias:
            return {
                "status": "ok",
                "mensaje": f"✓ Todas las {total_entidades} geometrías son válidas"
            }
        
        # Preparar mensaje de problemas encontrados
        problemas = []
        if geometrias_vacias:
            problemas.append(f"{len(geometrias_vacias)} geometrías vacías")
        if geometrias_invalidas:
            problemas.append(f"{len(geometrias_invalidas)} geometrías inválidas")
        
        # Intentar reparar
        capa.startEditing()
        
        # Reparar geometrías inválidas
        for fid in geometrias_invalidas:
            entidad = capa.getFeature(fid)
            geom = entidad.geometry()
            
            # Intentar reparación con makeValid
            geom_reparada = geom.makeValid()
            
            if geom_reparada and geom_reparada.isValid():
                capa.changeGeometry(fid, geom_reparada)
                geometrias_reparadas += 1
            else:
                # Intentar buffer(0) como alternativa
                geom_buffer = geom.buffer(0, 5)
                if geom_buffer and geom_buffer.isValid():
                    capa.changeGeometry(fid, geom_buffer)
                    geometrias_reparadas += 1
        
        # Eliminar geometrías vacías si el usuario lo desea
        if geometrias_vacias and params and params.get('eliminar_vacias', False):
            capa.deleteFeatures(geometrias_vacias)
            mensaje_vacias = f"\n• Eliminadas {len(geometrias_vacias)} entidades con geometrías vacías"
        else:
            mensaje_vacias = ""
        
        # Guardar cambios
        if capa.commitChanges():
            # Preparar resumen
            resumen = f"Problemas encontrados:\n"
            resumen += "\n".join(f"• {p}" for p in problemas)
            
            if geometrias_reparadas > 0:
                resumen += f"\n\n✓ Reparadas {geometrias_reparadas} geometrías"
            
            if geometrias_invalidas and geometrias_reparadas < len(geometrias_invalidas):
                no_reparadas = len(geometrias_invalidas) - geometrias_reparadas
                resumen += f"\n✗ No se pudieron reparar {no_reparadas} geometrías"
                resumen += f"\n\nIDs no reparados: {geometrias_invalidas[:10]}"
                if len(geometrias_invalidas) > 10:
                    resumen += "..."
            
            resumen += mensaje_vacias
            
            # Actualizar canvas
            iface.mapCanvas().refresh()
            
            return {
                "status": "ok" if geometrias_reparadas == len(geometrias_invalidas) else "warning",
                "mensaje": resumen
            }
        else:
            capa.rollBack()
            return {
                "status": "error",
                "mensaje": "Error al guardar los cambios. Se revirtieron las modificaciones."
            }
            
    except Exception as e:
        if capa.isEditable():
            capa.rollBack()
        
        return {
            "status": "error",
            "mensaje": f"Error al procesar geometrías: {str(e)}"
        }
