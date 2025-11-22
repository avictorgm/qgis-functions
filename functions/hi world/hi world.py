from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsExpression, QgsExpressionContext, QgsExpressionContextUtils

# Crear contexto de expresión (con el proyecto actual)
context = QgsExpressionContext()
context.appendScope(QgsExpressionContextUtils.globalScope())

# Definir la expresión
expr = QgsExpression("@user_full_name")

# Evaluarla
user_name = expr.evaluate(context)

# Mostrar en ventana emergente
QMessageBox.information(None, "Usuario actual", f"Usuario: {user_name}")