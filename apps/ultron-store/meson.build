project('ultron-store', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

# Install Python files
install_subdir(
  'src',
  install_dir: join_paths(get_option('prefix'), 'share', 'ultron-store')
)

# Install desktop file
install_data(
  'data/org.ultron.store.desktop',
  install_dir: join_paths(get_option('prefix'), 'share', 'applications'),
  rename: 'org.ultron.store.desktop'
)

# Install icon
install_data(
  'data/icons/org.ultron.store.svg',
  install_dir: join_paths(get_option('prefix'), 'share', 'icons', 'hicolor', 'scalable', 'apps'),
  rename: 'org.ultron.store.svg'
)

# Install wrapper script
install_data(
  'ultron-store',
  install_dir: join_paths(get_option('prefix'), 'bin'),
  install_mode: 'rwxr-xr-x'
)
