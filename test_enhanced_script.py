#!/usr/bin/env python3
"""
Test script for the enhanced icon generation script.
This script validates the integrity of generated files and tests edge cases.
"""
import os
import sys
import csv
import json
import tempfile
import shutil
from pathlib import Path
import subprocess

def test_basic_functionality():
    """Test basic icon generation functionality."""
    print("Testing basic functionality...")
    
    # Test help command
    result = subprocess.run([
        sys.executable, "scripts/generate_icons_enhanced.py", "--help"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Help command failed: {result.stderr}")
        return False
    
    print("✅ Help command works")
    return True

def test_validation():
    """Test validation functionality."""
    print("Testing validation functionality...")
    
    # Test validate-only
    result = subprocess.run([
        sys.executable, "scripts/generate_icons_enhanced.py", "--validate-only"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Validation failed: {result.stderr}")
        return False
    
    if "Validation completed successfully" not in result.stdout:
        print("❌ Validation success message not found")
        return False
    
    print("✅ Validation works")
    return True

def test_dry_run():
    """Test dry run functionality."""
    print("Testing dry run functionality...")
    
    result = subprocess.run([
        sys.executable, "scripts/generate_icons_enhanced.py", "--dry-run"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Dry run failed: {result.stderr}")
        return False
    
    if "Would generate:" not in result.stdout:
        print("❌ Dry run messages not found")
        return False
    
    print("✅ Dry run works")
    return True

def test_file_generation():
    """Test actual file generation."""
    print("Testing file generation...")
    
    # Clean up any existing generated files
    icons_dir = Path("assets/icons")
    if icons_dir.exists():
        shutil.rmtree(icons_dir)
    
    # Generate files
    result = subprocess.run([
        sys.executable, "scripts/generate_icons_enhanced.py", "--log-level", "WARNING"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ File generation failed: {result.stderr}")
        return False
    
    # Check if files were created
    if not icons_dir.exists():
        print("❌ Icons directory not created")
        return False
    
    # Count generated files
    svg_files = list(icons_dir.glob("**/*.svg"))
    if len(svg_files) == 0:
        print("❌ No SVG files generated")
        return False
    
    print(f"✅ Generated {len(svg_files)} SVG files")
    
    # Validate file contents
    for svg_file in svg_files[:3]:  # Check first 3 files
        if not svg_file.exists() or svg_file.stat().st_size == 0:
            print(f"❌ Invalid file: {svg_file}")
            return False
        
        content = svg_file.read_text()
        if not content.startswith("<?xml") and not content.startswith("<svg"):
            print(f"❌ Invalid SVG content in: {svg_file}")
            return False
    
    print("✅ File generation and validation works")
    return True

def test_error_handling():
    """Test error handling with invalid inputs."""
    print("Testing error handling...")
    
    # Test with non-existent CSV file
    result = subprocess.run([
        sys.executable, "scripts/generate_icons_enhanced.py", 
        "--csv-path", "nonexistent.csv"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("❌ Should have failed with non-existent CSV file")
        return False
    
    if "CSV file not found" not in result.stderr and "CSV file not found" not in result.stdout:
        print("❌ Expected error message not found")
        return False
    
    print("✅ Error handling works")
    return True

def test_custom_output_dir():
    """Test custom output directory functionality."""
    print("Testing custom output directory...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        custom_output = Path(temp_dir) / "custom_icons"
        
        result = subprocess.run([
            sys.executable, "scripts/generate_icons_enhanced.py",
            "--output-dir", str(custom_output),
            "--log-level", "WARNING"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Custom output directory test failed: {result.stderr}")
            return False
        
        if not custom_output.exists():
            print("❌ Custom output directory not created")
            return False
        
        svg_files = list(custom_output.glob("**/*.svg"))
        if len(svg_files) == 0:
            print("❌ No files generated in custom directory")
            return False
    
    print("✅ Custom output directory works")
    return True

def create_invalid_csv_test():
    """Test with invalid CSV content."""
    print("Testing invalid CSV handling...")
    
    # Create invalid CSV
    invalid_csv = "test_invalid.csv"
    with open(invalid_csv, "w") as f:
        f.write("Mode,Finish,Size (px),Context\n")
        f.write("invalid_mode,flat-orange,16,web\n")
        f.write("light,invalid_finish,32,web\n")
        f.write("dark,satin-black,invalid_size,web\n")
    
    try:
        result = subprocess.run([
            sys.executable, "scripts/generate_icons_enhanced.py",
            "--csv-path", invalid_csv,
            "--validate-only"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("❌ Should have failed with invalid CSV")
            return False
        
        if "Invalid mode" not in result.stderr and "Invalid mode" not in result.stdout:
            print("❌ Expected validation error not found")
            return False
        
        print("✅ Invalid CSV handling works")
        return True
    
    finally:
        if os.path.exists(invalid_csv):
            os.remove(invalid_csv)

def main():
    """Run all tests."""
    print("🧪 Starting Enhanced Icon Generation Script Tests\n")
    
    tests = [
        test_basic_functionality,
        test_validation,
        test_dry_run,
        test_file_generation,
        test_error_handling,
        test_custom_output_dir,
        create_invalid_csv_test,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()
    
    print(f"🎯 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())