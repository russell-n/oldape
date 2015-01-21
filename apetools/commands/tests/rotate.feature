Feature: Rotate Command
 Scenario: Rotate Command is called with one table
  Given the rotate command is built with one connection
  When the rotate command is called
  Then the connection is given the parameters for it
  And the call returns the expected string

 Scenario: Rotate command is called and gives output
  Given the rotate command is built without kill_process
  When the rotate command is called
  Then the output from the connection is logged
