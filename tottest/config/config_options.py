class ConfigOptions(object):
    """
    An enumeration of sorts to hold the section and option names for the config file.
    """
    test_section = 'TEST'
    output_folder_option = 'output_folder'
    data_file_option = "data_file"
    repetitions_option = "repetitions"
    
    dut_section = 'DUT'
    traffic_pc_section = "TRAFFIC_PC"
    login_option = "login"
    password_option = "password"
    control_ip_option = "control_ip_address"
    test_ip_option = "test_ip_address"
    
    iperf_section = "IPERF"
    window_option = "window"
    length_option = "length"
    parallel_option = "parallel"
    interval_option = "interval"
    format_option = "format"
    time_option = "time"
