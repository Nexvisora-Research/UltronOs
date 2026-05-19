project('ultron-settings', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

# Install Python files
install_subdir(
  'src',
  install_dir: join_paths(get_option('prefix'), 'share', 'ultron-settings')
)

# Install desktop file
install_data(
  'data/org.ultron.settings.desktop',
  install_dir: join_paths(get_option('prefix'), 'share', 'applications'),
  rename: 'org.ultron.settings.desktop'
)

# Install icon
install_data(
  'data/icons/org.ultron.settings.svg',
  install_dir: join_paths(get_option('prefix'), 'share', 'icons', 'hicolor', 'scalable', 'apps'),
  rename: 'org.ultron.settings.svg'
)

# Install wrapper script
wrapper = files('ultron-settings')
install_data(
  wrapper,
  install_dir: join_paths(get_option('prefix'), 'bin'),
  install_mode: 'rwxr-xr-x'
)
