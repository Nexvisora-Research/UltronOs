project('ultron-gtk-theme', 'c',
  version: '1.0.0',
  meson_version: '>= 0.57.0'
)

theme_name = 'Ultron'
themes = ['Ultron-Dark', 'Ultron-Light']

foreach theme : themes
  theme_dir = join_paths(get_option('prefix'), 'share', 'themes', theme)
  
  install_data(
    join_paths(theme, 'index.theme'),
    install_dir: join_paths(theme_dir)
  )
  
  install_data(
    join_paths(theme, 'gtk-4.0', 'gtk.css'),
    install_dir: join_paths(theme_dir, 'gtk-4.0')
  )
  
  # Install GTK 3 theme as well
  if fs.exists(join_paths(theme, 'gtk-3.0'))
    install_subdir(
      join_paths(theme, 'gtk-3.0'),
      install_dir: join_paths(theme_dir)
    )
  endif
endforeach

# Install icon theme
install_subdir(
  '../icons',
  install_dir: join_paths(get_option('prefix'), 'share', 'icons', 'Ultron-Icons')
)

# Install cursor theme
install_subdir(
  '../cursor',
  install_dir: join_paths(get_option('prefix'), 'share', 'icons', 'Ultron-Cursor')
)

# Install artwork
install_subdir(
  '../../artwork',
  install_dir: join_paths(get_option('prefix'), 'share', 'ultron')
)
