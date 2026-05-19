project('ultron-control-center', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

# Install Python files
install_data(
  'src/control-center.py',
  install_dir: join_paths(get_option('prefix'), 'share', 'ultron-control-center'),
  rename: 'control-center.py'
)

# Install desktop file
install_data(
  'data/org.ultron.control-center.desktop',
  install_dir: join_paths(get_option('prefix'), 'share', 'applications'),
  rename: 'org.ultron.control-center.desktop'
)

# Install wrapper script
install_data(
  'ultron-control-center',
  install_dir: join_paths(get_option('prefix'), 'bin'),
  install_mode: 'rwxr-xr-x'
)
