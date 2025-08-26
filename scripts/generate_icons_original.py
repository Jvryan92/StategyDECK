#!/usr/bin/env python3
"""
Enhanced Icon Generation Script for StategyDECK

This script generates icon variants from master SVG files based on a CSV configuration matrix.
Enhanced with robust error handling, logging, dynamic configuration, and GitHub integration.
"""
import os
import sys
import csv
import json
import argparse
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

# Third-party imports (will be imported conditionally)
try:
    import requests
except ImportError:
    requests = None

try:
    import cairosvg
except ImportError:
    cairosvg = None

# Default paths - can be overridden via CLI arguments
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
MASTERS = ASSETS / "masters"
OUT = ASSETS / "icons"
CSV_PATH = ROOT / "strategy_icon_variant_matrix.csv"

# Color tokens and finish mappings
TOKENS = {
    "paper": "#FFFFFF",
    "slate_950": "#060607",
    "brand_orange": "#FF6A00",
    "ink": "#000000",
    "copper": "#B87333",
    "burnt_orange": "#CC5500",
    "matte": "#333333",
    "embossed": "#F5F5F5"
}

FINISH_COLORS = {
    "flat-orange": TOKENS["brand_orange"],
    "matte-carbon": TOKENS["matte"],
    "satin-black": TOKENS["ink"],
    "burnt-orange": TOKENS["burnt_orange"],
    "copper-foil": TOKENS["copper"],
    "embossed-paper": TOKENS["embossed"]
}

# Logging configuration
def setup_logging(log_level: str = "INFO", log_file: Optional[Path] = None) -> logging.Logger:
    """Set up logging configuration with both file and console handlers."""
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")
    
    return logger

class IconGenerationError(Exception):
    """Custom exception for icon generation errors."""
    pass

class GitHubIntegration:
    """Handle GitHub API operations for pushing generated files."""
    
    def __init__(self, token: Optional[str] = None, repo_owner: str = "", repo_name: str = "", logger: Optional[logging.Logger] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.logger = logger or logging.getLogger(__name__)
        self.base_url = "https://api.github.com"
        
    def push_files(self, file_paths: List[Path], commit_message: str = "Update generated icons") -> bool:
        """Push generated files to GitHub repository."""
        if not self.token:
            self.logger.warning("No GitHub token provided, skipping repository push")
            return False
            
        if not requests:
            self.logger.warning("requests library not available, skipping repository push")
            return False
            
        try:
            self.logger.info(f"Pushing {len(file_paths)} files to {self.repo_owner}/{self.repo_name}")
            # Implementation would go here for actual GitHub API integration
            # For now, just log the action
            self.logger.info(f"Would push files with message: {commit_message}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to push to GitHub: {e}")
            return False

def validate_config(config: Dict) -> Tuple[bool, List[str]]:
    """Validate configuration parameters."""
    errors = []
    
    required_fields = ['csv_path', 'output_dir', 'masters_dir']
    for field in required_fields:
        if field not in config or not config[field]:
            errors.append(f"Missing required field: {field}")
    
    # Check if paths exist
    if 'csv_path' in config:
        csv_path = Path(config['csv_path'])
        if not csv_path.exists():
            errors.append(f"CSV file not found: {csv_path}")
    
    if 'masters_dir' in config:
        masters_dir = Path(config['masters_dir'])
        if not masters_dir.exists():
            errors.append(f"Masters directory not found: {masters_dir}")
    
    return len(errors) == 0, errors

def generate_icons(args: argparse.Namespace, logger: logging.Logger) -> Tuple[int, int, List[Path]]:

def pick_master(size_px: int, masters_dir: Path) -> Path:
    """Select appropriate master SVG file based on size."""
    micro_path = masters_dir / "strategy_icon_micro.svg"
    standard_path = masters_dir / "strategy_icon_standard.svg"
    
    if size_px <= 32 and micro_path.exists():
        return micro_path
    elif standard_path.exists():
        return standard_path
    else:
        raise IconGenerationError(f"No suitable master SVG found for size {size_px}px")

def bake_svg(master_svg: str, mode: str, finish: str, logger: Optional[logging.Logger] = None) -> str:
    """Transform master SVG with specified mode and finish colors."""
    if logger:
        logger.debug(f"Baking SVG with mode={mode}, finish={finish}")
    
    try:
        bg = TOKENS["paper"] if mode == "light" else TOKENS["slate_950"]
        fg = FINISH_COLORS.get(finish, TOKENS["brand_orange"])
        
        svg = master_svg.replace("#FF6A00", bg)   # replace background rect
        svg = svg.replace("#FFFFFF", fg)          # replace icon shapes
        
        return svg
    except Exception as e:
        if logger:
            logger.error(f"Failed to bake SVG: {e}")
        raise IconGenerationError(f"SVG processing failed: {e}")

def export_png(svg_bytes: bytes, out_png: Path, size_px: int, logger: Optional[logging.Logger] = None) -> bool:
    """Export SVG to PNG format using cairosvg."""
    if not cairosvg:
        if logger:
            logger.debug("cairosvg not available, skipping PNG export")
        return False
    
    try:
        out_png.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(
            bytestring=svg_bytes, 
            write_to=str(out_png), 
            output_width=size_px, 
            output_height=size_px
        )
        if logger:
            logger.debug(f"Exported PNG: {out_png}")
        return True
    except Exception as e:
        if logger:
            logger.warning(f"Failed to export PNG {out_png}: {e}")
        return False

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate icon variants from master SVG files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Use default settings
  %(prog)s --csv-path custom_matrix.csv      # Use custom CSV matrix
  %(prog)s --output-dir ./output             # Custom output directory
  %(prog)s --log-level DEBUG                 # Enable debug logging
  %(prog)s --push-to-github                  # Push results to GitHub
        """
    )
    
    parser.add_argument(
        '--csv-path', 
        type=Path,
        default=CSV_PATH,
        help=f'Path to CSV matrix file (default: {CSV_PATH})'
    )
    
    parser.add_argument(
        '--output-dir', 
        type=Path,
        default=OUT,
        help=f'Output directory for generated icons (default: {OUT})'
    )
    
    parser.add_argument(
        '--masters-dir', 
        type=Path,
        default=MASTERS,
        help=f'Directory containing master SVG files (default: {MASTERS})'
    )
    
    parser.add_argument(
        '--log-level', 
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file', 
        type=Path,
        help='Path to log file (optional)'
    )
    
    parser.add_argument(
        '--push-to-github', 
        action='store_true',
        help='Push generated files to GitHub repository'
    )
    
    parser.add_argument(
        '--github-repo', 
        help='GitHub repository in format owner/repo (env: GITHUB_REPO)'
    )
    
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Show what would be generated without creating files'
    )
    
    parser.add_argument(
        '--validate-only', 
        action='store_true',
        help='Only validate configuration and CSV, do not generate files'
    )
    
    return parser.parse_args()

def validate_csv_row(row: Dict[str, str], row_num: int, logger: logging.Logger) -> Tuple[bool, List[str]]:
    """Validate a single CSV row."""
    errors = []
    required_fields = ['Mode', 'Finish', 'Size (px)', 'Context']
    
    for field in required_fields:
        if field not in row or not row[field].strip():
            errors.append(f"Row {row_num}: Missing or empty field '{field}'")
    
    # Validate mode
    if 'Mode' in row and row['Mode'] not in ['light', 'dark']:
        errors.append(f"Row {row_num}: Invalid mode '{row['Mode']}'. Must be 'light' or 'dark'")
    
    # Validate finish
    if 'Finish' in row and row['Finish'] not in FINISH_COLORS:
        errors.append(f"Row {row_num}: Invalid finish '{row['Finish']}'. Must be one of: {list(FINISH_COLORS.keys())}")
    
    # Validate size
    if 'Size (px)' in row:
        try:
            size = int(row['Size (px)'])
            if size <= 0:
                errors.append(f"Row {row_num}: Size must be positive, got {size}")
        except ValueError:
            errors.append(f"Row {row_num}: Size must be a number, got '{row['Size (px)']}'")
    """Generate icon variants based on CSV configuration."""
    logger.info("Starting icon generation process")
    start_time = time.time()
    
    # Validate configuration
    config = {
        'csv_path': args.csv_path,
        'output_dir': args.output_dir,
        'masters_dir': args.masters_dir
    }
    
    is_valid, config_errors = validate_config(config)
    if not is_valid:
        for error in config_errors:
            logger.error(error)
        raise IconGenerationError("Configuration validation failed")
    
    # Read and validate CSV
    logger.info(f"Reading CSV matrix from: {args.csv_path}")
    try:
        with open(args.csv_path, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as e:
        logger.error(f"Failed to read CSV file: {e}")
        raise IconGenerationError(f"CSV reading failed: {e}")
    
    if not rows:
        logger.warning("CSV file is empty or has no data rows")
        return 0, 0, []
    
    logger.info(f"Loaded {len(rows)} rows from CSV")
    
    # Validate all CSV rows
    validation_errors = []
    for i, row in enumerate(rows, 1):
        is_valid_row, row_errors = validate_csv_row(row, i, logger)
        validation_errors.extend(row_errors)
    
    if validation_errors:
        for error in validation_errors:
            logger.error(error)
        raise IconGenerationError("CSV validation failed")
    
    if args.validate_only:
        logger.info("Validation completed successfully. Exiting (--validate-only)")
        return 0, 0, []
    
    generated = 0
    png_count = 0
    generated_files = []
    
    logger.info(f"Processing {len(rows)} icon variants")
    
    for i, row in enumerate(rows, 1):
        try:
            mode = row["Mode"]
            finish = row["Finish"]
            size = int(row["Size (px)"])
            context = row["Context"]
            filename = row.get("Filename") or f"strategy_icon-{mode}-{finish}-{size}px.png"
            
            logger.debug(f"Processing row {i}: {mode}/{finish}/{size}px/{context}")
            
            # Get master SVG
            master_path = pick_master(size, args.masters_dir)
            logger.debug(f"Using master: {master_path}")
            
            try:
                master_svg = master_path.read_text(encoding="utf-8")
            except Exception as e:
                logger.error(f"Failed to read master SVG {master_path}: {e}")
                continue
            
            # Transform SVG
            baked_svg = bake_svg(master_svg, mode, finish, logger)
            
            # Prepare output paths
            folder = args.output_dir / mode / finish / f"{size}px" / context
            svg_path = folder / (Path(filename).stem + ".svg")
            png_path = folder / Path(filename).name
            
            if args.dry_run:
                logger.info(f"Would generate: {svg_path}")
                generated += 1
                continue
            
            # Create output directory
            try:
                folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create directory {folder}: {e}")
                continue
            
            # Write SVG file using context manager
            try:
                with open(svg_path, "w", encoding="utf-8") as f:
                    f.write(baked_svg)
                generated_files.append(svg_path)
                logger.debug(f"Generated SVG: {svg_path}")
            except Exception as e:
                logger.error(f"Failed to write SVG file {svg_path}: {e}")
                continue
            
            # Export PNG if possible
            if export_png(baked_svg.encode("utf-8"), png_path, size, logger):
                png_count += 1
                generated_files.append(png_path)
            
            generated += 1
            
            # Progress logging
            if i % 10 == 0 or i == len(rows):
                logger.info(f"Progress: {i}/{len(rows)} rows processed")
        
        except Exception as e:
            logger.error(f"Failed to process row {i}: {e}")
            continue
    
    elapsed_time = time.time() - start_time
    logger.info(f"Generation completed in {elapsed_time:.2f} seconds")
    logger.info(f"Generated {generated} SVG variants, {png_count} PNG exports")
    
    return generated, png_count, generated_files

def main():
    """Main entry point for the icon generation script."""
    try:
        args = parse_args()
        
        # Set up logging
        logger = setup_logging(args.log_level, args.log_file)
        logger.info("Starting Icon Generation Script")
        logger.info(f"Configuration: CSV={args.csv_path}, Output={args.output_dir}")
        
        # Generate icons
        generated, png_count, generated_files = generate_icons(args, logger)
        
        if args.dry_run:
            logger.info(f"Dry run completed. Would generate {generated} SVG files")
            return
        
        # GitHub integration
        if args.push_to_github and generated_files:
            github_repo = args.github_repo or os.getenv('GITHUB_REPO', '')
            if github_repo and '/' in github_repo:
                repo_owner, repo_name = github_repo.split('/', 1)
                github = GitHubIntegration(
                    repo_owner=repo_owner, 
                    repo_name=repo_name, 
                    logger=logger
                )
                github.push_files(generated_files, f"Generated {generated} icon variants")
            else:
                logger.warning("GitHub repository not specified. Use --github-repo owner/repo")
        
        logger.info("Icon generation completed successfully")
        
    except IconGenerationError as e:
        logging.getLogger(__name__).error(f"Generation failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Generation interrupted by user")
        sys.exit(130)
    except Exception as e:
        logging.getLogger(__name__).error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

def pick_master(size_px: int, masters_dir: Path) -> Path:
    """Select appropriate master SVG file based on size."""
    micro_path = masters_dir / "strategy_icon_micro.svg"
    standard_path = masters_dir / "strategy_icon_standard.svg"
    
    if size_px <= 32 and micro_path.exists():
        return micro_path
    elif standard_path.exists():
        return standard_path
    else:
        raise IconGenerationError(f"No suitable master SVG found for size {size_px}px")

def bake_svg(master_svg: str, mode: str, finish: str, logger: Optional[logging.Logger] = None) -> str:
    """Transform master SVG with specified mode and finish colors."""
    if logger:
        logger.debug(f"Baking SVG with mode={mode}, finish={finish}")
    
    try:
        bg = TOKENS["paper"] if mode == "light" else TOKENS["slate_950"]
        fg = FINISH_COLORS.get(finish, TOKENS["brand_orange"])
        
        svg = master_svg.replace("#FF6A00", bg)   # replace background rect
        svg = svg.replace("#FFFFFF", fg)          # replace icon shapes
        
        return svg
    except Exception as e:
        if logger:
            logger.error(f"Failed to bake SVG: {e}")
        raise IconGenerationError(f"SVG processing failed: {e}")

def export_png(svg_bytes: bytes, out_png: Path, size_px: int, logger: Optional[logging.Logger] = None) -> bool:
    """Export SVG to PNG format using cairosvg."""
    if not cairosvg:
        if logger:
            logger.debug("cairosvg not available, skipping PNG export")
        return False
    
    try:
        out_png.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(
            bytestring=svg_bytes, 
            write_to=str(out_png), 
            output_width=size_px, 
            output_height=size_px
        )
        if logger:
            logger.debug(f"Exported PNG: {out_png}")
        return True
    except Exception as e:
        if logger:
            logger.warning(f"Failed to export PNG {out_png}: {e}")
        return False

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate icon variants from master SVG files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Use default settings
  %(prog)s --csv-path custom_matrix.csv      # Use custom CSV matrix
  %(prog)s --output-dir ./output             # Custom output directory
  %(prog)s --log-level DEBUG                 # Enable debug logging
  %(prog)s --push-to-github                  # Push results to GitHub
        """
    )
    
    parser.add_argument(
        '--csv-path', 
        type=Path,
        default=CSV_PATH,
        help=f'Path to CSV matrix file (default: {CSV_PATH})'
    )
    
    parser.add_argument(
        '--output-dir', 
        type=Path,
        default=OUT,
        help=f'Output directory for generated icons (default: {OUT})'
    )
    
    parser.add_argument(
        '--masters-dir', 
        type=Path,
        default=MASTERS,
        help=f'Directory containing master SVG files (default: {MASTERS})'
    )
    
    parser.add_argument(
        '--log-level', 
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file', 
        type=Path,
        help='Path to log file (optional)'
    )
    
    parser.add_argument(
        '--push-to-github', 
        action='store_true',
        help='Push generated files to GitHub repository'
    )
    
    parser.add_argument(
        '--github-repo', 
        help='GitHub repository in format owner/repo (env: GITHUB_REPO)'
    )
    
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Show what would be generated without creating files'
    )
    
    parser.add_argument(
        '--validate-only', 
        action='store_true',
        help='Only validate configuration and CSV, do not generate files'
    )
    
    return parser.parse_args()

def validate_csv_row(row: Dict[str, str], row_num: int, logger: logging.Logger) -> Tuple[bool, List[str]]:
    """Validate a single CSV row."""
    errors = []
    required_fields = ['Mode', 'Finish', 'Size (px)', 'Context']
    
    for field in required_fields:
        if field not in row or not row[field].strip():
            errors.append(f"Row {row_num}: Missing or empty field '{field}'")
    
    # Validate mode
    if 'Mode' in row and row['Mode'] not in ['light', 'dark']:
        errors.append(f"Row {row_num}: Invalid mode '{row['Mode']}'. Must be 'light' or 'dark'")
    
    # Validate finish
    if 'Finish' in row and row['Finish'] not in FINISH_COLORS:
        errors.append(f"Row {row_num}: Invalid finish '{row['Finish']}'. Must be one of: {list(FINISH_COLORS.keys())}")
    
    # Validate size
    if 'Size (px)' in row:
        try:
            size = int(row['Size (px)'])
            if size <= 0:
                errors.append(f"Row {row_num}: Size must be positive, got {size}")
        except ValueError:
            errors.append(f"Row {row_num}: Size must be a number, got '{row['Size (px)']}'")
