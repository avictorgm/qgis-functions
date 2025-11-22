"""Categoriza una capa vectorial por valores únicos de un campo"""

from qgis.core import (QgsProject, QgsCategorizedSymbolRenderer,
                       QgsSymbol, QgsRendererCategory, QgsGraduatedSymbolRenderer,
                       QgsClassificationRange, QgsGradientColorRamp)
from qgis.PyQt.QtGui import QColor
import random

def ejecutar(iface, params=None):
    """
    Aplica simbología categorizada a la capa activa
    
    Args:
        iface: Interfaz de QGIS
        params: Diccionario con 'campo' para categorizar
    
    Returns:
        dict: Estado y mensaje del resultado
    """
    capa = iface.activeLayer()
    
    # Verificar que hay una capa activa
    if not capa:
        return {
            "status": "warning",
            "mensaje": "Seleccione una capa vectorial para categorizar"
        }
    
    # Verificar que es vectorial
    if capa.type() != 0:  # 0 = Vector Layer
        return {
            "status": "error",
            "mensaje": "La capa activa debe ser vectorial"
        }
    
    try:
        # Obtener campo para categorizar
        if params and 'campo' in params:
            campo = params['campo']
        else:
            # Usar el primer campo de texto si no se especifica
            campos_texto = [field.name() for field in capa.fields() 
                          if field.type() in [10, 7]]  # String o String List
            if not campos_texto:
                return {
                    "status": "error",
                    "mensaje": "La capa no tiene campos de texto para categorizar"
                }
            campo = campos_texto[0]
        
        # Verificar que el campo existe
        if campo not in [field.name() for field in capa.fields()]:
            return {
                "status": "error",
                "mensaje": f"El campo '{campo}' no existe en la capa"
            }
        
        # Obtener valores únicos
        valores_unicos = capa.uniqueValues(capa.fields().indexOf(campo))
        
        if len(valores_unicos) > 50:
            return {
                "status": "warning",
                "mensaje": f"Demasiadas categorías ({len(valores_unicos)}). Máximo recomendado: 50"
            }
        
        # Crear categorías con colores aleatorios
        categorias = []
        for valor in sorted(valores_unicos):
            # Generar color aleatorio pero visible
            color = QColor(
                random.randint(50, 200),
                random.randint(50, 200),
                random.randint(50, 200)
            )
            
            # Crear símbolo según el tipo de geometría
            simbolo = QgsSymbol.defaultSymbol(capa.geometryType())
            simbolo.setColor(color)
            
            # Manejar valores nulos
            etiqueta = str(valor) if valor is not None else "Sin valor"
            
            # Crear categoría
            categoria = QgsRendererCategory(valor, simbolo, etiqueta)
            categorias.append(categoria)
        
        # Crear y aplicar el renderer
        renderer = QgsCategorizedSymbolRenderer(campo, categorias)
        capa.setRenderer(renderer)
        
        # Refrescar la capa
        capa.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(capa.id())
        
        return {
            "status": "ok",
            "mensaje": f"Capa categorizada por '{campo}' ({len(categorias)} categorías)"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "mensaje": f"Error al categorizar: {str(e)}"
        }
