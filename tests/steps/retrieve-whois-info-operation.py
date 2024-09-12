from behave import given, when, then
from behave.runner import Context
from hamcrest import assert_that, has_entries, has_key

from mocks.MockWhoisClient import MockWhoisClient
from wilde.model.LocationData import LocationData
from wilde.plugins.whois.operation.RetrieveWhoisInfoOperation import RetrieveWhoisInfoOperation

# This should be moved to a fixture
_PREVIOUS_KEYS: dict[str, str] = {"a": "1", "b": "2", "c": "3"}
_EXPECTED_KEYS: list[str] = ["Whois IANA#status", "Whois Refer#domain name"]
_IANA_URL: str = "whois.iana.org"
_REFER_URL: str = "whois.publicinterestregistry.org"
_MOCK_WHOIS_IANA_DATA_PATH: str = "tests/data/mock_org_whois_info_iana.txt"
_MOCK_WHOIS_REFER_DATA_PATH: str = "tests/data/mock_unicef_whois_info_refer.txt"
_DOMAIN: str = "unicef.org"


@given("I have an empty LocationData")
def step_impl(context: Context):
    context.location_data = LocationData(_DOMAIN, {})


@given("I have a LocationData with existing data")
def step_impl(context: Context):
    context.location_data = LocationData(_DOMAIN, _PREVIOUS_KEYS)


@when("I run the RetrieveWhoisInfoOperation for the location")
def step_impl(context: Context):
    whois_client = MockWhoisClient()

    domain = context.location_data.location
    whois_client.set_domain_whois_from_file(domain, _IANA_URL, _MOCK_WHOIS_IANA_DATA_PATH)
    whois_client.set_domain_whois_from_file(domain, _REFER_URL, _MOCK_WHOIS_REFER_DATA_PATH)

    operation = RetrieveWhoisInfoOperation(whois_client=whois_client)

    context.location_data = operation.run(context.location_data)


@then("I should get a LocationData with Whois information about it's location")
def step_impl(context: Context):
    location_data = context.location_data

    for expected_key in _EXPECTED_KEYS:
        assert_that(location_data.data, has_key(expected_key))


@then("I should get a LocationData with Whois information about it's location with previous and new data")
def step_impl(context: Context):
    location_data = context.location_data

    assert_that(location_data.data, has_entries(_PREVIOUS_KEYS))
    for expected_key in _EXPECTED_KEYS:
        assert_that(location_data.data, has_key(expected_key))
