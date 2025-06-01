import pytest
import time

# Global configuration for route interception
ROUTE_INTERCEPTION = False  # Set to True for mocked form submissions

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="function")
def page(page):
    """Customize page fixture if needed"""
    page.set_default_timeout(10000)
    return page

def setup_form_submission_mock(page, success=True, delay_ms=1000):
    """
    Helper function to mock form submissions using route interception.
    
    Args:
        page: Playwright page object
        success: Boolean - whether to simulate successful or failed submission
        delay_ms: Integer - delay in milliseconds to simulate server response time
    
    Usage:
        setup_form_submission_mock(page, success=True, delay_ms=500)
    """
    if not ROUTE_INTERCEPTION:
        print("Route interception disabled - using real form submission")
        return
    
    def handle_form_submission(route):
        # Simulate server delay
        if delay_ms > 0:
            time.sleep(delay_ms / 1000)
        
        if success:
            # Simulate successful submission
            route.fulfill(
                status=200,
                content_type="application/json",
                headers={"Access-Control-Allow-Origin": "*"},
                body='{"success": true, "data": {"message": "Thank you! Your message has been sent."}}'
            )
        else:
            # Simulate failed submission
            route.fulfill(
                status=400,
                content_type="application/json", 
                headers={"Access-Control-Allow-Origin": "*"},
                body='{"success": false, "data": {"message": "There was an error sending your message."}}'
            )
    # Intercept common form submission endpoints
    page.route("**/wp-admin/admin-ajax.php", handle_form_submission)
    # Generic form handlers
    page.route("**/contact/**", handle_form_submission)
    page.route("**/submit/**", handle_form_submission)
    page.route("**/send/**", handle_form_submission)
    print(f"Form submission mocking enabled - success: {success}, delay: {delay_ms}ms")

def verify_form_submission(page, expected_success=True, timeout=5000):
    """
    Verify form submission result based on ROUTE_INTERCEPTION setting.
    
    Args:
        page: Playwright page object
        expected_success: Boolean - whether to expect successful or failed submission
        timeout: Integer - maximum time to wait for response (default 5000ms)
    
    Returns:
        bool: True if verification passed, False otherwise
    
    Usage:
        verify_form_submission(page, expected_success=True, timeout=3000)
    """
    try:
        if ROUTE_INTERCEPTION:
            # Mocked submission
            page.wait_for_timeout(1000)
            current_url = page.url
            if expected_success:
                assert "contact" in current_url.lower(), "Should remain on contact page after mocked submission"
                print("Mocked successful form submission verified - remained on contact page")
                return True
            else:
                assert "contact" in current_url.lower(), "Should remain on contact page after mocked failed submission"
                print("Mocked failed form submission verified - remained on contact page")
                return False
        else:
            # For real submissions, check for actual page redirection
            if expected_success:
                # Wait for redirection to thank you page
                page.wait_for_url("**/thank-you/**", timeout=timeout)
                current_url = page.url
                assert "thank-you" in current_url.lower(), f"Expected thank-you page, got: {current_url}"
                assert "wearenotch.com" in current_url, f"Expected wearenotch.com domain, got: {current_url}"
                print("Real successful form submission verified - redirected to thank-you page")
                return True
            else:
                # For failed real submissions
                page.wait_for_timeout(2000)
                current_url = page.url
                assert "contact" in current_url.lower(), "Should remain on contact page after failed submission"
                print("Real failed form submission verified - remained on contact page")
                return True
                
    except Exception as e:
        print(f"Form submission verification failed: {e}")
        return False
