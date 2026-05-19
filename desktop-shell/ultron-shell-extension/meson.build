project('ultron-shell-extension', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

extension_uuid = 'ultron-shell@ultron.org'
extension_dir = join_paths(get_option('prefix'), 'share', 'gnome-shell', 'extensions', extension_uuid)

# Install extension files
install_data(
  'metadata.json',
  'extension.js',
  'prefs.js',
  'stylesheet.css',
  install_dir: extension_dir
)

# Install schemas
install_data(
  'schemas/org.ultron.shell.gschema.xml',
  install_dir: join_paths(extension_dir, 'schemas')
)

# Compile schemas
meson.add_install_script(
  'glib-compile-schemas',
  join_paths(get_option('prefix'), 'share', 'glib-2.0', 'schemas')
)

# Install components
install_subdir(
  'components',
  install_dir: extension_dir
)

# Install UI files
if fs.exists('ui')
  install_subdir(
    'ui',
    install_dir: extension_dir
  )
endif
