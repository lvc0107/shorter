Feature: Test Shorter API

  Scenario: Healthcheck
    When I test healthcheck
    Then I get status code 200
    And the value of Service is OK

  Scenario: Get a short URL list
    Given the user is authenticated as consumer_token
    When I get a valid short URL with a valid code
    Then I get status code 200

  Scenario: Get a short URL list. Unauthorized
    Given the user is authenticated as invalid_token
    When I get a valid short URL with a valid code
    Then I get status code 401


  Scenario: Create a short URL
    Given the user is authenticated as admin_token
    When I post a valid short URL with a valid code
    Then I get status code 201
    And the code is correct


  Scenario: Create a short URL without code
    Given the user is authenticated as admin_token
    When I post a valid short URL without code
    Then I get status code 201
    And the code is correct


  Scenario: Invalid URL
    Given the user is authenticated as admin_token
    When I post an invalid URL
    Then I get status code 400
    And the value of Error is ERROR_INVALID_URL


  Scenario: Missing URL
    Given the user is authenticated as admin_token
    When I post a missing URL
    Then I get status code 400
    And the value of Error is ERROR_URL_IS_REQUIRED


  Scenario: Invalid code
    Given the user is authenticated as admin_token
    When I post an invalid code
    Then I get status code 400
    And the value of Error is ERROR_INVALID_CODE


  Scenario: Duplicated code
    Given the user is authenticated as admin_token
    When I post a valid short URL with a valid code
    Then I get status code 201
    And the code is correct
    When I post a valid short URL with the same valid code
    Then I get status code 409
    And the value of Error is ERROR_DUPLICATED_CODE


  Scenario: Get code
    Given the user is authenticated as admin_token
    When I post a valid short URL with a valid code and URL http://url.com
    Then I get status code 201
    And the code is correct
    Given the user is authenticated as consumer_token
    When I get the same valid code
    Then I get status code 302
    And the value for location header is http://url.com


  Scenario: Get invalid code
    Given the user is authenticated as consumer_token
    When I get an invalid code
    Then I get status code 404
    And the value of Error is ERROR_CODE_NOT_FOUND


  Scenario: Get code stats
    Given the user is authenticated as admin_token
    When I post a valid short URL with a valid code and URL http://url.com
    Then I get status code 201
    And the code is correct
    Given the user is authenticated as consumer_token
    When I get the same valid code
    Then I get status code 302
    And the value for location header is http://url.com

    When I get the same valid code
    Then I get status code 302
    And the value for location header is http://url.com

    When I get the same valid code
    Then I get status code 302
    And the value for location header is http://url.com

    When I get code stats
    Then the value of created_at is a_valid_date
    Then the value of last_usage is a_valid_date
    Then the value of usage_count is 3


  Scenario: Get an invalid code for stats
    Given the user is authenticated as consumer_token
    When I get invalid code stats
    Then I get status code 404
    And the value of Error is ERROR_CODE_NOT_FOUND
