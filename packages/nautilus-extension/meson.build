project('ultron-nautilus-extension', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

# Install extension files
install_subdir(
  'ultron-nautilus',
  install_dir: join_paths(get_option('prefix'), 'share', 'nautilus-python', 'extensions')
)

# Install init file
install_data(
  'ultron-nautilus/__init__.py',
  install_dir: join_paths(get_option('prefix'), 'share', 'nautilus-python', 'extensions', 'ultron-nautilus')
)
