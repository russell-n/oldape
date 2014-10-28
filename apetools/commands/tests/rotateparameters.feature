Feature: Rotate Parameters
 Scenario: Rotate angles set
  Given Rotate Parameters built with only angles
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments are the angles

 Scenario: Rotate angles and configuration set
  Given Rotate Parameters built with a configuration
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments have angles and configuration

 Scenario: Rotate angles and section set
  Given Rotate Parameters built with a section
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments have angles and section

 Scenario: Rotate angles and velocity set
  Given Rotate Parameters built with a velocity
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments have angles and velocity

 Scenario: Rotate angles and acceleration set
  Given Rotate Parameters built with an acceleration
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments have angles and acceleration

 Scenario: Rotate angles and deceleration set
  Given Rotate Parameters built with an deceleration
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments have angles and deceleration
