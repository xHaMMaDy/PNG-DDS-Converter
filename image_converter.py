"""
Advanced Interactive PNG <-> DDS Image Converter
PySide6 Modern Black & White Theme with Custom Title Bar
"""

import os
import sys
import struct
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QProgressBar,
    QFileDialog, QMessageBox, QGroupBox, QRadioButton, QButtonGroup,
    QCheckBox, QLineEdit, QSplitter, QFrame, QAbstractItemView,
    QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QThread, Signal, QSize, QPoint
from PySide6.QtGui import QIcon, QFont, QDragEnterEvent, QDropEvent, QMouseEvent, QColor

import numpy as np

# Try to import image processing libraries
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from wand.image import Image as WandImage
    WAND_AVAILABLE = True
except ImportError:
    WAND_AVAILABLE = False


# Modern Black & White Theme Stylesheet
DARK_STYLE = """
QMainWindow {
    background-color: #0d0d0d;
    border: 1px solid #333;
}

QWidget {
    background-color: #0d0d0d;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

QWidget#centralWidget {
    background-color: #0d0d0d;
}

/* Custom Title Bar */
QWidget#titleBar {
    background-color: #1a1a1a;
    border-bottom: 1px solid #333;
}

QPushButton#titleBtn {
    background-color: transparent;
    border: none;
    border-radius: 0;
    padding: 8px 15px;
    font-size: 11pt;
    color: #888;
}

QPushButton#titleBtn:hover {
    background-color: #333;
    color: #fff;
}

QPushButton#closeBtn {
    background-color: transparent;
    border: none;
    border-radius: 0;
    padding: 8px 18px;
    font-size: 11pt;
    color: #888;
}

QPushButton#closeBtn:hover {
    background-color: #e81123;
    color: #fff;
}

QLabel#titleLabel {
    font-size: 12pt;
    font-weight: bold;
    color: #ffffff;
    padding-left: 10px;
}

QGroupBox {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    margin-top: 12px;
    padding: 15px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    color: #ffffff;
}

QPushButton {
    background-color: #1f1f1f;
    color: #ffffff;
    border: 1px solid #333;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: bold;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #2a2a2a;
    border-color: #555;
}

QPushButton:pressed {
    background-color: #ffffff;
    color: #000000;
}

QPushButton:disabled {
    background-color: #1a1a1a;
    color: #555;
    border-color: #222;
}

QPushButton#primaryBtn {
    background-color: #ffffff;
    color: #000000;
    border: none;
    font-size: 11pt;
    padding: 12px 30px;
}

QPushButton#primaryBtn:hover {
    background-color: #e0e0e0;
}

QPushButton#primaryBtn:pressed {
    background-color: #cccccc;
}

QPushButton#primaryBtn:disabled {
    background-color: #333;
    color: #666;
}

QPushButton#dangerBtn {
    background-color: #2a1a1a;
    border-color: #442222;
    color: #ff6666;
}

QPushButton#dangerBtn:hover {
    background-color: #3a2020;
    border-color: #663333;
}

QListWidget {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 5px;
    outline: none;
}

QListWidget::item {
    padding: 8px;
    border-radius: 4px;
    margin: 2px;
    color: #ccc;
}

QListWidget::item:selected {
    background-color: #ffffff;
    color: #000000;
}

QListWidget::item:hover:!selected {
    background-color: #1f1f1f;
}

QRadioButton {
    spacing: 8px;
    padding: 5px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #444;
    background-color: #1a1a1a;
}

QRadioButton::indicator:checked {
    background-color: #ffffff;
    border-color: #ffffff;
}

QRadioButton::indicator:hover {
    border-color: #888;
}

QCheckBox {
    spacing: 8px;
    padding: 5px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #444;
    background-color: #1a1a1a;
}

QCheckBox::indicator:checked {
    background-color: #ffffff;
    border-color: #ffffff;
}

QCheckBox::indicator:hover {
    border-color: #888;
}

QLineEdit {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
    selection-background-color: #ffffff;
    selection-color: #000000;
}

QLineEdit:focus {
    border-color: #555;
}

QLineEdit:disabled {
    background-color: #0d0d0d;
    color: #444;
    border-color: #1a1a1a;
}

QProgressBar {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    height: 22px;
    text-align: center;
    color: #000;
}

QProgressBar::chunk {
    background-color: #ffffff;
    border-radius: 5px;
}

QLabel#statusLabel {
    color: #666;
    font-size: 9pt;
}

QLabel#countLabel {
    font-size: 11pt;
    color: #ffffff;
    font-weight: bold;
}

QScrollBar:vertical {
    background-color: #141414;
    width: 10px;
    border-radius: 5px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #333;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #555;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background-color: #141414;
    height: 10px;
    border-radius: 5px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #333;
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #555;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QMessageBox {
    background-color: #0d0d0d;
}

QMessageBox QLabel {
    color: #ffffff;
}

QMessageBox QPushButton {
    min-width: 80px;
}
"""


class CustomTitleBar(QWidget):
    """Custom frameless window title bar"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(40)
        self._parent = parent
        self._drag_pos = None
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)
        
        # Icon and Title
        self.icon_label = QLabel("🖼️")
        self.icon_label.setStyleSheet("font-size: 14pt; padding-right: 8px;")
        layout.addWidget(self.icon_label)
        
        self.title_label = QLabel("PNG ↔ DDS Converter")
        self.title_label.setObjectName("titleLabel")
        layout.addWidget(self.title_label)
        
        layout.addStretch()
        
        # Window Controls
        self.btn_minimize = QPushButton("─")
        self.btn_minimize.setObjectName("titleBtn")
        self.btn_minimize.setFixedSize(46, 40)
        self.btn_minimize.clicked.connect(self._minimize)
        layout.addWidget(self.btn_minimize)
        
        self.btn_maximize = QPushButton("□")
        self.btn_maximize.setObjectName("titleBtn")
        self.btn_maximize.setFixedSize(46, 40)
        self.btn_maximize.clicked.connect(self._maximize)
        layout.addWidget(self.btn_maximize)
        
        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("closeBtn")
        self.btn_close.setFixedSize(46, 40)
        self.btn_close.clicked.connect(self._close)
        layout.addWidget(self.btn_close)
    
    def _minimize(self):
        self._parent.showMinimized()
    
    def _maximize(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
            self.btn_maximize.setText("□")
        else:
            self._parent.showMaximized()
            self.btn_maximize.setText("❐")
    
    def _close(self):
        self._parent.close()
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self._parent.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            if self._parent.isMaximized():
                self._parent.showNormal()
                self.btn_maximize.setText("□")
            self._parent.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._maximize()
            event.accept()


class DDSConverter:
    """Low-level DDS file handler for basic conversions"""
    
    DDS_MAGIC = b'DDS '
    DDSD_CAPS = 0x1
    DDSD_HEIGHT = 0x2
    DDSD_WIDTH = 0x4
    DDSD_PITCH = 0x8
    DDSD_PIXELFORMAT = 0x1000
    DDSD_MIPMAPCOUNT = 0x20000
    DDSD_LINEARSIZE = 0x80000
    
    DDPF_ALPHAPIXELS = 0x1
    DDPF_FOURCC = 0x4
    DDPF_RGB = 0x40
    
    DDSCAPS_TEXTURE = 0x1000
    
    @staticmethod
    def read_dds(filepath: str) -> Image.Image:
        """Read a DDS file and return PIL Image"""
        with open(filepath, 'rb') as f:
            magic = f.read(4)
            if magic != DDSConverter.DDS_MAGIC:
                raise ValueError("Not a valid DDS file")
            
            header = f.read(124)
            
            height = struct.unpack_from('<I', header, 8)[0]
            width = struct.unpack_from('<I', header, 12)[0]
            
            pf_flags = struct.unpack_from('<I', header, 76)[0]
            fourcc = header[80:84]
            rgb_bit_count = struct.unpack_from('<I', header, 84)[0]
            r_mask = struct.unpack_from('<I', header, 88)[0]
            g_mask = struct.unpack_from('<I', header, 92)[0]
            b_mask = struct.unpack_from('<I', header, 96)[0]
            a_mask = struct.unpack_from('<I', header, 100)[0]
            
            data = f.read()
            
            if pf_flags & DDSConverter.DDPF_FOURCC:
                fourcc_str = fourcc.decode('ascii', errors='ignore')
                raise ValueError(f"Compressed DDS format {fourcc_str} requires Wand/ImageMagick")
            elif pf_flags & DDSConverter.DDPF_RGB:
                return DDSConverter._decode_uncompressed(
                    data, width, height, rgb_bit_count,
                    r_mask, g_mask, b_mask, a_mask,
                    bool(pf_flags & DDSConverter.DDPF_ALPHAPIXELS)
                )
            else:
                raise ValueError(f"Unsupported DDS format: flags={pf_flags:#x}")
    
    @staticmethod
    def _decode_uncompressed(data, width, height, bit_count, r_mask, g_mask, b_mask, a_mask, has_alpha):
        """Decode uncompressed DDS data"""
        bytes_per_pixel = bit_count // 8
        expected_size = width * height * bytes_per_pixel
        
        if len(data) < expected_size:
            data = data + b'\x00' * (expected_size - len(data))
        
        if bit_count == 32:
            img_array = np.frombuffer(data[:expected_size], dtype=np.uint8)
            img_array = img_array.reshape((height, width, 4))
            if b_mask == 0xFF and r_mask == 0xFF0000:
                img_array = img_array[:, :, [2, 1, 0, 3]]
            return Image.fromarray(img_array, 'RGBA')
        elif bit_count == 24:
            img_array = np.frombuffer(data[:expected_size], dtype=np.uint8)
            img_array = img_array.reshape((height, width, 3))
            if b_mask == 0xFF and r_mask == 0xFF0000:
                img_array = img_array[:, :, [2, 1, 0]]
            return Image.fromarray(img_array, 'RGB')
        else:
            raise ValueError(f"Unsupported bit count: {bit_count}")
    
    @staticmethod
    def write_dds(image: Image.Image, filepath: str):
        """Write an image to DDS format"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        width, height = image.size
        
        header = bytearray(128)
        header[0:4] = DDSConverter.DDS_MAGIC
        struct.pack_into('<I', header, 4, 124)
        
        flags = (DDSConverter.DDSD_CAPS | DDSConverter.DDSD_HEIGHT | 
                 DDSConverter.DDSD_WIDTH | DDSConverter.DDSD_PIXELFORMAT |
                 DDSConverter.DDSD_PITCH)
        struct.pack_into('<I', header, 8, flags)
        struct.pack_into('<I', header, 12, height)
        struct.pack_into('<I', header, 16, width)
        struct.pack_into('<I', header, 20, width * 4)
        struct.pack_into('<I', header, 24, 1)
        struct.pack_into('<I', header, 28, 1)
        
        struct.pack_into('<I', header, 76, 32)
        struct.pack_into('<I', header, 80, DDSConverter.DDPF_RGB | DDSConverter.DDPF_ALPHAPIXELS)
        struct.pack_into('<I', header, 88, 32)
        struct.pack_into('<I', header, 92, 0x00FF0000)
        struct.pack_into('<I', header, 96, 0x0000FF00)
        struct.pack_into('<I', header, 100, 0x000000FF)
        struct.pack_into('<I', header, 104, 0xFF000000)
        struct.pack_into('<I', header, 108, DDSConverter.DDSCAPS_TEXTURE)
        
        pixels = np.array(image)
        pixels = pixels[:, :, [2, 1, 0, 3]]
        
        with open(filepath, 'wb') as f:
            f.write(header)
            f.write(pixels.tobytes())


class ConversionWorker(QThread):
    """Worker thread for file conversion"""
    progress = Signal(int, str)
    finished = Signal(int, int, list, str)  # Added output_dir to signal
    
    def __init__(self, files: List[str], mode: str, base_output_dir: str):
        super().__init__()
        self.files = files
        self.mode = mode
        self.base_output_dir = base_output_dir
        
        # Create timestamped output directories
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.dds_output_dir = os.path.join(base_output_dir, "DDS", self.timestamp)
        self.png_output_dir = os.path.join(base_output_dir, "PNG", self.timestamp)
        
        # Create directories as needed based on mode
        if mode in ["png_to_dds", "auto"]:
            os.makedirs(self.dds_output_dir, exist_ok=True)
        if mode in ["dds_to_png", "auto"]:
            os.makedirs(self.png_output_dir, exist_ok=True)
    
    def run(self):
        success = 0
        errors = []
        
        for i, filepath in enumerate(self.files):
            try:
                self.progress.emit(i, f"Converting: {os.path.basename(filepath)}")
                
                ext = os.path.splitext(filepath)[1].lower()
                
                if self.mode == "auto":
                    if ext == '.png':
                        self._convert_png_to_dds(filepath)
                    elif ext == '.dds':
                        self._convert_dds_to_png(filepath)
                    else:
                        raise ValueError(f"Unsupported format: {ext}")
                elif self.mode == "png_to_dds":
                    if ext != '.png':
                        raise ValueError(f"Expected PNG file, got {ext}")
                    self._convert_png_to_dds(filepath)
                elif self.mode == "dds_to_png":
                    if ext != '.dds':
                        raise ValueError(f"Expected DDS file, got {ext}")
                    self._convert_dds_to_png(filepath)
                
                success += 1
            except Exception as e:
                errors.append((filepath, str(e)))
        
        # Determine which output dir to show
        output_dir = self.dds_output_dir if self.mode == "png_to_dds" else self.png_output_dir
        if self.mode == "auto":
            output_dir = self.base_output_dir  # Show base dir for auto mode
        self.finished.emit(success, len(self.files), errors, output_dir)
    
    def _get_output_path(self, input_path: str, new_ext: str) -> str:
        base = os.path.splitext(os.path.basename(input_path))[0]
        filename = base + new_ext
        
        # Route to appropriate folder based on output extension
        if new_ext == '.dds':
            return os.path.join(self.dds_output_dir, filename)
        else:  # .png
            return os.path.join(self.png_output_dir, filename)
    
    def _convert_png_to_dds(self, input_path: str):
        output_path = self._get_output_path(input_path, '.dds')
        
        if WAND_AVAILABLE:
            try:
                with WandImage(filename=input_path) as img:
                    img.format = 'dds'
                    img.save(filename=output_path)
                return
            except Exception:
                pass
        
        if PIL_AVAILABLE:
            img = Image.open(input_path)
            DDSConverter.write_dds(img, output_path)
            return
        
        raise RuntimeError("No library available for PNG to DDS conversion")
    
    def _convert_dds_to_png(self, input_path: str):
        output_path = self._get_output_path(input_path, '.png')
        
        if WAND_AVAILABLE:
            try:
                with WandImage(filename=input_path) as img:
                    img.format = 'png'
                    img.save(filename=output_path)
                return
            except Exception:
                pass
        
        if PIL_AVAILABLE:
            try:
                img = Image.open(input_path)
                img.save(output_path, 'PNG')
                return
            except Exception:
                pass
        
        if PIL_AVAILABLE:
            try:
                img = DDSConverter.read_dds(input_path)
                img.save(output_path, 'PNG')
                return
            except Exception as e:
                raise RuntimeError(f"Failed to convert DDS: {e}")
        
        raise RuntimeError("No library available for DDS to PNG conversion")


class ImageConverterApp(QMainWindow):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PNG ↔ DDS Image Converter")
        self.setMinimumSize(900, 700)
        self.resize(950, 750)
        
        # Frameless window with icon
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        # Set window icon for taskbar
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # Fallback to png
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.png')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        
        self.files_list: List[str] = []
        self.worker: Optional[ConversionWorker] = None
        
        self._setup_ui()
        self._check_libraries()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_widget = QWidget()
        main_widget.setObjectName("centralWidget")
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom Title Bar
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Content Area
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title removed - now in custom title bar
        
        # Mode Selection
        mode_group = QGroupBox("Conversion Mode")
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setSpacing(30)
        
        self.mode_group = QButtonGroup(self)
        
        self.radio_png_to_dds = QRadioButton("PNG → DDS")
        self.radio_dds_to_png = QRadioButton("DDS → PNG")
        self.radio_auto = QRadioButton("Auto-detect")
        self.radio_auto.setChecked(True)
        
        self.mode_group.addButton(self.radio_png_to_dds, 0)
        self.mode_group.addButton(self.radio_dds_to_png, 1)
        self.mode_group.addButton(self.radio_auto, 2)
        
        mode_layout.addStretch()
        mode_layout.addWidget(self.radio_png_to_dds)
        mode_layout.addWidget(self.radio_dds_to_png)
        mode_layout.addWidget(self.radio_auto)
        mode_layout.addStretch()
        
        layout.addWidget(mode_group)
        
        # Files Section
        files_group = QGroupBox("Files to Convert")
        files_layout = QHBoxLayout(files_group)
        files_layout.setSpacing(15)
        
        # File list
        list_layout = QVBoxLayout()
        
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.file_list.setAcceptDrops(True)
        self.file_list.setDragDropMode(QAbstractItemView.InternalMove)
        list_layout.addWidget(self.file_list)
        
        self.count_label = QLabel("0 files")
        self.count_label.setObjectName("countLabel")
        list_layout.addWidget(self.count_label)
        
        files_layout.addLayout(list_layout, 1)
        
        # Buttons
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_add_files = QPushButton("📁  Add Files")
        self.btn_add_files.clicked.connect(self.add_files)
        btn_layout.addWidget(self.btn_add_files)
        
        self.btn_add_folder = QPushButton("📂  Add Folder")
        self.btn_add_folder.clicked.connect(self.add_folder)
        btn_layout.addWidget(self.btn_add_folder)
        
        btn_layout.addSpacing(10)
        
        self.btn_remove = QPushButton("✖  Remove Selected")
        self.btn_remove.clicked.connect(self.remove_selected)
        btn_layout.addWidget(self.btn_remove)
        
        self.btn_clear = QPushButton("🗑  Clear All")
        self.btn_clear.setObjectName("dangerBtn")
        self.btn_clear.clicked.connect(self.clear_files)
        btn_layout.addWidget(self.btn_clear)
        
        btn_layout.addStretch()
        
        files_layout.addLayout(btn_layout)
        layout.addWidget(files_group, 1)
        
        # Output Settings
        output_group = QGroupBox("Output Settings")
        output_layout = QVBoxLayout(output_group)
        
        # Info label explaining the output structure
        info_label = QLabel("📂 Output: [Base Dir]/DDS or PNG/[timestamp]/")
        info_label.setStyleSheet("color: #888; font-size: 9pt;")
        output_layout.addWidget(info_label)
        
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Base Output Directory:"))
        
        # Default to folder next to script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_output = os.path.join(os.path.dirname(script_dir), "Converted_Images")
        
        self.output_edit = QLineEdit()
        self.output_edit.setText(default_output)
        self.output_edit.setPlaceholderText("Select base output directory...")
        dir_layout.addWidget(self.output_edit, 1)
        
        self.btn_browse = QPushButton("Browse...")
        self.btn_browse.clicked.connect(self.browse_output)
        dir_layout.addWidget(self.btn_browse)
        
        output_layout.addLayout(dir_layout)
        layout.addWidget(output_group)
        
        # Progress Section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        progress_bar_layout = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_bar_layout.addWidget(self.progress_bar, 1)
        
        self.btn_convert = QPushButton("🔄  Convert")
        self.btn_convert.setObjectName("primaryBtn")
        self.btn_convert.clicked.connect(self.start_conversion)
        self.btn_convert.setMinimumWidth(150)
        progress_bar_layout.addWidget(self.btn_convert)
        
        progress_layout.addLayout(progress_bar_layout)
        
        self.status_label = QLabel("Ready - Add files to begin")
        self.status_label.setObjectName("statusLabel")
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
        
        # Add content to main layout
        main_layout.addWidget(content, 1)
    
    def _check_libraries(self):
        """Check available libraries"""
        if not PIL_AVAILABLE:
            QMessageBox.warning(
                self,
                "Missing Library",
                "Pillow (PIL) is not installed.\n"
                "Install it with: pip install Pillow\n\n"
                "Some features may not work."
            )
    
    def add_files(self):
        """Add files via dialog"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images to Convert",
            "",
            "All Supported (*.png *.dds);;PNG Files (*.png);;DDS Files (*.dds);;All Files (*.*)"
        )
        
        if files:
            for f in files:
                if f not in self.files_list:
                    self.files_list.append(f)
                    self.file_list.addItem(f)
            self._update_count()
    
    def add_folder(self):
        """Add folder recursively"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if folder:
            mode_id = self.mode_group.checkedId()
            extensions = []
            
            if mode_id == 0:  # PNG to DDS
                extensions = ['.png']
            elif mode_id == 1:  # DDS to PNG
                extensions = ['.dds']
            else:  # Auto
                extensions = ['.png', '.dds']
            
            count = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        filepath = os.path.join(root, file)
                        if filepath not in self.files_list:
                            self.files_list.append(filepath)
                            self.file_list.addItem(filepath)
                            count += 1
            
            self._update_count()
            
            if count > 0:
                QMessageBox.information(self, "Files Added", f"Added {count} files from folder.")
            else:
                QMessageBox.information(self, "No Files", "No matching files found.")
    
    def remove_selected(self):
        """Remove selected files"""
        for item in self.file_list.selectedItems():
            row = self.file_list.row(item)
            self.file_list.takeItem(row)
            self.files_list.remove(item.text())
        self._update_count()
    
    def clear_files(self):
        """Clear all files"""
        self.file_list.clear()
        self.files_list.clear()
        self._update_count()
    
    def browse_output(self):
        """Browse for output directory"""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if folder:
            self.output_edit.setText(folder)
    
    def _update_count(self):
        """Update file count label"""
        count = len(self.files_list)
        self.count_label.setText(f"{count} file{'s' if count != 1 else ''}")
    
    def _get_mode(self) -> str:
        """Get current conversion mode"""
        mode_id = self.mode_group.checkedId()
        if mode_id == 0:
            return "png_to_dds"
        elif mode_id == 1:
            return "dds_to_png"
        return "auto"
    
    def start_conversion(self):
        """Start conversion process"""
        if not self.files_list:
            QMessageBox.warning(self, "No Files", "Please add files to convert first!")
            return
        
        if not self.output_edit.text():
            QMessageBox.warning(self, "No Output", "Please select a base output directory!")
            return
        
        self.btn_convert.setEnabled(False)
        self.progress_bar.setMaximum(len(self.files_list))
        self.progress_bar.setValue(0)
        
        self.worker = ConversionWorker(
            self.files_list.copy(),
            self._get_mode(),
            self.output_edit.text()
        )
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()
    
    def _on_progress(self, index: int, message: str):
        """Handle progress update"""
        self.progress_bar.setValue(index + 1)
        self.status_label.setText(message)
    
    def _on_finished(self, success: int, total: int, errors: list, output_dir: str):
        """Handle conversion finished"""
        self.btn_convert.setEnabled(True)
        self.progress_bar.setValue(total)
        
        if errors:
            error_msg = "\n".join([f"• {os.path.basename(f)}: {e}" for f, e in errors[:10]])
            if len(errors) > 10:
                error_msg += f"\n... and {len(errors) - 10} more"
            
            self.status_label.setText(f"Completed with errors: {success}/{total}")
            QMessageBox.warning(
                self,
                "Conversion Complete",
                f"Successfully converted: {success}/{total}\n"
                f"Failed: {len(errors)}\n\n{error_msg}"
            )
        else:
            self.status_label.setText(f"✓ Converted {total} files → {output_dir}")
            QMessageBox.information(
                self,
                "Conversion Complete",
                f"Successfully converted all {total} files!\n\n"
                f"Output: {output_dir}"
            )


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(DARK_STYLE)
    
    window = ImageConverterApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
