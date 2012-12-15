class ConfigOptions(object):
    """
    An enumeration of sorts to hold the section and option names for the config file.
    """
    # sections
    test_section = 'TEST'
    poweron_section = "POWERON"
    oscillate_section = 'OSCILLATE'
    watchlogs_section = "WATCHLOGS"

    #options
    operation_setup_option = "operation_setup"
    operation_teardown_option = "operation_teardown"
    test_setup_option = "setup_test"
    execute_test_option = "execute_test"
    teardown_test_option="teardown_test"
    
    output_folder_option = 'output_folder'
    data_file_option = "data_file"
    repeat_option = "repeat"
    recovery_time_option = "recovery_time"
    
    test_interface_option = "test_interface"
    operating_system_option = "operating_system"
    control_ip_option = "hostname"
    test_ip_option = "test_ip"
    connection_option = 'connection'
    traffic_pc_section = "TRAFFIC_PC"
    login_option = "login"
    password_option = "password"
    
    apconnect_section = "APCONNECT"
    ssids_option = "ssids"
    paths_option = "paths"
    port_option = 'port'

    nodes_section = "NODES"
    
    iperf_section = "IPERF"
    directions_option = "directions"
    window_option = "window"
    length_option = "length"
    parallel_option = "parallel"
    interval_option = "interval"
    format_option = "format"
    time_option = "time"
    protocol_option = "protocol"

    time_to_recovery_section="TIMETORECOVERY"
    threshold_option = "threshold"
    timeout_option = "timeout"
    affector_section = "AFFECTOR"
    affector_type_option = "type"
    switches_option = "switches"
    hostname_option = "hostname"
    username_option = 'username'
    rotate_section = "ROTATE"
    angles_option = "angles"

    start_option = "start"
    arc_option = "arc"
    noise_start_option = "noise_start"
    noise_end_option = "noise_end"

    block_option = "block"
    no_cleanup_option = "no_cleanup"

    anti_adjustment_option = 'anti_adjustment'
    clockwise_adjustment_option = 'clockwise_adjustment'
