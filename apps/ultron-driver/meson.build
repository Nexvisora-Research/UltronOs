project('ultron-driver', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

install_data(
  'src/driver-manager.py',
  install_dir: join_paths(get_option('prefix'), 'share', 'ultron-driver'),
  rename: 'driver-manager.py'
)

install_data(
  'data/org.ultron.driver.desktop',
  install_dir: join_paths(get_option('prefix'), 'share', 'applications'),
  rename: 'org.ultron.driver.desktop'
)

install_data(
  'ultron-driver',
  install_dir: join_paths(get_option('prefix'), 'bin'),
  install_mode: 'rwxr-xr-x'
)
