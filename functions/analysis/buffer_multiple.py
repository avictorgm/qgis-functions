"""Crea buffers múltiples con distancias incrementales"""

from qgis.core import (QgsProject, QgsVectorLayer, QgsFeature, 
                       QgsGeometry, QgsField, QgsFields)
from qgis.PyQt.QtCore import QVariant
import processing

def ejecutar(iface, params=None):
    """
    Crea múltiples anillos de buffer alrededor de las entidades seleccionadas
    
    Args:
        iface: Interfaz de QGIS
        params: Diccionario con distancias y número de anillos
    
    Returns:
        dict: Estado y mensaje del resultado
    """
    capa = iface.activeLayer()
    
    if not capa or capa.type() != 0:
        return {
            "status": "warning",
            "mensaje": "Seleccione una capa vectorial"
        }
    
    # Obtener entidades seleccionadas o todas
    if capa.selectedFeatureCount() > 0:
        entidades = capa.selectedFeatures()
        mensaje_seleccion = f"{capa.selectedFeatureCount()} entidades seleccionadas"
    else:
        entidades = list(capa.getFeatures())
        mensaje_seleccion = f"todas las {capa.featureCount()} entidades"
    
    if not entidades:
        return {
            "status": "error",
            "mensaje": "La capa no tiene entidades"
        }
    
    try:
        # Parámetros por defecto
        if params is None:
            params = {}
        
        distancia_inicial = params.get('distancia_inicial', 100)
        incremento = params.get('incremento', 100)
        num_anillos = params.get('num_anillos', 3)
        
        # Crear capa de salida
        crs = capa.crs().authid()
        nombre_capa = f"Buffers_{capa.name()}"
        
        # Definir campos
        campos = QgsFields()
        campos.append(QgsField("id_original", QVariant.Int))
        campos.append(QgsField("distancia", QVariant.Double))
        campos.append(QgsField("anillo", QVariant.Int))
        
        # Crear capa en memoria
        capa_buffer = QgsVectorLayer(
            f"Polygon?crs={crs}",
            nombre_capa,
            "memory"
        )
        
        proveedor = capa_buffer.dataProvider()
        proveedor.addAttributes(campos)
        capa_buffer.updateFields()
        
        nuevas_entidades = []
        
        # Crear buffers para cada entidad y cada distancia
        for entidad in entidades:
            geom = entidad.geometry()
            
            for i in range(num_anillos):
                distancia = distancia_inicial + (incremento * i)
                
                # Crear buffer
                buffer = geom.buffer(distancia, 10)
                
                # Si no es el primer anillo, crear anillo (donut)
                if i > 0:
                    distancia_interior = distancia_inicial + (incremento * (i - 1))
                    buffer_interior = geom.buffer(distancia_interior, 10)
                    buffer = buffer.difference(buffer_interior)
                
                # Crear nueva entidad
                nueva_entidad = QgsFeature()
                nueva_entidad.setGeometry(buffer)
                nueva_entidad.setAttributes([
                    entidad.id(),
                    distancia,
                    i + 1
                ])
                nuevas_entidades.append(nueva_entidad)
        
        # Agregar entidades a la capa
        proveedor.addFeatures(nuevas_entidades)
        
        # Agregar la capa al proyecto
        QgsProject.instance().addMapLayer(capa_buffer)
        
        # Aplicar estilo degradado
        from qgis.core import QgsGraduatedSymbolRenderer, QgsClassificationRange
        from qgis.PyQt.QtGui import QColor
        
        rangos = []
        for i in range(num_anillos):
            simbolo = QgsSymbol.defaultSymbol(capa_buffer.geometryType())
            # Color degradado de oscuro a claro
            intensidad = 200 - (i * 50)
            color = QColor(intensidad, intensidad, 255, 150)
            simbolo.setColor(color)
            
            rango = QgsClassificationRange(
                i + 0.5,
                i + 1.5,
                simbolo,
                f"Anillo {i + 1}"
            )
            rangos.append(rango)
        
        renderer = QgsGraduatedSymbolRenderer("anillo", rangos)
        capa_buffer.setRenderer(renderer)
        capa_buffer.triggerRepaint()
        
        return {
            "status": "ok",
            "mensaje": f"Creados {num_anillos} anillos de buffer para {mensaje_seleccion}\n" +
                      f"Distancias: {distancia_inicial} a {distancia_inicial + (incremento * (num_anillos - 1))} metros"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "mensaje": f"Error creando buffers: {str(e)}"
        }
