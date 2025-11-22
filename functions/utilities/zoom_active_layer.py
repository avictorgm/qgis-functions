"""Zoom to the extent of the active layer"""

def execute(iface):
    """
    Zoom to the full extent of the active layer
    
    Args:
        iface: QGIS interface
    
    Returns:
        dict: Status and result message
    """
    layer = iface.activeLayer()
    
    if not layer:
        return {
            "status": "warning",
            "message": "No active layer selected"
        }
    
    try:
        canvas = iface.mapCanvas()
        extent = layer.extent()
        
        # Check that extent is valid
        if extent.isEmpty():
            return {
                "status": "error",
                "message": f"Layer '{layer.name()}' has no valid extent"
            }
        
        # Apply zoom
        canvas.setExtent(extent)
        canvas.refresh()
        
        return {
            "status": "ok",
            "message": f"Zoomed to layer: {layer.name()}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error zooming: {str(e)}"
        }
