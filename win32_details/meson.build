# Copy files to Python libraries directory (disable for now)
#sources = [
#    '__init__.py',
#    'cli.py',
#    'win32_details.py'
#]
#PY_INSTALLDIR.install_sources(sources, subdir: 'win32_details')

# Copy extension code to Nautilus extensions directory
configure_file(
    input: 'win32_details.py',
    output: 'win32_details.py',
    configuration: conf,
    install: true,
    install_dir: EXTENSIONS_DIR
)