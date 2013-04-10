Use Case 1 Static Model
=======================

.. uml::

   ArgumentParser: Namespace args

   ConfigurationMap o-- ArgumentParser 
   ConfigurationMap: ConfigParser parser
   ConfigurationMap: String get(section, option)
   ConfigurationMap: Integer get_int(section, option)
   ConfigurationMap: Float get_time(section, option)
   ConfigurationMap: String | None get_optional(section, option, default)

   Lexicographer o-- ConfigurationMap
   Lexicographer: Parameter parameters

   Builder: Generator parameters
   Builder: DeviceBuilder dut_device_builder
   Builder: ConnectionBuilder dut_connection_builder
   Builder: ConnectionBuilder tpc_connection_builder
   Builder: TearDownBuilder teardown_builder
   Builder: TestBuilder test_builder
   Builder: Hortator hortator
   Builder *-- DeviceBuilder
   Builder *-- ConnectionBuilder
   Builder *-- TestBuilder
   Builder *-- Lexicographer
   Builder *-- Hortator
   Builder *-- TearDownBuilder

   ParameterGenerator: Generator parameters

   abstract class DeviceBuilder
   DeviceBuilder: Device device
   DeviceBuilder: init(parameters)

   TearDownBuilder: init(StaticParameters parameters, StorageOutput storage)
   TearDownBuilder: TearDown teardown

   AdbDeviceBuilder: ADBDevice device
   AdbDeviceBuilder --|> DeviceBuilder

   abstract class ConnectionBuilder
   ConnectionBuilder: Connection connection
   ConnectionBuilder: init(parameters)

   AdbConnectionBuilder: ADBShellConnection connection
   AdbConnectionBuilder --|> ConnectionBuilder
   AdbConnectionBuilder o-- ADBShellConnection

   SshConnectionBuilder: SSHConnection connection
   SshConnectionBuilder --|> ConnectionBuilder
   SshConnectionBuilder o-- SSHConnection

   abstract class TestBuilder
   TestBuilder: init(parameters)
   TestBuilder: Test test

   IperfTestBuilder: IperfTest test
   IperfTestBuilder --|> TestBuilder   

   abstract class Test

   IperfTest: IperfCommand sender
   IperfTest: IperfCommand receiver
   IperfTest: KillAll List killers
   IperfTest --|> Test
   IperfTest *-- IperfCommand   
   IperfTest *-- KillAll

   SSHConnection: String address
   SSHConnection: String username
   SSHConnection: [String password]
   SSHConnection: OperatingSystem operating_system
   SSHConnection --|> Connection   

   TestOperator: ParameterGenerator parameters
   TestOperator: Device dut
   TestOperator: Test test
   TestOperator: TearDown cleanup
   TestOperator: run()
   TestOperator *-- TearDown
   TestOperator *-- Test
   TestOperator *-- Device
   TestOperator *-- ParameterGenerator

   TearDown: Iter tools
   TearDown: run()

   Hortator *-- TestOperator
   Hortator: Generator operators
   Hortator: run()

   abstract class Command

   IperfCommand: StorageOutput output
   IperfCommand: Connection connection
   IperfCommand: run(parameters)
   IperfCommand --|> Command
   IperfCommand o-- StorageOutput
   IperfCommand o-- Connection

   KillAll: String name
   KillAll: Connection connection
   KillAll: OperatingSystem operating_system
   KillAll o-- Connection

   StorageOutput: folder_name
   StorageOutput: StorageOutput open(name, extension)
   StorageOutput: write(line)
   StorageOutput: copy(source)

   abstract class Device

   ADBDevice --|> Device

   ADBConnection: OperatingSystem operating_system
   
   abstract class Connection

   ADBShellConnection --|> ADBConnection

   ADBConnection --|> Connection   
