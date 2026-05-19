project('ultron-updater', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

install_data(
  'src/updater.py',
  install_dir: join_paths(get_option('prefix'), 'share', 'ultron-updater'),
  rename: 'updater.py'
)

install_data(
  'data/org.ultron.updater.desktop',
  install_dir: join_paths(get_option('prefix'), 'share', 'applications'),
  rename: 'org.ultron.updater.desktop'
)

install_data(
  'ultron-updater',
  install_dir: join_paths(get_option('prefix'), 'bin'),
  install_mode: 'rwxr-xr-x'
)
