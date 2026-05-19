project('ultron-voice', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

install_subdir(
  'src',
  install_dir: join_paths(get_option('prefix'), 'share', 'ultron-voice')
)

install_data(
  'ultron-voice',
  install_dir: join_paths(get_option('prefix'), 'bin'),
  install_mode: 'rwxr-xr-x'
)
