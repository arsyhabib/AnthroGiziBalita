#!/usr/bin/env python3
"""
Test script untuk memverifikasi semua template berfungsi dengan baik
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app
from app import app

def test_templates():
    """Test semua template yang ada"""
    
    template_dir = Path('templates')
    templates = [
        'index.html',
        'calculator.html', 
        'kpsp.html',
        'videos.html',
        'easy_mode.html',
        'library.html',
        'reports.html',
        'premium.html',
        'about.html'
    ]
    
    print("🧪 Testing Templates...")
    print("=" * 50)
    
    with app.app_context():
        for template in templates:
            template_path = template_dir / template
            
            if template_path.exists():
                try:
                    # Test render template
                    with app.test_request_context():
                        rendered = app.jinja_env.get_template(template).render()
                        print(f"✅ {template} - OK")
                except Exception as e:
                    print(f"❌ {template} - ERROR: {str(e)[:100]}...")
            else:
                print(f"⚠️  {template} - NOT FOUND")
    
    print("\n📊 Template Test Summary")
    print("=" * 50)
    
    # Check static files
    static_files = [
        'css/style.css',
        'js/main.js',
        'js/calculator.js',
        'js/kpsp.js',
        'js/videos.js',
        'js/library.js',
        'js/reports.js',
        'js/premium.js',
        'js/about.js'
    ]
    
    static_dir = Path('static')
    print("\n📁 Static Files Check:")
    for static_file in static_files:
        static_path = static_dir / static_file
        if static_path.exists():
            print(f"✅ {static_file}")
        else:
            print(f"⚠️  {static_file} - NOT FOUND")
    
    # Check configuration files
    config_files = [
        'requirements.txt',
        'Procfile', 
        'runtime.txt',
        'DOKUMENTASI_KOMPREHENSIF.md'
    ]
    
    print("\n⚙️  Configuration Files:")
    for config_file in config_files:
        config_path = Path(config_file)
        if config_path.exists():
            print(f"✅ {config_file}")
        else:
            print(f"⚠️  {config_file} - NOT FOUND")

if __name__ == '__main__':
    test_templates()
    print("\n🎉 Template testing completed!")