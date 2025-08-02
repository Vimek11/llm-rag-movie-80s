Feature: Ask intelligent questions about 1980s movie descriptions

  Scenario: User asks about movies related to space
    Given the movie question-and-answer system is available
    When the user asks "What movies are about space?"
    Then the system should return a relevant answer
    And the system should include at least one matching movie
