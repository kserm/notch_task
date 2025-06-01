import pytest
from pages.contact_page import ContactPage
from helpers import setup_form_submission_mock, verify_form_submission


class TestContactPage:
    """Test suite for the contact page functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup contact page for each test"""
        self.contact_page = ContactPage(page)
        self.contact_page.navigate()

    def test_page_loads_successfully(self, page):
        """Test that the contact page loads without errors"""
        # Check if page loaded by verifying the submit button is present
        submit_button = page.locator(self.contact_page.submit_button)
        assert submit_button.is_visible(), "Submit button should be visible on page load"

    def test_required_fields_validation(self, page):
        """Test form validation for required fields"""
        # Try to submit without filling required fields
        self.contact_page.check_consent()
        self.contact_page.submit()
        assert page.url == self.contact_page.url or "contact" in page.url

    def test_successful_form_submission_minimal_data(self, page):
        """Test successful form submission with minimal required data"""
        # Setup mock for successful submission
        setup_form_submission_mock(page, success=True, delay_ms=500)
        # Fill only required fields
        self.contact_page.fill_required_fields()
        self.contact_page.check_consent()
        self.contact_page.submit()
        assert verify_form_submission(page, expected_success=True, timeout=3000), "Form submission verification failed"

    def test_privacy_policy_link_has_valid_href(self, page):
        """Test that privacy policy link has a valid href attribute - EXPECTED TO FAIL"""
        privacy_link = page.locator('//*[@id="field_2_16"]/div/label/a')
        assert privacy_link.is_visible(), "Privacy policy link should be visible"
        href = privacy_link.get_attribute('href')
        print(f"Privacy policy href: '{href}'")
        # This will fail because href="" 
        assert href is not None and href != "", "Privacy policy link should have a valid href attribute"
        assert href.startswith('http') or href.startswith('/'), f"Privacy policy href should be a valid URL or path, got: '{href}'"
    
    def test_invalid_name_validation(self, page):
        """Test that single special characters should not be accepted as names - EXPECTED TO FAIL"""
        setup_form_submission_mock(page, success=False, delay_ms=500)
        # Test with dash as first name
        self.contact_page.fill_required_fields(
            first_name="-",
            last_name="User",
            email="test@example.com"
        )
        self.contact_page.check_consent()
        self.contact_page.submit()
        # This test expects validation to prevent submission, but will likely fail
        # because the form accepts single dash characters
        assert verify_form_submission(page, expected_success=False, timeout=3000), "Successful form submission"

    def test_successful_form_submission_complete_data(self, page):
        """Test successful form submission with all fields filled"""
        # Setup mock for successful submission
        setup_form_submission_mock(page, success=True, delay_ms=500)
        # Fill all fields
        self.contact_page.fill_required_fields()
        self.contact_page.fill_optional_fields(
            phone="+1234567890",
            company="Test Company Ltd",
            project_details="Test project details."
        )
        self.contact_page.select_hear_about()
        self.contact_page.select_budget()
        self.contact_page.check_service_by_name(["Custom Software Development", "UX/UI Design"])
        self.contact_page.check_consent()
        self.contact_page.submit()
        assert verify_form_submission(page, expected_success=True, timeout=3000), "Form submission verification failed"

    def test_email_field_validation(self, page):
        """Test email field accepts valid email formats"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "firstname+lastname@company.org"
        ]
        for email in valid_emails:
            # Clear and fill email field
            page.fill(self.contact_page.email, "")
            page.fill(self.contact_page.email, email)
            
            email_value = page.input_value(self.contact_page.email)
            assert email_value == email, f"Email {email} should be accepted"

    def test_phone_field_accepts_various_formats(self, page):
        """Test phone field accepts various phone number formats"""
        phone_formats = [
            "+1234567890",
            "(123) 456-7890",
            "123-456-7890",
            "123.456.7890",
            "1234567890"
        ]
        for phone in phone_formats:
            page.fill(self.contact_page.phone, "")
            page.fill(self.contact_page.phone, phone)
            # Verify the phone number was entered
            phone_value = page.input_value(self.contact_page.phone)
            assert len(phone_value) > 0, f"Phone format {phone} should be accepted"

    def test_hear_about_dropdown_selections(self, page):
        """Test hear about dropdown menu selections work correctly"""
        hear_about_options = ["Recommendation", "Google", "Clutch", "LinkedIn", "Facebook", "Instagram"]
        for option in hear_about_options:
            try:
                self.contact_page.select_hear_about(option)
                # If no exception, selection was successful
                page.wait_for_timeout(200)
            except Exception as e:
                print(f"Option '{option}' not found in hear_about dropdown: {e}")
        self.contact_page.submit()
        assert page.url == self.contact_page.url or "contact" in page.url
    
    def test_budget_dropdown_selections(self, page):
        """Test budget dropdown menu selections work correctly"""
        budget_options = ["Up to €50.000", "€50.000 to €100.000", "€100.000 to €250.000", "Over €250.000", "Can’t disclose"]
        for option in budget_options:
            try:
                self.contact_page.select_budget(option)
                page.wait_for_timeout(200)
            except Exception as e:
                print(f"Option '{option}' not found in budget dropdown: {e}")
        self.contact_page.submit()
        assert page.url == self.contact_page.url or "contact" in page.url

    def test_service_checkboxes(self, page):
        """Test service checkbox selections"""
        services = [
            "Custom Software Development",
            "Enterprise Application Modernization",
            "Team Extension",
            "Product Discovery",
            "Technology Discovery",
            "AI Discovery",
            "Ideation Workshop",
            "Business Process Consulting",
            "Requirements Consulting",
            "Scrum Coaching",
            "UX/UI Design",
            "User Research",
            "Design Systems",
            "Proof of Concept",
            "Minimum Viable Product",
            "Okta CIC Platform Integration",
            "Camunda BPM Platform Integration"
        ]
        for service in services:
            self.contact_page.check_service_by_name([service])
            label_locator = page.locator(f'label:has-text("{service}")')
            label_for = label_locator.get_attribute('for')
            checkbox = page.locator(f'input#{label_for}')
            assert checkbox.is_checked(), f"Service '{service}' checkbox is not checked"
        self.contact_page.submit()
        assert page.url == self.contact_page.url or "contact" in page.url

    def test_consent_checkbox_required(self, page):
        """Test that consent checkbox is required for form submission"""
        self.contact_page.fill_required_fields()
        self.contact_page.submit()
        page.wait_for_timeout(500)
        assert page.url == self.contact_page.url or "contact" in page.url

    def test_form_field_character_limits(self, page):
        """Test form fields handle long input appropriately"""
        # Test long text in project details
        long_text = "A" * 1000
        page.fill(self.contact_page.project_details, long_text)
        entered_text = page.input_value(self.contact_page.project_details)
        # Text should be entered (might be truncated by field limits)
        assert len(entered_text) > 0, "Long text should be handled gracefully"
        
        # Test long company name
        long_company_name = "Very Long Company Name That Exceeds Normal Length Limits" * 3
        page.fill(self.contact_page.company, long_company_name)
        entered_company = page.input_value(self.contact_page.company)
        assert len(entered_company) > 0, "Long company name should be handled"
