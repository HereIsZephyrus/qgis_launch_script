import os
from qgis.PyQt.QtCore import QUrl, Qt
from qgis.PyQt.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from qgis.core import QgsMessageLog, Qgis

# Initialize variables
QWebEngineView = None
QWebView = None
WEB_ENGINE_AVAILABLE = None

# Try to import QWebEngineView (QGIS 3.4+)
try:
    from qgis.PyQt.QtWebEngineWidgets import QWebEngineView
    WEB_ENGINE_AVAILABLE = True
except ImportError:
    # Fallback to QWebView for older QGIS versions
    try:
        from qgis.PyQt.QtWebKitWidgets import QWebView
        WEB_ENGINE_AVAILABLE = False
    except ImportError:
        QgsMessageLog.logMessage(
            "WebView components not available. Welcome page cannot be displayed.",
            "launch script",
            Qgis.Warning
        )


def get_welcome_url():
    """
    Get the welcome page URL from environment variable or use default.

    Returns:
        str: URL to display in welcome page
    """
    default_url = "https://news.google.com"
    url = os.environ.get("QGIS_WELCOME_URL", default_url)
    return url


class WelcomeDialog(QDockWidget):
    """
    Custom welcome dock widget that displays web content in the center of QGIS.
    """

    def __init__(self, parent=None, url=None):
        """
        Initialize the welcome dock widget.

        Args:
            parent: Parent widget (optional, should be QGIS main window)
            url: URL to display (optional, defaults to Google News)
        """
        super().__init__("Welcome Page", parent)

        if WEB_ENGINE_AVAILABLE is None:
            QgsMessageLog.logMessage(
                "Cannot create welcome widget: WebView components not available",
                "launch script",
                Qgis.Critical
            )
            return

        # Set dock widget properties - allow it to be in the center area
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setMinimumSize(400, 300)

        # Create main widget container
        main_widget = QWidget()
        self.setWidget(main_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_widget.setLayout(main_layout)

        # Create web view
        if WEB_ENGINE_AVAILABLE:
            self.web_view = QWebEngineView()
        elif WEB_ENGINE_AVAILABLE is False and QWebView is not None:
            self.web_view = QWebView()
        else:
            # Fallback: show a label
            label = QLabel("Web view not available")
            label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(label)
            return

        # Load URL
        display_url = url if url else get_welcome_url()
        self.web_view.setUrl(QUrl(display_url))

        main_layout.addWidget(self.web_view)

        # Log action
        QgsMessageLog.logMessage(
            f"Welcome page opened: {display_url}",
            "launch script",
            Qgis.Info
        )
