"""API tests for US-1.11 View ATM and branch locations."""

import os
from typing import Any

import allure
import pytest
import requests

from tests.api.epic_1_welcome_page.data.view_ATM_and_branch_locations_data import (
    INVALID_CITY,
    INVALID_PAGE_VALUES,
    INVALID_PAGES,
    INVALID_TYPES,
    REQUIRED_LOCATION_FIELDS,
    REQUIRED_RESPONSE_FIELDS,
    VALID_CITY,
    VALID_LOCATION_TYPES,
    VALID_PAGES,
    VALID_STATUSES,
)

BASE_URL = os.getenv("BASE_URL", "https://api-dev.example.com")
LOCATIONS_ENDPOINT = "/api/locations"


def get_locations(params: dict[str, Any] | None = None) -> requests.Response:
    return requests.get(f"{BASE_URL}{LOCATIONS_ENDPOINT}", params=params, timeout=15)


def assert_base_response_structure(response_data: dict[str, Any]) -> None:
    for field in REQUIRED_RESPONSE_FIELDS:
        assert field in response_data, f"Missing response field: {field}"

    assert isinstance(response_data["items"], list)
    assert isinstance(response_data["page"], int)
    assert isinstance(response_data["size"], int)
    assert isinstance(response_data["totalElements"], int)


def assert_location_structure(location: dict[str, Any]) -> None:
    for field in REQUIRED_LOCATION_FIELDS:
        assert field in location, f"Missing location field: {field}"

    assert isinstance(location["id"], str)
    assert location["type"] in VALID_LOCATION_TYPES
    assert isinstance(location["city"], str)
    assert isinstance(location["locationNumber"], int)
    assert isinstance(location["name"], str)
    assert isinstance(location["address"], str)
    assert isinstance(location["latitude"], int | float)
    assert isinstance(location["longitude"], int | float)
    assert isinstance(location["workingHours"], str)
    assert isinstance(location["todayHours"], str)
    assert location["weekendHours"] is None or isinstance(location["weekendHours"], str)
    assert location["holidayHours"] is None or isinstance(location["holidayHours"], str)
    assert location["status"] in VALID_STATUSES
    assert isinstance(location["isOpen"], bool)


@allure.title("Get locations successfully")
def test_get_locations_success():
    response = get_locations()

    assert response.status_code == 200

    assert_base_response_structure(response.json())


@allure.title("Get locations successfully")
def test_location_items_have_required_structure():
    response = get_locations()

    assert response.status_code == 200

    items = response.json()["items"]
    assert items, "Locations list should not be empty"

    for location in items:
        assert_location_structure(location)


@allure.title("Location response contains required fields")
@pytest.mark.parametrize("location_type", VALID_LOCATION_TYPES)
def test_filter_locations_by_type(location_type):
    response = get_locations({"type": location_type})

    assert response.status_code == 200

    for location in response.json()["items"]:
        assert location["type"] == location_type


@allure.title("Filter locations by city")
def test_filter_locations_by_city():
    response = get_locations({"city": VALID_CITY})

    assert response.status_code == 200

    for location in response.json()["items"]:
        assert location["city"] == VALID_CITY


@allure.title("Filter locations by city and type")
def test_filter_locations_by_city_and_type():
    location_type = "BRANCH"

    response = get_locations({"city": VALID_CITY, "type": location_type})

    assert response.status_code == 200

    for location in response.json()["items"]:
        assert location["city"] == VALID_CITY
        assert location["type"] == location_type


@allure.title("Valid pagination")
@pytest.mark.parametrize("page", VALID_PAGES)
def test_valid_page_values(page):
    response = get_locations({"page": page})

    assert response.status_code == 200
    assert_base_response_structure(response.json())


@allure.title("Valid pagination")
@pytest.mark.parametrize("page", INVALID_PAGES)
def test_invalid_page_values_return_validation_error(page):
    response = get_locations({"page": page})

    assert response.status_code == 422


@allure.title("Invalid page validation")
@pytest.mark.parametrize("page", INVALID_PAGE_VALUES)
def test_invalid_page_type_return_validation_error(page):
    response = get_locations({"page": page})

    assert response.status_code == 422


@allure.title("Invalid page type validation")
@pytest.mark.parametrize("location_type", INVALID_TYPES)
def test_invalid_type_return_validation_error(location_type):
    response = get_locations({"type": location_type})

    assert response.status_code == 422


@allure.title("Invalid location type validation")
def test_invalid_city_returns_empty_list():
    response = get_locations({"city": INVALID_CITY})

    assert response.status_code == 200

    response_data = response.json()
    assert_base_response_structure(response_data)
    assert response_data["items"] == []


@allure.title("Invalid city returns empty result")
def test_locations_are_sorted_by_city_and_location_number():
    response = get_locations()

    assert response.status_code == 200

    items = response.json()["items"]
    actual_order = [(location["city"], location["locationNumber"]) for location in items]
    expected_order = sorted(actual_order, key=lambda item: (item[0], item[1]))

    assert actual_order == expected_order


@allure.title("Locations are sorted correctly")
def test_status_and_is_open_are_consistent():
    response = get_locations()

    assert response.status_code == 200

    for location in response.json()["items"]:
        assert location["isOpen"] == (location["status"] == "OPEN")
