from qgis.core import QgsProject, QgsMessageLog, Qgis
from .utils import check_and_create_spatial_index, on_layers_added, _processed_layers


def initialize_monitor():
    """
    Initialize the layer monitor by connecting to QGIS project signals.

    This function should be called from startup.py to start monitoring layers.
    """
    try:
        # Connect to the layersAdded signal
        project = QgsProject.instance()
        project.layersAdded.connect(on_layers_added)

        # Process any existing layers in the project
        existing_layers = project.mapLayers().values()
        for layer in existing_layers:
            check_and_create_spatial_index(layer)

        QgsMessageLog.logMessage(
            "Layer monitor initialized successfully",
            "Layer Monitor",
            Qgis.Success
        )

    except Exception as e:
        QgsMessageLog.logMessage(
            f"Error initializing layer monitor: {str(e)}",
            "Layer Monitor",
            Qgis.Critical
        )


def cleanup_monitor():
    """
    Cleanup function to disconnect signals and clear processed layers cache.

    This can be called when the module is unloaded.
    """
    try:
        project = QgsProject.instance()
        project.layersAdded.disconnect(on_layers_added)

        # Clear processed layers cache
        _processed_layers.clear()

        QgsMessageLog.logMessage(
            "Layer monitor cleaned up",
            "Layer Monitor",
            Qgis.Info
        )
    except Exception as e:
        QgsMessageLog.logMessage(
            f"Error cleaning up layer monitor: {str(e)}",
            "Layer Monitor",
            Qgis.Warning
        )

