# 🖼️ PNG ↔ DDS Converter

A modern, lightweight image converter for batch converting between PNG and DDS formats. Built with Python and PySide6 featuring a sleek dark theme interface.

![Screenshot](screenshot.png)

## ✨ Features

- **Bidirectional Conversion** - Convert PNG → DDS or DDS → PNG
- **Auto-detect Mode** - Automatically determines conversion based on file extension
- **Batch Processing** - Convert multiple files at once
- **Folder Import** - Recursively add files from folders
- **Organized Output** - Separate folders for DDS and PNG outputs with timestamps
- **Modern UI** - Clean black & white dark theme with custom title bar
- **Portable** - Single executable, no installation required

## 📁 Output Structure

Each conversion run creates a timestamped folder to keep your files organized:

```
Converted_Images/
├── DDS/
│   ├── 2026-01-28_10-00-00/
│   │   └── image1.dds
│   └── 2026-01-28_15-30-45/
│       └── image2.dds
└── PNG/
    ├── 2026-01-28_10-00-00/
    │   └── image1.png
    └── 2026-01-28_15-30-45/
        └── image2.png
```

## 🚀 Usage

### Windows Executable
1. Download `PNG-DDS-Converter.exe` from [Releases](../../releases)
2. Run the executable
3. Add files using "Add Files" or "Add Folder" buttons
4. Select conversion mode (PNG→DDS, DDS→PNG, or Auto-detect)
5. Set output directory (default: `Converted_Images` next to the executable)
6. Click **Convert**

### From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/PNG-DDS-Converter.git
cd PNG-DDS-Converter

# Install dependencies
pip install PySide6 Pillow numpy

# Run
python image_converter.py
```

## 📋 Requirements

### For running from source:
- Python 3.8+
- PySide6
- Pillow
- NumPy

### Optional (for DXT compressed DDS):
- [Wand](https://docs.wand-py.org/) (requires ImageMagick)

## 🛠️ Building from Source

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=icon.ico --name="PNG-DDS-Converter" image_converter.py
```

The executable will be in the `dist` folder.

## 📝 Supported Formats

### DDS (DirectDraw Surface)
- ✅ Uncompressed RGBA (32-bit)
- ✅ Uncompressed RGB (24-bit)
- ⚠️ DXT1/DXT3/DXT5 (requires Wand/ImageMagick)

### PNG
- ✅ All PNG formats (via Pillow)

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Add Files |
| `Delete` | Remove Selected |
| `F5` | Start Conversion |

## 🎨 Interface

The application features a modern frameless window with:
- Custom title bar with minimize/maximize/close buttons
- Drag to move window
- Double-click title bar to maximize
- Clean black & white color scheme

## 📄 License

MIT License - feel free to use and modify.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ using Python and PySide6
