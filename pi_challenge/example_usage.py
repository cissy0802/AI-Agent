"""
Example usage of the Pi Circle Automation script.

This demonstrates how to use the automation programmatically.
"""

from pi_circle_automation import PiCircleAutomation

def example_basic():
    """Basic usage example."""
    print("=== Basic Example ===")
    automation = PiCircleAutomation(headless=False)
    
    try:
        # Draw a circle with default settings
        automation.run(method='js')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        automation.close()


def example_custom_circle():
    """Example with custom circle parameters."""
    print("=== Custom Circle Example ===")
    automation = PiCircleAutomation(headless=False)
    
    try:
        # Draw a custom-sized circle
        automation.run(
            method='js',
            center_x=400,
            center_y=400,
            radius=150,
            num_points=300  # Higher points = smoother circle
        )
    except Exception as e:
        print(f"Error: {e}")
    finally:
        automation.close()


def example_mouse_simulation():
    """Example using mouse simulation method."""
    print("=== Mouse Simulation Example ===")
    automation = PiCircleAutomation(headless=False)
    
    try:
        # Use mouse simulation instead of JavaScript
        automation.run(method='mouse', num_points=100)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        automation.close()


def example_headless():
    """Example running in headless mode."""
    print("=== Headless Mode Example ===")
    automation = PiCircleAutomation(headless=True)
    
    try:
        automation.run(method='js', num_points=200)
        print("Circle drawn! Check the screenshot or result if available.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        automation.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example_type = sys.argv[1].lower()
        
        if example_type == "basic":
            example_basic()
        elif example_type == "custom":
            example_custom_circle()
        elif example_type == "mouse":
            example_mouse_simulation()
        elif example_type == "headless":
            example_headless()
        else:
            print(f"Unknown example: {example_type}")
            print("Available examples: basic, custom, mouse, headless")
    else:
        # Run basic example by default
        print("Running basic example. Use 'python example_usage.py [basic|custom|mouse|headless]' for other examples.")
        example_basic()

