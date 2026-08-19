# Changelog

All notable changes to this project are documented here.

## [Unreleased]

### Added
- Web version (HTML, CSS, JavaScript) in the `web/` folder
- Keyboard support for both desktop and web versions
- `.gitignore`, `.editorconfig`, `LICENSE`, `CONTRIBUTING.md`
- Open Graph meta tags and theme-color to the web app

### Changed
- Project restructured: Python source moved to `src/`, web files in `web/`
- Glow strip height increased from 3px to 8px with coloured box-shadow
- README rewritten with standard formatting and for-the-badge shields

### Fixed
- Double-operator stacking prevented in web calculator
- Removed unused imports (`math`, `threading`) from Python source
