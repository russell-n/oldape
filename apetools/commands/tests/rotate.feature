Feature: Rotate Command
 Scenario: Rotate Command is called with one table
  Given the rotate command is built with one connection
  When the rotate command is called
  Then the connection is given the parameters for it
