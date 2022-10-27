project('win32-details',
        version: '0.4',
        meson_version: '>= 0.59.0',
        default_options: [ 'warning_level=2',
                           'werror=false',
                         ]
)

# Import modules
python = import('python')

# Nautilus extension directory
EXTENSIONS_DIR = join_paths(get_option('prefix'), get_option('datadir'), 'nautilus-python/extensions')

dependency('glib-2.0')
dependency('gtk+-3.0')
dependency('pygobject-3.0', version: '>= 3.40.0')

# Check if python3 is installed
PY_INSTALLDIR = python.find_installation('python3', required: true)

# Check if exiftool is installed
find_program('exiftool', required: true)

# Install configuration data
conf = configuration_data()
conf.set('EXTENSIONS_DIR', EXTENSIONS_DIR)

# Subdirs
subdir('win32_details')
