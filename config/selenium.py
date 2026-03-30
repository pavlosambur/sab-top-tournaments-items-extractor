"""Selenium configuration: timeouts, retries, selectors."""

SELENIUM_WAIT_TIMEOUT = 10
SELENIUM_RETRIES = 3

# Login page selectors
LOGIN_INPUT_XPATH = '//input[@data-testid="login-form-email"]'
PASSWORD_INPUT_XPATH = '//input[@data-testid="login-form-password"]'
LOGIN_SUBMIT_XPATH = '//button[@data-testid="login-form-sign-in"]'

# 2FA page selectors
TWO_FA_INPUT_XPATH = '//input[@name="otp"]'
TWO_FA_SUBMIT_XPATH = '//button[@type="submit"]'

# Post-login verification
LOGGED_IN_INDICATOR_XPATH = '//img[@data-testid="aside-header-logo-img"]'

# Error indicators
FORM_ERROR_XPATH = '//div[@class="ant-form-item-explain-error"]'

# Widget page selectors
WIDGET_PAGE_LOADED_XPATH = '//div[@data-rbd-droppable-id="ROOT"]'
WIDGET_ITEM_LINK_XPATH = '//a[@data-testid="table-item-name"]'

# Item page selectors
ITEM_PAGE_LOADED_XPATH = '//h5[@data-testid="badge-title-header"]'
ITEM_NAME_XPATH = '//input[@data-testid="create-widget-form-name-input"]'
ITEM_WEB_LINK_XPATH = '//textarea[@data-testid="web-link-input"]'
ITEM_STATUS_XPATH = '//span[@data-testid="status-select-tag-status"]'
