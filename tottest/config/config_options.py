class ConfigOptions(object):
    """
    An enumeration of sorts to hold the section and option names for the config file.
    """
    test_section = 'TEST'
    dut_section = 'DUT'
    logwatcher_section = "LOGWATCHER"
    logcatwatcher_section = "LOGCATWATCHER"
    output_folder_option = 'output_folder'
    data_file_option = "data_file"
    repetitions_option = "repeat"
    recovery_time_option = "recovery_time"
    timeout_option = 'timeout'
    criteria_option = "criteria"
    target_option = 'target'
    wifi_interface_option = 'wifi_interface'
    threshold_option = "threshold"
    logs_option = "logs"
