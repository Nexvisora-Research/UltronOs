project('ultron-gesture', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

install_subdir(
  'src',
  install_dir: join_paths(get_option('prefix'), 'share', 'ultron-gesture')
)

install_data(
  'ultron-gesture',
  install_dir: join_paths(get_option('prefix'), 'bin'),
  install_mode: 'rwxr-xr-x'
)
