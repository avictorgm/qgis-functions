"""Print the current map using the first available layout"""

from qgis.core import QgsProject, QgsLayoutExporter
import os
from datetime import datetime

def execute(iface, params=None):
    """
    Export the current map to PDF using the first available layout
    
    Args:
        iface: QGIS interface
        params: Optional parameters (layout_name, output_folder, dpi)
    
    Returns:
        dict: Status and result message
    """
    if params is None:
        params = {}
    
    project = QgsProject.instance()
    manager = project.layoutManager()
    
    # Get available layouts
    layouts = manager.layouts()
    if not layouts:
        return {
            "status": "error",
            "message": "No layouts available in the project"
        }
    
    # Select layout
    layout_name = params.get('layout_name')
    if layout_name:
        layout = manager.layoutByName(layout_name)
        if not layout:
            return {
                "status": "error",
                "message": f"Layout not found: {layout_name}"
            }
    else:
        layout = layouts[0]
    
    try:
        # Configure exporter
        exporter = QgsLayoutExporter(layout)
        
        # Configure output path
        output_folder = params.get('output_folder', os.path.expanduser("~/Desktop"))
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"map_{layout.name()}_{timestamp}.pdf"
        output_path = os.path.join(output_folder, filename)
        
        # Configure export settings
        settings = QgsLayoutExporter.PdfExportSettings()
        settings.dpi = params.get('dpi', 300)
        settings.exportMetadata = True
        settings.simplifyGeometries = True
        
        # Export
        result = exporter.exportToPdf(output_path, settings)
        
        if result == QgsLayoutExporter.Success:
            return {
                "status": "ok",
                "message": f"Map successfully exported to:\n{output_path}",
                "file": output_path
            }
        else:
            errors = {
                QgsLayoutExporter.MemoryError: "Memory error",
                QgsLayoutExporter.FileError: "File error",
                QgsLayoutExporter.PrintError: "Print error",
                QgsLayoutExporter.SvgLayerError: "SVG layer error",
                QgsLayoutExporter.Canceled: "Export canceled"
            }
            error_message = errors.get(result, "Unknown error")
            return {
                "status": "error",
                "message": f"Export error: {error_message}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error exporting map: {str(e)}"
        }
