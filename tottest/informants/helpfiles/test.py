from timetorecovertest.info.constants import TEMPLATE, BOLD, RESET, NAME_TEMPLATE, BLUE

name = NAME_TEMPLATE.format(name="ttr test",
                            description="(test the connections to the DUT)").center(80)

synopsis = """
The {bold}test{reset} ({blue}ttr test{reset}) tests whether the connections to the DUT needed for the test are set up.
""".format(bold=BOLD, reset=RESET, blue=BLUE)

description = """
The {bold}ttr test{reset} tests three(3) connections:

    1. ADB (via USB)
    2. SL4A (via ADB)
    3. network (via WiFi)

The {blue}ADB{reset} and {blue}SL4A{reset} connections are necessary for the testing - if they fail a crash will result. The network connection would be good to have but isn't necessary. If it you get a network_id of -1, it probably isn't connected, but the test will still work if the DUT has its radio off and will connect once it's turned on...
""".format(bold=BOLD, reset=RESET, blue=BLUE)

examples="""
A {blue}disabled{reset} but usable DUT will say:

****************************************
network_id:-1
supplicant_state:completed
link_speed:-1
mac_address:f0:a2:25:b2:5c:56
rssi:-200
ip_address:0
hidden_ssid:False
****************************************

While a fully functional one will say:

****************************************
ssid:wndr3700
bssid:a0:21:b7:b6:0e:f1
network_id:0
supplicant_state:completed
link_speed:-1
mac_address:e0:cb:1d:3d:84:71
rssi:-200
ip_address:1628743872
hidden_ssid:False
Real IP: 192.168.20.97
****************************************
""".format(blue=BLUE, reset=RESET, bold=BOLD)

see_also = """
    RFKill
"""

output = TEMPLATE.format(name=name, synopsis=synopsis, description=description,
                         examples=examples, see_also=see_also)
