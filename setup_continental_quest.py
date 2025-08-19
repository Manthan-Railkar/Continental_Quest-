#!/usr/bin/env python3
"""
Continental Quest - Setup Script
Sets up the integration between your existing globe.py and the web launcher
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("🌍 Continental Quest - Project Setup")
    print("Integration with your existing OpenGL globe")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_existing_dependencies():
    """Check your existing game dependencies"""
    print("\n🔍 Checking your existing game dependencies...")
    
    existing_deps = [
        ("pygame", "Your 3D globe game engine"),
        ("OpenGL", "3D rendering (PyOpenGL)"),
        ("PIL", "Image processing (Pillow)"),
        ("numpy", "Numerical computations"),
    ]
    
    all_good = True
    for package, description in existing_deps:
        try:
            if package == "OpenGL":
                import OpenGL.GL
            elif package == "PIL":
                import PIL.Image
            else:
                __import__(package)
            print(f"✅ {package} - Available ({description})")
        except ImportError:
            print(f"❌ {package} - Missing ({description})")
            all_good = False
    
    return all_good

def install_integration_dependencies():
    """Install dependencies needed for the web launcher integration"""
    print("\n📦 Installing web launcher dependencies...")
    
    integration_deps = [
        ("pywebview", "Desktop web integration"),
        ("flask", "Optional: Web server fallback"),
    ]
    
    for package, description in integration_deps:
        try:
            __import__(package)
            print(f"✅ {package} - Already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                print(f"   You can install it manually: pip install {package}")

def check_project_files():
    """Check if all required files are present"""
    print("\n🔍 Checking project files...")
    
    project_dir = Path(__file__).parent
    
    required_files = [
        ('globe.py', 'Your existing 3D OpenGL globe'),
        ('continental_quest_landing.html', 'Web launcher interface'),
        ('style.css', 'Landing page styling'),
        ('script.js', 'Interactive JavaScript'),
        ('continental_quest_app.py', 'Integrated application'),
    ]
    
    optional_files = [
        ('world.jpg', 'Earth texture (required by globe.py)'),
        ('galaxy.jpg', 'Galaxy background texture (required by globe.py)'),
    ]
    
    all_required = True
    
    print("📋 Required files:")
    for filename, description in required_files:
        file_path = project_dir / filename
        if file_path.exists():
            print(f"✅ {filename} - Found ({description})")
        else:
            print(f"❌ {filename} - Missing ({description})")
            all_required = False
    
    print("\n📋 Optional files (required by your globe.py):")
    for filename, description in optional_files:
        file_path = project_dir / filename
        if file_path.exists():
            print(f"✅ {filename} - Found ({description})")
        else:
            print(f"⚠️  {filename} - Missing ({description})")
            print(f"   👉 Make sure you have this texture file for your 3D globe")
    
    return all_required

def create_requirements_file():
    """Create requirements.txt for the integrated project"""
    requirements_content = """# Continental Quest - Integrated Project Requirements

# Your existing game dependencies
pygame>=2.0.0
PyOpenGL>=3.1.0
Pillow>=8.0.0
numpy>=1.20.0

# Web launcher integration
pywebview>=4.0.0

# Optional web server fallback
flask>=2.0.0
requests>=2.25.0

# Development tools (optional)
# pip-tools>=6.0.0
"""
    
    try:
        with open('requirements.txt', 'w') as f:
            f.write(requirements_content)
        print("✅ Created requirements.txt")
        return True
    except Exception as e:
        print(f"❌ Failed to create requirements.txt: {e}")
        return False

def create_run_script():
    """Create a simple run script"""
    run_script_content = """@echo off
echo 🌍 Starting Continental Quest...
python continental_quest_app.py
pause
"""
    
    try:
        with open('run_continental_quest.bat', 'w') as f:
            f.write(run_script_content)
        print("✅ Created run_continental_quest.bat")
        return True
    except Exception as e:
        print(f"❌ Failed to create run script: {e}")
        return False

def show_usage_guide():
    """Display usage instructions"""
    print("\n" + "=" * 60)
    print("🚀 USAGE GUIDE")
    print("=" * 60)
    
    print("""
📋 HOW TO RUN YOUR INTEGRATED CONTINENTAL QUEST:

1. 🖥️  DESKTOP APP (Recommended):
   python continental_quest_app.py
   
   OR double-click: run_continental_quest.bat

2. 🌐 WEB BROWSER FALLBACK:
   Open continental_quest_landing.html in your browser
   (Note: 3D globe integration won't work in browser mode)

🎮 HOW IT WORKS:

1. 🌍 Beautiful web launcher opens with the space-themed interface
2. 🖱️  Click on continent hotspots or "Explore" buttons
3. 🚀 Your 3D OpenGL globe automatically launches
4. 🎯 Navigate your 3D Earth with mouse and keyboard
5. 🔄 When you close the 3D globe, the launcher reappears

🎨 FEATURES:

✅ Space-themed landing page with realistic Earth
✅ Interactive continent selection
✅ Seamless integration with your existing 3D globe
✅ Automatic window management (minimize/restore)
✅ Progress tracking (ready for your game logic)
✅ Difficulty selection system

🔧 CUSTOMIZATION:

- Modify globe.py to add continent-specific features
- Update progress tracking in continental_quest_app.py
- Customize the web interface in the HTML/CSS/JS files
- Add your own textures and game logic

📁 PROJECT STRUCTURE:

continental_quest_app.py     # Main integrated application
globe.py                     # Your existing 3D OpenGL globe
continental_quest_landing.html # Web launcher interface
style.css                    # Landing page styling
script.js                   # Interactive features
requirements.txt            # All project dependencies

🆘 TROUBLESHOOTING:

- If pywebview fails: The app will automatically fallback to browser mode
- If globe.py has import errors: Check that all textures (world.jpg, galaxy.jpg) are present
- If fonts don't load: Check internet connection (uses Google Fonts)

Ready to explore the galaxy through Earth's continents! 🌍🚀
""")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup cannot continue with incompatible Python version")
        return
    
    # Check existing dependencies
    existing_deps_ok = check_existing_dependencies()
    
    # Install integration dependencies
    install_integration_dependencies()
    
    # Check project files
    files_ok = check_project_files()
    
    # Create additional files
    print("\n📝 Creating additional project files...")
    create_requirements_file()
    create_run_script()
    
    # Show final status
    print("\n" + "=" * 60)
    print("📊 SETUP SUMMARY")
    print("=" * 60)
    
    if existing_deps_ok:
        print("✅ Your existing game dependencies are installed")
    else:
        print("⚠️  Some of your existing game dependencies are missing")
        print("   Install them with: pip install pygame PyOpenGL Pillow numpy")
    
    if files_ok:
        print("✅ All required integration files are present")
    else:
        print("❌ Some integration files are missing")
        print("   Make sure all files are in the same directory as globe.py")
    
    print("✅ Setup completed!")
    
    # Show usage guide
    show_usage_guide()
    
    # Ask user what they want to do next
    print("\n🚀 What would you like to do next?")
    print("1. Run the integrated Continental Quest app")
    print("2. Test your existing globe.py")
    print("3. Open the web launcher in browser")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        print("\n🌍 Starting Continental Quest integrated app...")
        try:
            subprocess.run([sys.executable, "continental_quest_app.py"])
        except KeyboardInterrupt:
            print("\n👋 App closed")
        except FileNotFoundError:
            print("❌ continental_quest_app.py not found")
    
    elif choice == '2':
        print("\n🎮 Testing your existing globe.py...")
        try:
            subprocess.run([sys.executable, "globe.py"])
        except KeyboardInterrupt:
            print("\n👋 Globe closed")
        except FileNotFoundError:
            print("❌ globe.py not found")
    
    elif choice == '3':
        print("\n🌐 Opening web launcher in browser...")
        import webbrowser
        html_path = Path(__file__).parent / 'continental_quest_landing.html'
        if html_path.exists():
            webbrowser.open(f'file://{html_path.absolute()}')
        else:
            print("❌ continental_quest_landing.html not found")
    
    else:
        print("\n👋 Setup complete! Use 'python continental_quest_app.py' to run your app.")

if __name__ == '__main__':
    main()
