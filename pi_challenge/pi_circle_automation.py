"""
Pi Day Challenge Circle Automation
Automates drawing a perfect circle in the Pi Day Challenge game
to achieve the highest possible ranking (S rank).

Game URL: https://yage.ai/genai/pi.html
"""

import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Try to import webdriver-manager for automatic ChromeDriver management
try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False


class PiCircleAutomation:
    def __init__(self, headless=False):
        """
        Initialize the automation with Chrome WebDriver.
        
        Args:
            headless: If True, run browser in headless mode (faster but you won't see it)
        """
        self.driver = None
        self.headless = headless
        self.game_url = "https://yage.ai/genai/pi.html"
        
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Use webdriver-manager if available for automatic ChromeDriver management
            if WEBDRIVER_MANAGER_AVAILABLE:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                self.driver = webdriver.Chrome(options=chrome_options)
            
            # Hide webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"Error setting up driver: {e}")
            print("Make sure ChromeDriver is installed and in your PATH")
            if not WEBDRIVER_MANAGER_AVAILABLE:
                print("Or install it via: pip install webdriver-manager")
            return False
    
    def open_game(self):
        """Navigate to the Pi Day Challenge game."""
        if not self.driver:
            if not self.setup_driver():
                return False
        
        print(f"Opening game: {self.game_url}")
        self.driver.get(self.game_url)
        time.sleep(2)  # Wait for page to load
        
        # Wait for the canvas or drawing area to be available
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "canvas"))
            )
            print("Game loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            # Try to find any drawing element
            try:
                canvas = self.driver.find_element(By.TAG_NAME, "canvas")
                if canvas:
                    print("Canvas found!")
                    return True
            except:
                pass
            return False
    
    def get_canvas_info(self):
        """
        Get canvas element and its dimensions.
        Returns canvas element and its size, or None if not found.
        """
        try:
            canvas = self.driver.find_element(By.TAG_NAME, "canvas")
            canvas_size = canvas.size
            canvas_location = canvas.location
            
            # Get actual canvas dimensions from JavaScript
            canvas_width = self.driver.execute_script(
                "return arguments[0].width;", canvas
            )
            canvas_height = self.driver.execute_script(
                "return arguments[0].height;", canvas
            )
            
            print(f"Canvas found: {canvas_width}x{canvas_height}")
            return canvas, canvas_width, canvas_height, canvas_location
        except Exception as e:
            print(f"Error finding canvas: {e}")
            return None, None, None, None
    
    def draw_circle_with_js(self, center_x=None, center_y=None, radius=None, num_points=200):
        """
        Draw a perfect circle directly on the canvas using JavaScript.
        This is the most precise method.
        
        Args:
            center_x: X coordinate of circle center (None = use canvas center)
            center_y: Y coordinate of circle center (None = use canvas center)
            radius: Circle radius (None = use 40% of canvas width)
            num_points: Number of points to draw (more = smoother but slower)
        """
        canvas, canvas_width, canvas_height, canvas_location = self.get_canvas_info()
        
        if not canvas:
            print("Could not find canvas element")
            return False
        
        # Use defaults if not specified
        if center_x is None:
            center_x = canvas_width / 2
        if center_y is None:
            center_y = canvas_height / 2
        if radius is None:
            radius = min(canvas_width, canvas_height) * 0.35  # 35% of smaller dimension
        
        print(f"Drawing circle: center=({center_x:.1f}, {center_y:.1f}), radius={radius:.1f}, points={num_points}")
        
        # JavaScript code to draw a perfect circle on canvas
        draw_script = f"""
        var canvas = arguments[0];
        var ctx = canvas.getContext('2d');
        
        // Clear canvas first (optional - comment out if you want to keep existing drawings)
        // ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        var centerX = {center_x};
        var centerY = {center_y};
        var radius = {radius};
        var numPoints = {num_points};
        
        // Set drawing style
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        
        // Begin drawing path
        ctx.beginPath();
        
        // Draw circle using parametric equations
        for (var i = 0; i <= numPoints; i++) {{
            var angle = (2 * Math.PI * i) / numPoints;
            var x = centerX + radius * Math.cos(angle);
            var y = centerY + radius * Math.sin(angle);
            
            if (i === 0) {{
                ctx.moveTo(x, y);
            }} else {{
                ctx.lineTo(x, y);
            }}
        }}
        
        // Close the path and stroke
        ctx.closePath();
        ctx.stroke();
        
        // Trigger any necessary events (mousemove, mouseup, etc.) that the game might listen to
        var event = new Event('mousemove', {{ bubbles: true }});
        canvas.dispatchEvent(event);
        """
        
        try:
            self.driver.execute_script(draw_script, canvas)
            print("Circle drawn successfully!")
            time.sleep(0.5)  # Brief wait
            
            # Trigger mouse events via JavaScript to make the game recognize the drawing
            # This is fast and doesn't redraw since we're just dispatching events
            if not self.trigger_mouse_events_js(canvas, center_x, center_y, radius, num_points=20):
                # Fallback: if JS events don't work, try fast mouse simulation
                print("Trying fast mouse simulation as fallback...")
                self.quick_mouse_simulation(canvas, center_x, center_y, radius, num_points=30)
            
            return True
        except Exception as e:
            print(f"Error drawing circle: {e}")
            return False
    
    def trigger_mouse_events_js(self, canvas, center_x, center_y, radius, num_points=20):
        """
        Trigger mouse events via JavaScript to make the game recognize the drawing.
        This is fast and doesn't redraw - just dispatches events.
        """
        try:
            # JavaScript to dispatch mouse events along the circle path
            trigger_events_script = f"""
            var canvas = arguments[0];
            var centerX = {center_x};
            var centerY = {center_y};
            var radius = {radius};
            var numPoints = {num_points};
            
            // Get bounding rect for accurate coordinate calculation
            var rect = canvas.getBoundingClientRect();
            
            // Trigger mousedown at start point
            var startX = centerX + radius;
            var startY = centerY;
            var mouseDownEvent = new MouseEvent('mousedown', {{
                bubbles: true,
                cancelable: true,
                clientX: rect.left + startX,
                clientY: rect.top + startY,
                button: 0
            }});
            canvas.dispatchEvent(mouseDownEvent);
            
            // Trigger mousemove events along the circle path (minimal points for speed)
            for (var i = 1; i <= numPoints; i++) {{
                var angle = (2 * Math.PI * i) / numPoints;
                var x = centerX + radius * Math.cos(angle);
                var y = centerY + radius * Math.sin(angle);
                
                var mouseMoveEvent = new MouseEvent('mousemove', {{
                    bubbles: true,
                    cancelable: true,
                    clientX: rect.left + x,
                    clientY: rect.top + y,
                    button: 0
                }});
                canvas.dispatchEvent(mouseMoveEvent);
            }}
            
            // Trigger mouseup at end point (same as start for a complete circle)
            var mouseUpEvent = new MouseEvent('mouseup', {{
                bubbles: true,
                cancelable: true,
                clientX: rect.left + startX,
                clientY: rect.top + startY,
                button: 0
            }});
            canvas.dispatchEvent(mouseUpEvent);
            
            // Also trigger click event which some games use
            var clickEvent = new MouseEvent('click', {{
                bubbles: true,
                cancelable: true,
                clientX: rect.left + startX,
                clientY: rect.top + startY,
                button: 0
            }});
            canvas.dispatchEvent(clickEvent);
            """
            
            self.driver.execute_script(trigger_events_script, canvas)
            print("Mouse events triggered (fast)")
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"Error triggering mouse events: {e}")
            return False
    
    def quick_mouse_simulation(self, canvas, center_x, center_y, radius, num_points=30):
        """
        Quick mouse simulation - traces the circle very fast for game recognition.
        Uses minimal points and no delays for speed.
        """
        try:
            # Calculate circle points
            points = []
            for i in range(num_points + 1):
                angle = 2 * math.pi * i / num_points
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            
            # Get canvas location for accurate positioning
            canvas_location = canvas.location
            
            # Convert points to JavaScript array format
            points_js = "[" + ", ".join([f"[{x}, {y}]" for x, y in points]) + "]"
            
            # Use JavaScript to dispatch mouse events quickly
            # This simulates mouse movement but doesn't actually draw since circle is already drawn
            trace_script = f"""
            var canvas = arguments[0];
            var points = {points_js};
            var rect = canvas.getBoundingClientRect();
            
            // Trigger mousedown at start
            var mouseDown = new MouseEvent('mousedown', {{
                bubbles: true,
                cancelable: true,
                clientX: rect.left + points[0][0],
                clientY: rect.top + points[0][1],
                button: 0,
                buttons: 1
            }});
            canvas.dispatchEvent(mouseDown);
            
            // Rapidly trigger mousemove events
            for (var i = 1; i < points.length; i++) {{
                var mouseMove = new MouseEvent('mousemove', {{
                    bubbles: true,
                    cancelable: true,
                    clientX: rect.left + points[i][0],
                    clientY: rect.top + points[i][1],
                    button: 0,
                    buttons: 1
                }});
                canvas.dispatchEvent(mouseMove);
            }}
            
            // Trigger mouseup at end
            var mouseUp = new MouseEvent('mouseup', {{
                bubbles: true,
                cancelable: true,
                clientX: rect.left + points[0][0],
                clientY: rect.top + points[0][1],
                button: 0,
                buttons: 0
            }});
            canvas.dispatchEvent(mouseUp);
            """
            
            self.driver.execute_script(trace_script, canvas)
            print("Fast mouse simulation completed")
            time.sleep(0.2)
            return True
        except Exception as e:
            print(f"Error in quick mouse simulation: {e}")
            return False
    
    def simulate_mouse_events_on_canvas(self, canvas, center_x, center_y, radius, num_points=50):
        """
        Simulate mouse events on the canvas to trigger game recognition.
        Uses fewer points for speed while maintaining quality.
        NOTE: This method actually draws with mouse, which may draw a second circle.
        """
        try:
            actions = ActionChains(self.driver)
            
            # Move to canvas first
            actions.move_to_element(canvas)
            actions.perform()
            time.sleep(0.5)
            
            # Calculate circle points
            points = []
            for i in range(num_points + 1):
                angle = 2 * math.pi * i / num_points
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            
            # Move to starting point
            start_x = points[0][0]
            start_y = points[0][1]
            
            # Convert canvas coordinates to screen coordinates
            canvas_location = canvas.location
            screen_x = canvas_location['x'] + start_x
            screen_y = canvas_location['y'] + start_y
            
            actions.move_to_element_with_offset(canvas, start_x - canvas.size['width']/2, 
                                               start_y - canvas.size['height']/2)
            actions.click_and_hold()
            
            # Draw circle by moving through points
            for x, y in points[1:]:
                offset_x = x - canvas.size['width']/2
                offset_y = y - canvas.size['height']/2
                actions.move_to_element_with_offset(canvas, offset_x, offset_y)
                time.sleep(0.01)  # Small delay for smoothness
            
            actions.release()
            actions.perform()
            
            
            print("Mouse events simulated")
        except Exception as e:
            print(f"Error simulating mouse events: {e}")
            # This is optional, the JS drawing should work on its own
    
    def draw_circle_with_mouse(self, center_x=None, center_y=None, radius=None, num_points=100):
        """
        Draw a circle by simulating mouse movements.
        Alternative method if JavaScript drawing doesn't work.
        """
        canvas, canvas_width, canvas_height, canvas_location = self.get_canvas_info()
        
        if not canvas:
            print("Could not find canvas element")
            return False
        
        if center_x is None:
            center_x = canvas_width / 2
        if center_y is None:
            center_y = canvas_height / 2
        if radius is None:
            radius = min(canvas_width, canvas_height) * 0.35
        
        print(f"Drawing circle with mouse simulation: center=({center_x:.1f}, {center_y:.1f}), radius={radius:.1f}")
        
        actions = ActionChains(self.driver)
        
        # Calculate circle points
        points = []
        for i in range(num_points + 1):
            angle = 2 * math.pi * i / num_points
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        
        # Move to starting point and begin drawing
        start_x = points[0][0]
        start_y = points[0][1]
        
        # Scroll canvas into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", canvas)
        time.sleep(0.5)
        
        # Click and hold at starting point
        actions.move_to_element(canvas)
        actions.move_by_offset(start_x - canvas_width/2, start_y - canvas_height/2)
        actions.click_and_hold()
        
        # Draw circle
        for x, y in points[1:]:
            offset_x = x - center_x
            offset_y = y - center_y
            actions.move_by_offset(offset_x, offset_y)
            time.sleep(0.02)  # Small delay for smooth drawing
        
        actions.release()
        actions.perform()
        
        print("Circle drawn with mouse simulation!")
        time.sleep(1)
        return True
    
    def wait_for_result(self, timeout=10):
        """Wait for the game to calculate and display the result."""
        print("Waiting for game to process...")
        time.sleep(timeout)
        
        # Try to find and display the result
        try:
            # Look for common result indicators (adjust selectors based on actual game)
            result_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'S') or contains(text(), 'Rank') or contains(text(), 'Score')]")
            if result_elements:
                for elem in result_elements:
                    print(f"Found result: {elem.text}")
        except:
            pass
    
    def run(self, method='js', **kwargs):
        """
        Main method to run the automation.
        
        Args:
            method: 'js' for JavaScript drawing, 'mouse' for mouse simulation
            **kwargs: Additional parameters for draw_circle methods
        """
        if not self.open_game():
            print("Failed to open game")
            return False
        
        # Allow user to position/click on canvas if needed
        if not self.headless:
            print("\nGame is ready. You have 5 seconds to click on the canvas if needed...")
            print("(Press Ctrl+C to skip waiting)")
            try:
                time.sleep(5)
            except KeyboardInterrupt:
                print("\nSkipping wait...")
        
        # Draw the circle
        if method == 'js':
            success = self.draw_circle_with_js(**kwargs)
        else:
            success = self.draw_circle_with_mouse(**kwargs)
        
        if success:
            self.wait_for_result()
            if not self.headless:
                print("\nCircle drawing complete! Check the game for your ranking.")
                print("Press Enter to close the browser...")
                input()
        
        return success
    
    def close(self):
        """Close the browser and cleanup."""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automate circle drawing in Pi Day Challenge')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--method', choices=['js', 'mouse'], default='js',
                       help='Drawing method: js (JavaScript) or mouse (mouse simulation)')
    parser.add_argument('--radius', type=float, default=None,
                       help='Circle radius (default: 35%% of canvas size)')
    parser.add_argument('--center-x', type=float, default=None,
                       help='X coordinate of circle center (default: canvas center)')
    parser.add_argument('--center-y', type=float, default=None,
                       help='Y coordinate of circle center (default: canvas center)')
    parser.add_argument('--points', type=int, default=200,
                       help='Number of points for circle (default: 200, more = smoother)')
    
    args = parser.parse_args()
    
    automation = PiCircleAutomation(headless=args.headless)
    
    try:
        automation.run(
            method=args.method,
            center_x=args.center_x,
            center_y=args.center_y,
            radius=args.radius,
            num_points=args.points
        )
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        automation.close()


if __name__ == "__main__":
    main()
