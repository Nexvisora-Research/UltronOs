project('ultron-sync', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

install_subdir(
  'src',
  install_dir: join_paths(get_option('prefix'), 'share', 'ultron-sync')
)

install_data(
  'ultron-sync',
  install_dir: join_paths(get_option('prefix'), 'bin'),
  install_mode: 'rwxr-xr-x'
)

install_data(
  'ultron-sync.service',
  install_dir: join_paths(get_option('prefix'), 'lib', 'systemd', 'user')
)
