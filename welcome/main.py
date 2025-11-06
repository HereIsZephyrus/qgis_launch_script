from qgis.core import QgsMessageLog, Qgis
from qgis.PyQt.QtCore import Qt
from .welcome_dialog import WelcomeDialog, WEB_ENGINE_AVAILABLE


def initialize_welcome(url=None, show_on_startup=True, in_center=True):
    """
    Initialize and show the welcome page as a dock widget in QGIS main window.

    This function should be called from startup.py to display the welcome page
    when QGIS starts. The widget will be placed in the center area, potentially
    tabified with existing widgets like "Project Templates".

    Args:
        url: URL to display (optional, defaults to Google News)
        show_on_startup: Whether to show the dock widget immediately (default: True)
        in_center: Whether to place in center area as tabbed (default: True)
    """
    if WEB_ENGINE_AVAILABLE is None:
        QgsMessageLog.logMessage(
            "Welcome module cannot be initialized: WebView components not available",
            "launch script",
            Qgis.Warning
        )
        return None

    try:
        # Get QGIS main window
        main_window = None

        # Try to get the main window from QGIS iface
        try:
            from qgis.utils import iface
            if iface:
                main_window = iface.mainWindow()
        except Exception:
            pass

        if not main_window:
            QgsMessageLog.logMessage(
                "Cannot initialize welcome module: QGIS main window not available",
                "launch script",
                Qgis.Warning
            )
            return None

        # Create dock widget
        dock_widget = WelcomeDialog(main_window, url)

        if in_center:
            # Try to tabify with existing central dock widgets
            # Find existing dock widgets in the main window
            existing_docks = main_window.findChildren(dock_widget.__class__.__bases__[0])
            center_dock = None
            
            # Look for common QGIS dock widgets that might be in the center
            for dock in existing_docks:
                dock_name = dock.windowTitle().lower()
                # Try to find browser panel or other central widgets
                if any(name in dock_name for name in ['browser', 'template', 'project']):
                    center_dock = dock
                    break
            
            if center_dock:
                # Tabify with the found dock widget
                main_window.tabifyDockWidget(center_dock, dock_widget)
                QgsMessageLog.logMessage(
                    f"Welcome widget tabified with existing dock: {center_dock.windowTitle()}",
                    "launch script",
                    Qgis.Info
                )
            else:
                # No suitable dock found, add to right area
                main_window.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
                QgsMessageLog.logMessage(
                    "Welcome widget added to right area (no center dock found)",
                    "launch script",
                    Qgis.Info
                )
        else:
            # Add to right dock area
            main_window.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        if show_on_startup:
            dock_widget.show()
            dock_widget.raise_()  # Bring to front if tabified
        else:
            dock_widget.hide()

        QgsMessageLog.logMessage(
            "Welcome module initialized successfully as dock widget",
            "launch script",
            Qgis.Success
        )

        return dock_widget
    except Exception as e:
        QgsMessageLog.logMessage(
            f"Error initializing welcome module: {str(e)}",
            "launch script",
            Qgis.Critical
        )
        return None

