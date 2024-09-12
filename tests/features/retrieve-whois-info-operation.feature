Feature: Querying Whois information for domains

  Scenario: Add info to empty location_data object
    Given I have an empty LocationData
    When I run the RetrieveWhoisInfoOperation for the location
    Then I should get a LocationData with Whois information about it's location

  Scenario: Add info to object without overwriting existing data
    Given I have a LocationData with existing data
    When I run the RetrieveWhoisInfoOperation for the location
    Then I should get a LocationData with Whois information about it's location with previous and new data
