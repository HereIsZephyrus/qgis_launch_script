

from qgis.core import (
    QgsVectorLayer,
    QgsMessageLog,
    Qgis
)


# Threshold for automatic spatial index creation
FEATURE_COUNT_THRESHOLD = 10000

# Track processed layers to avoid duplicate processing
_processed_layers = set()


def check_and_create_spatial_index(layer):
    """
    Check if a vector layer needs a spatial index and create it if needed.

    Args:
        layer: QgsMapLayer to check
    """
    # Only process vector layers
    if not isinstance(layer, QgsVectorLayer):
        return

    # Check if layer is valid
    if not layer.isValid():
        QgsMessageLog.logMessage(
            f"Layer '{layer.name()}' is not valid, skipping spatial index check",
            "Layer Monitor",
            Qgis.Warning
        )
        return

    # Get layer ID to track processed layers
    layer_id = layer.id()

    # Skip if already processed
    if layer_id in _processed_layers:
        return

    try:
        # Get feature count
        feature_count = layer.featureCount()

        QgsMessageLog.logMessage(
            f"Checking layer '{layer.name()}': {feature_count} features",
            "Layer Monitor",
            Qgis.Info
        )

        # Check if feature count exceeds threshold
        if feature_count > FEATURE_COUNT_THRESHOLD:
            # Check if spatial index already exists
            if layer.hasSpatialIndex():
                QgsMessageLog.logMessage(
                    f"Layer '{layer.name()}' already has a spatial index",
                    "Layer Monitor",
                    Qgis.Info
                )
            else:
                # Create spatial index
                QgsMessageLog.logMessage(
                    f"Creating spatial index for layer '{layer.name()}' ({feature_count} features)",
                    "Layer Monitor",
                    Qgis.Info
                )

                success = layer.createSpatialIndex()

                if success:
                    QgsMessageLog.logMessage(
                        f"Spatial index created successfully for layer '{layer.name()}'",
                        "Layer Monitor",
                        Qgis.Success
                    )
                else:
                    QgsMessageLog.logMessage(
                        f"Failed to create spatial index for layer '{layer.name()}'",
                        "Layer Monitor",
                        Qgis.Warning
                    )
        else:
            QgsMessageLog.logMessage(
                f"Layer '{layer.name()}' has {feature_count} features (threshold: {FEATURE_COUNT_THRESHOLD}), "
                "spatial index not needed",
                "Layer Monitor",
                Qgis.Info
            )

        # Mark as processed
        _processed_layers.add(layer_id)

    except Exception as e:
        QgsMessageLog.logMessage(
            f"Error processing layer '{layer.name()}': {str(e)}",
            "Layer Monitor",
            Qgis.Critical
        )


def on_layers_added(layers):
    """
    Callback function called when layers are added to the project.

    Args:
        layers: List of QgsMapLayer objects that were added
    """
    for layer in layers:
        check_and_create_spatial_index(layer)
