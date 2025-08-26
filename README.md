# StategyDECK

A comprehensive icon generation system for creating variant icons from master SVG templates with enhanced workflow integration.

## Overview

StategyDECK provides an enhanced script that generates icon variants from master SVG files based on a CSV configuration matrix. The system supports multiple modes, finishes, sizes, and contexts to create a complete icon library for your brand assets.

## Features

### 🛡️ Robust Error Handling
- Comprehensive input validation
- Graceful handling of missing files or directories
- Detailed error messages for troubleshooting
- Recovery mechanisms for partial failures

### 📊 Advanced Logging
- Configurable log levels (DEBUG, INFO, WARNING, ERROR)
- Optional file logging with automatic log rotation
- Progress tracking for large batches
- Detailed operation timestamps

### ⚙️ Dynamic Configuration
- Command-line argument support
- Environment variable integration
- Flexible path configuration
- Custom output directory specification

### 🔧 Optimized Performance
- Context manager usage for file operations
- Efficient SVG processing
- Batch progress reporting
- Memory-efficient file handling

### 🚀 GitHub Integration
- Direct repository push functionality
- GitHub API authentication support
- Automated commit message generation
- Branch-specific deployment options

### 🧪 Testing & Validation
- Built-in validation mechanisms
- Dry-run mode for testing
- File integrity verification
- Edge case handling

## Installation

### Prerequisites

```bash
# Required for basic functionality
pip install pathlib

# Optional for PNG export (recommended)
pip install cairosvg

# Optional for GitHub integration
pip install requests
```

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Jvryan92/StategyDECK.git
cd StategyDECK
```

2. Ensure master SVG files are in place:
```
assets/masters/
├── strategy_icon_micro.svg    # For sizes ≤ 32px
└── strategy_icon_standard.svg # For sizes > 32px
```

3. Create or modify the CSV configuration matrix:
```
strategy_icon_variant_matrix.csv
```

## Usage

### Basic Usage

```bash
# Generate icons with default settings
python3 scripts/generate_icons.py

# Show what would be generated without creating files
python3 scripts/generate_icons.py --dry-run

# Validate configuration and CSV without generating
python3 scripts/generate_icons.py --validate-only
```

### Advanced Configuration

```bash
# Use custom paths and settings
python3 scripts/generate_icons.py \
  --csv-path custom_matrix.csv \
  --output-dir ./custom_output \
  --masters-dir ./custom_masters \
  --log-level DEBUG \
  --log-file generation.log

# Generate with GitHub integration
python3 scripts/generate_icons.py \
  --push-to-github \
  --github-repo username/repository
```

### Environment Variables

```bash
export GITHUB_TOKEN="your_github_token"
export GITHUB_REPO="username/repository"

python3 scripts/generate_icons.py --push-to-github
```

## Configuration

### CSV Matrix Format

The CSV file defines which icon variants to generate:

```csv
Mode,Finish,Size (px),Context,Filename
light,flat-orange,16,web,strategy_icon-light-flat-orange-16px.png
light,flat-orange,32,web,strategy_icon-light-flat-orange-32px.png
dark,satin-black,64,mobile,strategy_icon-dark-satin-black-64px.png
```

**Fields:**
- `Mode`: `light` or `dark` theme
- `Finish`: Color variant (see available finishes below)
- `Size (px)`: Icon size in pixels (positive integer)
- `Context`: Usage context (e.g., web, mobile, print)
- `Filename`: Optional custom filename (auto-generated if empty)

### Available Finishes

- `flat-orange`: Brand orange (#FF6A00)
- `matte-carbon`: Matte gray (#333333)
- `satin-black`: Pure black (#000000)
- `burnt-orange`: Dark orange (#CC5500)
- `copper-foil`: Copper color (#B87333)
- `embossed-paper`: Light gray (#F5F5F5)

### Output Structure

Generated icons are organized in a hierarchical structure:

```
assets/icons/
├── light/
│   ├── flat-orange/
│   │   ├── 16px/
│   │   │   └── web/
│   │   │       ├── icon.svg
│   │   │       └── icon.png
│   └── matte-carbon/
└── dark/
    └── satin-black/
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--csv-path` | Path to CSV matrix file | `strategy_icon_variant_matrix.csv` |
| `--output-dir` | Output directory for generated icons | `assets/icons` |
| `--masters-dir` | Directory containing master SVG files | `assets/masters` |
| `--log-level` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` |
| `--log-file` | Path to log file (optional) | None |
| `--push-to-github` | Push generated files to GitHub | `false` |
| `--github-repo` | GitHub repository (owner/repo format) | From env |
| `--dry-run` | Show what would be generated | `false` |
| `--validate-only` | Only validate configuration | `false` |

## Examples

### Generate Icons for Different Contexts

```csv
Mode,Finish,Size (px),Context,Filename
light,flat-orange,16,web,icon-web-16.png
light,flat-orange,32,mobile,icon-mobile-32.png
light,flat-orange,48,desktop,icon-desktop-48.png
dark,satin-black,16,web,icon-web-dark-16.png
```

### Batch Processing with Logging

```bash
python3 scripts/generate_icons.py \
  --log-level DEBUG \
  --log-file batch_$(date +%Y%m%d).log
```

### CI/CD Integration

```bash
# In your CI/CD pipeline
python3 scripts/generate_icons.py \
  --validate-only \
  --log-level WARNING

if [ $? -eq 0 ]; then
  python3 scripts/generate_icons.py \
    --push-to-github \
    --github-repo $GITHUB_REPOSITORY
fi
```

## Testing

Run the comprehensive test suite:

```bash
python3 test_enhanced_script.py
```

The test suite validates:
- Basic functionality
- Input validation
- File generation integrity
- Error handling
- Edge cases
- Custom configuration options

## Troubleshooting

### Common Issues

**Error: "CSV file not found"**
- Ensure the CSV file exists at the specified path
- Check file permissions and encoding (should be UTF-8)

**Error: "Master not found"**
- Verify master SVG files are in the masters directory
- Check that filenames match: `strategy_icon_micro.svg` and `strategy_icon_standard.svg`

**Warning: "PNG exports: 0"**
- Install cairosvg for PNG generation: `pip install cairosvg`
- PNG export is optional; SVG files are still generated

**GitHub Push Issues**
- Set GITHUB_TOKEN environment variable
- Ensure token has appropriate repository permissions
- Verify repository format: `owner/repository`

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
python3 scripts/generate_icons.py --log-level DEBUG --log-file debug.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate tests
4. Run the test suite to ensure compatibility
5. Submit a pull request with a detailed description

## License

This project is part of the StategyDECK brand asset management system.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the test output for validation errors
3. Enable debug logging for detailed diagnostics
4. Create an issue with relevant logs and configuration details