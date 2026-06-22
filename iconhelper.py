from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer


def create_tray_icon(svg_path, color_hex):
    with open(svg_path, "r") as f:
        svg_data = f.read()

    if '#000000' in svg_data:
        modified_svg = svg_data.replace('#000000', color_hex)
    else:
        modified_svg = svg_data.replace('<path', f'<path fill="{color_hex}"')

    renderer = QSvgRenderer(QByteArray(modified_svg.encode("utf-8")))

    pixmap = QPixmap(128, 128)
    # Bei PySide6 nutzen wir direkt den Enum-Wert für Transparenz
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)