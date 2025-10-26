"""
A tool for controlling a web browser using the Gemini Computer Use API.

This tool allows the agent to perform tasks like data entry, automated testing,
and web research by controlling a web browser. It uses the Gemini Computer Use
API to "see" the screen and "act" by generating UI actions like mouse clicks
and keyboard inputs.
"""

import argparse
import sys
import os
import time
from playwright.sync_api import sync_playwright
import google.generativeai as genai

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.gemini_api.client import GeminiApiClient


def denormalize_x(x, screen_width):
    """Convert normalized x coordinate (0-1000) to actual pixel coordinate."""
    return int(x / 1000 * screen_width)


def denormalize_y(y, screen_height):
    """Convert normalized y coordinate (0-1000) to actual pixel coordinate."""
    return int(y / 1000 * screen_height)


def execute_function_calls(candidate, page, screen_width, screen_height):
    results = []
    function_calls = []
    for part in candidate.content.parts:
        if part.function_call:
            function_calls.append(part.function_call)

    for function_call in function_calls:
        action_result = {}
        fname = function_call.name
        args = function_call.args
        print(f"  -> Executing: {fname}")

        try:
            if fname == "open_web_browser":
                pass  # Already open
            elif fname == "click_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                page.mouse.click(actual_x, actual_y)
            elif fname == "type_text_at":
                actual_x = denormalize_x(args["x"], screen_width)
                actual_y = denormalize_y(args["y"], screen_height)
                text = args["text"]
                press_enter = args.get("press_enter", False)

                page.mouse.click(actual_x, actual_y)
                # Improved clear (Control+A, Backspace for cross-platform)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(text)
                if press_enter:
                    page.keyboard.press("Enter")
            else:
                print(f"Warning: Unimplemented or custom function {fname}")

            # Wait for potential navigations/renders
            page.wait_for_load_state(timeout=5000)
            time.sleep(1)

        except Exception as e:
            print(f"Error executing {fname}: {e}")
            action_result = {"error": str(e)}

        results.append((fname, action_result))

    return results


def get_function_responses(page, results):
    screenshot_bytes = page.screenshot(type="png")
    current_url = page.url
    function_responses = []
    for name, result in results:
        response_data = {"url": current_url}
        response_data.update(result)
        function_responses.append(
            genai.types.FunctionResponse(
                name=name,
                response=response_data,
                parts=[
                    genai.types.FunctionResponsePart(
                        inline_data=genai.types.FunctionResponseBlob(
                            mime_type="image/png", data=screenshot_bytes
                        )
                    )
                ],
            )
        )
    return function_responses


def main():
    """The main entry point for the GeminiComputerUse tool."""
    parser = argparse.ArgumentParser(
        description="Controls a web browser using the Gemini Computer Use API."
    )
    parser.add_argument(
        "task",
        help="The task to perform, e.g., 'fill out the form on example.com'",
    )
    args = parser.parse_args()

    SCREEN_WIDTH = 1440
    SCREEN_HEIGHT = 900

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
    )
    page = context.new_page()
    page.goto("https://www.google.com")

    client = GeminiApiClient()
    model = genai.GenerativeModel("gemini-2.0-pro")

    initial_screenshot = page.screenshot(type="png")
    contents = [
        {
            "role": "user",
            "parts": [
                {"text": args.task},
                {
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": initial_screenshot,
                    }
                },
            ],
        }
    ]

    turn_limit = 5
    for i in range(turn_limit):
        print(f"\n--- Turn {i+1} ---")
        print("Thinking...")
        response = model.generate_content(contents)

        candidate = response.candidates[0]
        contents.append(candidate.content)

        has_function_calls = any(part.function_call for part in candidate.content.parts)
        if not has_function_calls:
            text_response = " ".join(
                [part.text for part in candidate.content.parts if part.text]
            )
            print("Agent finished:", text_response)
            break

        print("Executing actions...")
        results = execute_function_calls(candidate, page, SCREEN_WIDTH, SCREEN_HEIGHT)

        print("Capturing state...")
        function_responses = get_function_responses(page, results)

        contents.append(
            genai.types.Content(
                role="user",
                parts=[
                    genai.types.Part(function_response=fr) for fr in function_responses
                ],
            )
        )

    browser.close()
    playwright.stop()


if __name__ == "__main__":
    main()
