Feature: Rotate Parameters
 Scenario: Rotate angles set
  Given Rotate Parameters built with only angles
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments are the angles

 Scenario: Rotate angles and test set
  Given Rotate Parameters built with test flag
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments have angles and test

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

 Scenario: Rotate angles and multiple booleans set
  Given Rotate Parameters built with boolean options
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments have angles and boolean options

 Scenario: Rotate angles and multiple values set
  Given Rotate Parameters built with value options
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments have angles and values options

 Scenario: Rotate angles and multiple values and booleans set
  Given Rotate Parameters built with value and boolean options
  When the Rotate Parameters arguments are checked
  Then the Rotate Parameters arguments have angles, boolean and value options
