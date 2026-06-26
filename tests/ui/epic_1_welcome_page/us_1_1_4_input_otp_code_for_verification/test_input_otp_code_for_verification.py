import random
import time

import allure
import pytest
from allure_commons.types import Severity as severity_level

from framework.email.otp_client import OtpEmailClient
from framework.ui.pages.registration_contact_info import RegistrationPage


@allure.epic("UI")
@allure.feature("Sign up")
@pytest.mark.ui
class TestSignUp:

    @allure.story("Email verification step with valid OTP")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-28")
    def test_email_verification_step_with_valid_otp(self, page):
        registration_page = RegistrationPage(page)
        registration_page.go_to_contact_info_step()
        registration_page.fill_email("pretty.aqa@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()
        registration_page.click_continue()

        client = OtpEmailClient()
        otp = client.wait_for_otp(recipient="pretty.aqa@gmail.com")

        registration_page.fill_otp(otp)
        registration_page.click_verify()

    @allure.story("Verify incorrect OTP attemps")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-29")
    def test_verify_incorrect_OTP_attempts(self, page):
        registration_page = RegistrationPage(page)
        registration_page.go_to_contact_info_step()
        registration_page.fill_email("alinapetrova@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()
        registration_page.click_continue()
        registration_page.fill_otp("12@456")
        registration_page.click_verify()
        registration_page.expect_otp_error_message("Must contain only digits")

        registration_page.fill_otp("123456")
        registration_page.click_verify()

        registration_page.fill_otp("99999")

    @allure.story("Verify OTP becomes available after countdown ends")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-51")
    def test_verify_otp_becomes_available_after_countdown_ends(self, page):
        registration_page = RegistrationPage(page)
        registration_page.go_to_contact_info_step()
        registration_page.fill_email("alina.petrova@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()
        registration_page.click_continue()

        for otp in ("111111", "222222", "333333", "444444", "555555"):
            registration_page.fill_otp(otp)
            registration_page.click_verify()
            if registration_page.otp_is_locked():
                break

        registration_page.expect_otp_is_locked()
        registration_page.expect_countdown_finished()

    @allure.story("Verify mixed attempts reset after lockout")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-52")
    @pytest.mark.skip(
        reason="email already registered and can't use it twice. This is the only email to retrieve OTP. Waiting for FE to add +"
    )
    def test_verify_mixed_attempts_reset_after_lockout(self, page):
        registration_page = RegistrationPage(page)
        registration_page.go_to_contact_info_step()
        registration_page.fill_email(f"pretty.aqa+{random.randint(1000, 9999)}@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()
        registration_page.click_continue()

        for otp in ("111111", "222222", "333333", "444444", "555555"):
            registration_page.fill_otp(otp)
            registration_page.click_verify()
            if registration_page.otp_is_locked():
                break

        registration_page.expect_otp_is_locked()
        registration_page.expect_countdown_finished()

        registration_page.fill_otp("666666")
        registration_page.click_verify()

        client = OtpEmailClient()
        otp = client.wait_for_otp(recipient="pretty.aqa@gmail.com")

        registration_page.fill_otp(otp)
        registration_page.click_verify()

    @allure.story("Verify entering an expired OTP")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-31")
    @pytest.mark.skip(reason="Waiting time is too long and it is not recommended for automation.")
    def test_verify_entering_an_expired_otp(self, page):
        pass

    @allure.story("Verify invalidation of previous codes")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-32")
    @pytest.mark.skip(
        reason="email already registered and can't use it twice. This is the only email to retrieve OTP. Waiting for FE to add +"
    )
    def test_verify_invalidation_of_previous_codes(self, page):
        registration_page = RegistrationPage(page)
        registration_page.go_to_contact_info_step()
        registration_page.fill_email("pretty.aqa@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()
        registration_page.click_continue()

        client = OtpEmailClient()
        old_otp = client.wait_for_otp(recipient="pretty.aqa@gmail.com")

        page.wait_for_timeout(31000)
        registration_page.click_resend_code()

        registration_page.fill_otp(old_otp)
        registration_page.click_verify()
        registration_page.expect_otp_error_message("Invalid code")

    @allure.story("Verify resend OTP becomes available after countdown")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-55")
    @pytest.mark.skip(
        reason="email already registered and can't use it twice. This is the only email to retrieve OTP. Waiting for FE to add +"
    )
    def test_verify_resend_otp_becomes_available_after_countdown(self, page):
        registration_page = RegistrationPage(page)
        registration_page.go_to_contact_info_step()
        registration_page.fill_email("pretty.aqa@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()
        registration_page.click_continue()

        client = OtpEmailClient()
        otp = client.wait_for_otp(recipient="pretty.aqa@gmail.com")
        registration_page.fill_otp(otp)

        page.wait_for_timeout(31000)
        registration_page.click_resend_code()
        registration_page.expect_click_resend_code_is_not_clickable()
        page.wait_for_timeout(31000)

    @allure.story("Verify block after exceeding 5 resends within 60 minutes")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-34")
    @pytest.mark.skip(
        reason="Cannot automate: CAPTCHA is triggered after multiple OTP resend requests. Test environment does not have "
        "CAPTCHA disabled and only one OTP email (pretty.aqa@gmail.com) is available."
        "This test requires 5 resends within 60 minutes which triggers CAPTCHA. Will be unblocked when CAPTCHA is disabled "
        "for test environment or additional OTP emails are provided."
    )
    def test_verify_block_after_exceeding_5_resends_within_60_minutes(self, page):
        pass

    @allure.story("Verify block after exceeding 10 resends within 24 hours")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-56")
    @pytest.mark.skip(
        reason="Cannot automate: CAPTCHA is triggered after multiple OTP resend requests. Test environment does not have "
        "CAPTCHA disabled and only one OTP email (pretty.aqa@gmail.com) is available."
        "This test requires 5 resends within 60 minutes which triggers CAPTCHA. Will be unblocked when CAPTCHA is disabled "
        "for test environment or additional OTP emails are provided. "
        "Also Waiting time is too long and it is not recommended for automation."
    )
    def test_verify_after_exceeding_10_resends_within_24_hours(self, page):
        pass

    @allure.story("Verify resend becomes available after 60 minutes")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-58")
    @pytest.mark.skip(reason="Waiting time is too long and it is not recommended for automation.")
    def test_verify_resend_becomes_available_after_60_minutes(self, page):
        pass

    @allure.story("Verify storing info for audit and fraud logging")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-59")
    @pytest.mark.skip(
        reason="Cannot automate: requires direct database access to check audit/fraud logs."
        " Database is in private AWS subnet accessible only via SSM tunnel."
    )
    def test_verify_storing_info_for_audit_and_fraud_logging(self, page):
        pass

    @allure.story("Verify solved CAPTCHA allows resending OTP")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-60")
    @pytest.mark.skip(
        reason="Cannot automate: requires solving CAPTCHA which is designed to prevent automation."
        "CAPTCHA is not disabled in test environment."
    )
    def test_verify_solved_captcha_allows_resending_otp(self, page):
        pass

    @allure.story("Verify unsolved CAPTCHA does not allow resending OTP")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-61")
    @pytest.mark.skip(
        reason="Cannot automate: requires solving CAPTCHA which is designed to prevent automation."
        "CAPTCHA is not disabled in test environment."
    )
    def test_verify_unsolved_captcha_does_not_allow_resending_otp(self, page):
        pass

    @allure.story("Verify block after solving CAPTCHA and requesting new OTP again")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-62")
    @pytest.mark.skip(
        reason="Cannot automate: requires solving CAPTCHA which is designed to prevent automation."
        "CAPTCHA is not disabled in test environment."
    )
    def test_verify_block_after_solving_captcha_and_requesting_new_otp_again(self, page):
        pass

    @allure.story("Verify OTP send fails due to service outage")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-63")
    @pytest.mark.skip(
        reason="Frontend does not handle OTP send failure gracefully - "
        "navigates to email verification page even when OTP service is aborted."
    )
    def test_verify_otp_send_fails_due_to_service_outage(self, page):
        registration_page = RegistrationPage(page)
        registration_page.go_to_contact_info_step()
        registration_page.fill_email("alina.petrova@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()

        def handle_route(route):
            if "/otp/send" in route.request.url:
                print("ABORTING OTP")
                route.abort()
            else:
                route.continue_()

        page.route("https://api-dev.pretty-py.andersenlab.dev/**", handle_route)

        registration_page.click_continue()

        time.sleep(5)
        registration_page.expect_otp_error_message("Something went wrong. Please try again later.")
        registration_page.expect_resend_countdown_is_not_started()
        registration_page.expect_resent_code_is_available()

    @allure.story("Verify OTP verification fails due to service outage")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-64")
    @pytest.mark.skip(
        reason="Frontend does not handle OTP send failure gracefully - "
        "navigates to email verification page even when OTP service is aborted."
    )
    def test_verify_otp_verification_fails_due_to_service_outage(self, page):
        registration_page = RegistrationPage(page)
        registration_page.go_to_contact_info_step()
        registration_page.fill_email("alina.petrova@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()
        registration_page.click_continue()

        def handle_route(route):
            if "/otp/verify" in route.request.url:
                print("ABORTING OTP VERIFYING")
                route.abort()
            else:
                route.continue_()

        page.route("https://api-dev.pretty-py.andersenlab.dev/**", handle_route)

        registration_page.fill_otp("123456")
        registration_page.click_verify()

        time.sleep(5)
        registration_page.expect_otp_error_message("Something went wrong. Please try again later.")

    @allure.story("Verify new OTP is needed after leaving the verification page")
    @allure.severity(severity_level.NORMAL)
    @pytest.mark.qase("LP-66")
    @pytest.mark.skip(
        reason="email already registered and can't use it twice. This is the only email to retrieve OTP. Waiting for FE to add +"
    )
    def test_verify_new_otp_is_needed_after_leaving_the_verification_page(self, page):
        registration_page = RegistrationPage(page)
        registration_page.go_to_contact_info_step()
        registration_page.fill_email("pretty.aqa@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()
        registration_page.click_continue()

        client = OtpEmailClient()
        old_otp = client.wait_for_otp(recipient="pretty.aqa@gmail.com")

        registration_page.fill_otp(old_otp)

        page.reload()

        registration_page.go_to_contact_info_step()
        registration_page.fill_email("pretty.aqa@gmail.com")
        registration_page.fill_phone("+359 881234567")
        registration_page.click_continue()
        registration_page.fill_address_step_with_valid_data()
        registration_page.click_continue()

        registration_page.fill_otp(old_otp)
        registration_page.click_verify()
        registration_page.expect_otp_error_message("Invalid code")
