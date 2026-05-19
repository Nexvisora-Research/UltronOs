# Contributing to Ultron OS

Thank you for your interest in contributing to Ultron OS! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Create a new branch** for your feature or bug fix
4. **Make your changes** following our coding standards
5. **Run the tests** to ensure everything passes
6. **Submit a pull request** with a clear description of your changes

## Development Setup

### Prerequisites

- Ubuntu 24.04 LTS or compatible distribution
- Python 3.12+
- GTK 4 development libraries
- Meson and Ninja build systems
- GNOME Shell development packages

### Install Dependencies

```bash
sudo apt install \
  python3 python3-dev python3-pip \
  libgtk-4-dev libadwaita-1-dev \
  meson ninja-build \
  gnome-shell-extensions \
  gobject-introspection
```

### Build and Test

```bash
# Run build validation
bash build.sh

# Run test suite
bash tests/run_tests.sh
```

## Project Structure

```
ultron-os/
├── apps/           # GTK4 applications
├── artwork/        # Icons, wallpapers, branding assets
├── config/         # Configuration files
├── desktop-shell/  # GNOME Shell extension
├── docs/           # Documentation
├── iso/            # ISO build configuration
├── scripts/        # Build and setup scripts
├── services/       # Background services
├── tests/          # Test suite
├── themes/         # GTK, cursor, and icon themes
└── tools/          # System utilities
```

## Coding Standards

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Maximum line length: 120 characters
- Use `pylint` or `ruff` for linting

```python
def get_system_info() -> dict[str, str]:
    """Retrieve system information including OS, kernel, and hardware.
    
    Returns:
        Dictionary containing system information key-value pairs.
    """
    ...
```

### GTK4/Libadwaita

- Use GTK 4 and Libadwaita for all UI components
- Follow GNOME Human Interface Guidelines (HIG)
- Support both light and dark themes
- Ensure accessibility compliance (WCAG 2.1)

### Shell Scripts

- Use `set -e` for error handling
- Quote all variables: `"$variable"`
- Use `[[ ]]` for conditionals
- Add comments for non-obvious operations

### CSS/SCSS

- Use CSS custom properties for theming
- Follow BEM naming convention where applicable
- Keep selectors specific but not overly complex

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(settings): add network configuration page
fix(store): resolve flatpak search timeout
docs(readme): update installation instructions
```

## Pull Request Process

1. **Update documentation** if your changes affect user-facing features
2. **Add tests** for new functionality
3. **Ensure all tests pass** (`bash tests/run_tests.sh`)
4. **Update RELEASE-NOTES.md** for significant changes
5. **Request review** from maintainers

### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with main branch

## Reporting Bugs

Use the GitHub Issues tracker with the following template:

```
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - Ultron OS Version: [e.g. 1.0.0]
 - Desktop: [e.g. GNOME 46]
 - Kernel: [e.g. 6.8.0]
```

## Feature Requests

We welcome feature requests! Please use GitHub Issues with the `enhancement` label and include:

- A clear description of the proposed feature
- The problem it would solve
- Any alternative solutions considered
- Mockups or screenshots if applicable

## License

By contributing to Ultron OS, you agree that your contributions will be licensed under the GNU General Public License v3.0.

## Contact

- **Project Website:** https://ultron.org
- **Developer:** Nexvisora Research
- **Bug Reports:** https://ultron.org/bugs
- **Support:** https://ultron.org/support
