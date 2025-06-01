class ContactPage:
    def __init__(self, page):
        self.page = page
        self.url = "https://wearenotch.com/contact/"
        
        # Form field selectors
        self.first_name = 'input[name="input_5"]'
        self.last_name = 'input[name="input_18"]'
        self.email = 'input[name="input_17"]'
        self.phone = 'input[name="input_8"]'
        self.company = 'input[name="input_11"]'
        self.project_details = 'textarea[name="input_15"]'
        
        # Dropdown selectors
        # self.hear_about_container = '#input_2_9_chosen'
        self.hear_about_trigger = '#input_2_9_chosen a.chosen-single'
        self.hear_about_option = lambda value: f'#input_2_9_chosen .chosen-results li:has-text("{value}")'
        # self.budget_container = '#input_2_12_chosen'
        self.budget_trigger = '#input_2_12_chosen a.chosen-single'
        self.budget_option = lambda value: f'#input_2_12_chosen .chosen-results li:has-text("{value}")'
        
        # Checkbox and submit
        self.consent_checkbox = '#input_2_16_1'
        self.submit_button = '#gform_submit_button_2'
        
        # Service checkboxes
        self.service_checkbox_by_label = lambda label: f'label:has-text("{label}") >> input[type="checkbox"]'
        
        # Accept cookie button
        self.cookie_accept_button = 'button.cky-btn.cky-btn-accept[data-cky-tag="accept-button"]'

    def handle_cookie_consent(self, timeout=5000):
        """
        Handle cookie consent popup if it appears.
        
        Args:
            timeout: Maximum time to wait for cookie popup (default 5000ms)
        
        Returns:
            bool: True if cookie popup was handled, False otherwise
        """
        try:
            cookie_button = self.page.locator(self.cookie_accept_button)
            
            if cookie_button.is_visible(timeout=timeout):
                print("Cookie consent popup detected - clicking Accept All")
                cookie_button.click()
                self.page.wait_for_timeout(1000)
                return True
            else:
                print("No cookie consent popup found")
                return False
                
        except Exception as e:
            print(f"Cookie consent handling failed: {e}")
            return False

    def navigate(self):
        self.page.goto(self.url)
        self.page.wait_for_timeout(500)
        self.handle_cookie_consent()

    def fill_required_fields(self, first_name="Test", last_name="Test", email="test.test@example.com"):
        self.page.fill(self.first_name, first_name)
        self.page.fill(self.last_name, last_name)
        self.page.fill(self.email, email)

    def fill_optional_fields(self, phone=None, company=None, project_details=None):
        if phone:
            self.page.fill(self.phone, phone)
        if company:
            self.page.fill(self.company, company)
        if project_details:
            self.page.fill(self.project_details, project_details)

    def check_consent(self):
        self.page.check(self.consent_checkbox)

    def select_hear_about(self, value="Google"):
        self.page.click(self.hear_about_trigger)
        self.page.click(self.hear_about_option(value))

    def select_budget(self, value="Up to €50.000"):
        self.page.click(self.budget_trigger)
        self.page.click(self.budget_option(value))

    def check_service_by_name(self, services):
        for service in services:
            label_locator = self.page.locator(f'fieldset#field_2_14 label', has_text=service)
            if label_locator.count() == 0:
                raise Exception(f"Label for service '{service}' not found.")
            label_locator.first.click()

    def submit(self):
        self.page.click(self.submit_button)
