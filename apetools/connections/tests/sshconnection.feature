Feature: SSH Connection
 Scenario: User sets the connection's identifier
  Given an ssh connection created with an identifier
  When the connection's identifier is checked
  Then the connection's identifier is the one the user set
