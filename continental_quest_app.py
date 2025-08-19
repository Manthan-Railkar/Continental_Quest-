#!/usr/bin/env python3
"""
Continental Quest - Integrated Desktop Application
Combines the beautiful web landing page with your existing 3D OpenGL globe
"""

import os
import sys
import threading
import time
import subprocess
from pathlib import Path
import json

# Try to import webview for desktop integration
try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("⚠️  pywebview not installed. Install with: pip install pywebview")

# Import your existing globe functionality
try:
    import globe
    GLOBE_AVAILABLE = True
except ImportError:
    GLOBE_AVAILABLE = False
    print("⚠️  globe.py not found or has import errors")

class ContinentalQuestApp:
    """Main application class that manages both the launcher and 3D globe"""
    
    def __init__(self):
        self.current_continent = None
        self.current_difficulty = 'medium'
        self.game_running = False
        self.web_window = None
        self.game_process = None
        
        # Paths
        self.app_dir = Path(__file__).parent
        self.launcher_path = self.app_dir / 'continental_quest_landing.html'
        
        print("🌍 Continental Quest - Starting Application")
        print(f"📁 App Directory: {self.app_dir}")
        
    def setup_api_bridge(self):
        """Setup JavaScript-Python communication bridge"""
        
        class WebAPI:
            def __init__(self, app_instance):
                self.app = app_instance
            
            def launch_continent(self, continent_name):
                """Called when user selects a continent from the web interface"""
                print(f"🌍 Web: Launching {continent_name}")
                self.app.current_continent = continent_name
                
                # Start the 3D globe with the selected continent
                return self.app.start_3d_globe(continent_name)
            
            def start_game(self, options=None):
                """Start the main 3D globe game"""
                print("\n🚀 [DEBUG] start_game() called from JavaScript!")
                print(f"📊 [DEBUG] Options received: {options}")
                
                continent = 'earth'  # Default to full earth view
                difficulty = 'medium'
                
                if options:
                    continent = options.get('continent', 'earth')
                    difficulty = options.get('difficulty', 'medium')
                
                self.app.current_continent = continent
                self.app.current_difficulty = difficulty
                
                print(f"🎮 Starting 3D Globe: {continent} ({difficulty})")
                result = self.app.start_3d_globe(continent)
                print(f"🔄 [DEBUG] Globe start result: {result}")
                return result
            
            def set_difficulty(self, difficulty):
                """Set game difficulty level"""
                self.app.current_difficulty = difficulty
                print(f"⚡ Difficulty set to: {difficulty}")
                return {'status': 'success', 'difficulty': difficulty}
            
            def get_progress(self, continent=None):
                """Get player progress (mock data for now)"""
                # You can integrate this with your actual game progress later
                progress_data = {
                    'north-america': 75,
                    'south-america': 60,
                    'europe': 85,
                    'africa': 45,
                    'asia': 55,
                    'australia': 90,
                    'antarctica': 25
                }
                
                if continent:
                    return progress_data.get(continent, 0)
                return progress_data
            
            def minimize_launcher(self):
                """Minimize the launcher window"""
                if self.app.web_window:
                    self.app.web_window.minimize()
                return {'status': 'success'}
            
            def close_application(self):
                """Close the entire application"""
                self.app.shutdown()
                return {'status': 'success'}
            
            def test_connection(self):
                """Test if the Python API bridge is working"""
                print("\n🔥 [TEST] Python API connection successful!")
                return {
                    'status': 'success',
                    'message': 'Python API bridge is working!',
                    'timestamp': time.time()
                }
        
        return WebAPI(self)
    
    def start_3d_globe(self, continent='earth'):
        """Start the 3D OpenGL globe"""
        try:
            if not GLOBE_AVAILABLE:
                return {
                    'status': 'error',
                    'message': 'globe.py not available'
                }
            
            # Minimize the web launcher
            if self.web_window:
                self.web_window.minimize()
            
            print(f"🌍 Starting 3D Globe for: {continent}")
            
            # Start the 3D globe in a separate thread to avoid blocking
            globe_thread = threading.Thread(
                target=self.run_globe_with_continent,
                args=(continent,)
            )
            globe_thread.daemon = True
            globe_thread.start()
            
            return {
                'status': 'success',
                'continent': continent,
                'message': f'3D Globe started for {continent}'
            }
            
        except Exception as e:
            print(f"❌ Error starting 3D globe: {e}")
            return {
                'status': 'error',
                'message': f'Failed to start 3D globe: {str(e)}'
            }
    
    def run_globe_with_continent(self, continent):
        """Run the 3D globe with continent-specific settings"""
        try:
            self.game_running = True
            print(f"🎮 3D Globe running for: {continent}")
            
            # You can modify globe.py's main() function or create continent-specific versions
            # For now, we'll run the existing globe
            globe.main()
            
        except Exception as e:
            print(f"❌ Globe error: {e}")
        finally:
            self.game_running = False
            # Restore the launcher window when globe closes
            if self.web_window:
                self.web_window.show()
    
    def create_launcher_files(self):
        """Copy the landing page files to the app directory if needed"""
        required_files = [
            'continental_quest_landing.html',
            'style.css',
            'script.js'
        ]
        
        source_dir = Path("C:\\Users\\Manthan Railkar")
        
        for filename in required_files:
            source_file = source_dir / filename
            target_file = self.app_dir / filename
            
            if source_file.exists() and not target_file.exists():
                try:
                    import shutil
                    shutil.copy2(source_file, target_file)
                    print(f"✅ Copied {filename} to app directory")
                except Exception as e:
                    print(f"⚠️  Could not copy {filename}: {e}")
    
    def run_webview_launcher(self):
        """Run the web launcher using pywebview"""
        if not WEBVIEW_AVAILABLE:
            print("❌ pywebview is not available")
            return False
        
        # Ensure launcher files are available
        self.create_launcher_files()
        
        if not self.launcher_path.exists():
            print(f"❌ Launcher file not found: {self.launcher_path}")
            return False
        
        # Setup API bridge
        api = self.setup_api_bridge()
        
        # Create the webview window
        self.web_window = webview.create_window(
            title='Continental Quest - Choose Your Adventure',
            url=str(self.launcher_path),
            width=1400,
            height=900,
            resizable=True,
            fullscreen=False,
            js_api=api,
            on_top=False
        )
        
        # Add a callback to handle window events
        def on_window_loaded():
            print("\n🔥 [DEBUG] Window loaded - setting up Python integration")
            
            # Inject a direct call to our API
            script = f"""
            // Override the Python interface to force webview mode
            if (window.pythonInterface) {{
                window.pythonInterface.backend_type = 'webview';
                console.log('🔥 [FORCED] Backend type set to webview');
                
                // Override startGame to directly call the Python API
                const originalStartGame = window.pythonInterface.startGame.bind(window.pythonInterface);
                window.pythonInterface.startGame = async function(options) {{
                    console.log('🚀 [OVERRIDE] startGame called, triggering Python...');
                    try {{
                        // Call the Python API directly
                        const result = await pywebview.api.start_game(options);
                        console.log('✅ [PYTHON] Success:', result);
                        return result;
                    }} catch (error) {{
                        console.error('❌ [PYTHON] Error:', error);
                        // If that fails, try the original method
                        return await originalStartGame(options);
                    }}
                }};
            }}
            
            // Also inject a global direct function
            window.directStartGame = function() {{
                console.log('🚀 [DIRECT] Starting game directly!');
                return window.pythonInterface.startGame({{}});
            }};
            
            console.log('🔥 [INJECTED] Python integration enhanced');
            """
            
            try:
                # Wait a bit for the page to fully load
                import time
                time.sleep(1)
                self.web_window.evaluate_js(script)
                print("✅ [DEBUG] Successfully enhanced Python integration")
            except Exception as e:
                print(f"❌ [DEBUG] Failed to enhance integration: {e}")
        
        # Set the callback
        webview.windows[0].events.loaded += on_window_loaded
        
        print("🚀 Starting Continental Quest Launcher...")
        print("🌍 Use the web interface to select your continent!")
        
        # Start the webview (this blocks until window closes)
        webview.start(debug=True)
        
        return True
    
    def run_fallback_launcher(self):
        """Fallback method using system browser"""
        print("🔄 Using fallback browser launcher...")
        
        self.create_launcher_files()
        
        if self.launcher_path.exists():
            import webbrowser
            webbrowser.open(f'file://{self.launcher_path.absolute()}')
            print("🌐 Opened launcher in default browser")
            print("👉 The 3D globe integration works best with the desktop app")
            
            # Keep the app running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("👋 Application closed")
        else:
            print("❌ Launcher files not found")
    
    def shutdown(self):
        """Clean shutdown of the application"""
        print("🛑 Shutting down Continental Quest...")
        
        if self.web_window:
            try:
                self.web_window.destroy()
            except:
                pass
        
        if self.game_process:
            try:
                self.game_process.terminate()
            except:
                pass
        
        # Force exit
        os._exit(0)
    
    def run(self):
        """Main application entry point"""
        print("🌍 Continental Quest - Desktop Application")
        print("=" * 50)
        
        # Check dependencies
        if not GLOBE_AVAILABLE:
            print("❌ Warning: globe.py not available - 3D features may not work")
        
        # Try to run with webview first (best experience)
        if WEBVIEW_AVAILABLE:
            print("🚀 Starting with WebView integration")
            success = self.run_webview_launcher()
        else:
            print("🔄 WebView not available, using browser fallback")
            self.run_fallback_launcher()

def main():
    """Main entry point"""
    try:
        app = ContinentalQuestApp()
        app.run()
    except KeyboardInterrupt:
        print("👋 Application interrupted by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
