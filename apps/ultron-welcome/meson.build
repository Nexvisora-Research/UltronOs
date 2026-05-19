project('ultron-welcome', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

# Install Python script
install_data(
  'ultron-welcome.py',
  install_dir: join_paths(get_option('prefix'), 'bin'),
  rename: 'ultron-welcome'
)

# Install desktop file
install_data(
  'ultron-welcome.desktop',
  install_dir: join_paths(get_option('prefix'), 'share', 'applications')
)

# Install icon
install_data(
  '../../artwork/icons/scalable/apps/ultron-welcome.svg',
  install_dir: join_paths(get_option('prefix'), 'share', 'icons', 'hicolor', 'scalable', 'apps'),
  rename: 'ultron-welcome.svg'
)
