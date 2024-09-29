#!/usr/bin/env python
"""A simple CLI tool."""
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import argparse
import distutils.dir_util
import datetime
import os
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

try:
    from version import __version__
except ImportError:
    __version__ = "dev"

from pyfritzhome import Fritzhome

_LOGGER = logging.getLogger(__name__)

def write_temparature_longterm(fritz, args):
    """Command that write actual thermostat temperature to a file"""
    targetpath = "/mnt/4TBIronWolfPro01/fritzdata"
    devices = fritz.get_thermostat_devices()
    year = datetime.date.today().year
    month = datetime.date.today().month
    timestamp = datetime.datetime.utcnow()
    distutils.dir_util.mkpath('%s/%s/%s' % (targetpath, year, month))
    """Create csv file per device"""
    for device in devices:
        if os.path.isfile('%s/%s/%s/%s' % (targetpath, year, month, device.name)):
            f = open('%s/%s/%s/%s' % (targetpath, year, month, device.name), 'a')
            f.write('%s,%s,%s,%s\n' % (timestamp, device.name, device.actual_temperature, device.target_temperature))
            f.close()
        else:
            f = open('%s/%s/%s/%s' % (targetpath, year, month, device.name), 'w+')
            f.write('Time,SensorName,actualTemperature,targetTemperature\n')
            f.close()
            f = open('%s/%s/%s/%s' % (targetpath, year, month, device.name), 'a')
            f.write('%s,%s,%s,%s\n' % (timestamp, device.name, device.actual_temperature, device.target_temperature))
            f.close()


def write_temparature_longterm_influx(fritz, args):
    """Command that write actual thermostat temperature to a file"""
    token = args.token
    url = args.url
    org = args.org
    bucket = args.bucket
    devices = fritz.get_thermostat_devices()
    #timestamp = datetime.datetime.utcnow()
    if not token:
        #token = os.environ.get("INFLUXDB_TOKEN")
        token = "VrmRq6LReMXLUUASYblbNidcNyR-_pywXJAeYqO1FvzLsd17zYF4pBjSuMXVNqi_od89MMUgpe00_sA8h6xy4A=="
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    """ Create csv file per device """
    for device in devices:
        write_api = write_client.write_api(write_options=SYNCHRONOUS)

        point = (
                Point(device.name)
                .field("temp", device.actual_temperature)
            )
        write_api.write(bucket=bucket, org=org, record=point)

        #temperature_data = [timestamp, device.name, device.actual_temperature, device.target_temperature]


def write_powerconsumption_longterm_influx(fritz, args):
    """Command that write actual power consumption temperature to influx db"""
    token = args.token
    url = args.url
    org = args.org
    bucket = args.bucket
    devices = fritz.get_powermeter_devices()
    #timestamp = datetime.datetime.utcnow()
    if not token:
        #token = os.environ.get("INFLUXDB_TOKEN")
        token = "VrmRq6LReMXLUUASYblbNidcNyR-_pywXJAeYqO1FvzLsd17zYF4pBjSuMXVNqi_od89MMUgpe00_sA8h6xy4A=="
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    """ Create csv file per device """
    for device in devices:
        write_api = write_client.write_api(write_options=SYNCHRONOUS)

        point = (
                Point(device.name)
                .field("consumption", device.power/1000)
            )
        write_api.write(bucket=bucket, org=org, record=point)

        #temperature_data = [timestamp, device.name, device.actual_temperature, device.target_temperature]


def list_thermostats(fritz, args):
    """Command that prints all thermostat device information."""
    devices = fritz.get_thermostat_devices()

    for device in devices:

        print('#' * 30)
        print("Thermostat:")
        print('name=%s' % device.name)
        print('  ain=%s' % device.ain)
        print('  id=%s' % device.identifier)
        print('  productname=%s' % device.productname)
        print('  manufacturer=%s' % device.manufacturer)
        print("  present=%s" % device.present)
        print("  lock=%s" % device.lock)
        print("  devicelock=%s" % device.device_lock)
        print("  battery_low=%s" % device.battery_low)
        print("  battery_level=%s" % device.battery_level)
        print("  actual=%s" % device.actual_temperature)
        print("  target=%s" % device.target_temperature)
        print("  comfort=%s" % device.comfort_temperature)
        print("  eco=%s" % device.eco_temperature)
        print("  window=%s" % device.window_open)
        print("  summer=%s" % device.summer_active)
        print("  holiday=%s" % device.holiday_active)

        if device.present is False:
            continue
        if device.has_alarm:
            print(" Alert:")
            print("  alert=%s" % device.alert_state)


def list_all(fritz, args):
    """Command that prints all device information."""
    devices = fritz.get_devices()

    for device in devices:
        print("#" * 30)
        print("name=%s" % device.name)
        print("  ain=%s" % device.ain)
        print("  id=%s" % device.identifier)
        print("  productname=%s" % device.productname)
        print("  manufacturer=%s" % device.manufacturer)
        print("  present=%s" % device.present)
        print("  lock=%s" % device.lock)
        print("  devicelock=%s" % device.device_lock)
        print("  is_group=%s" % device.is_group)
        if device.is_group:
            print("  group_members=%s" % device.group_members)

        if device.present is False:
            continue

        if device.has_switch:
            print(" Switch:")
            print("  switch_state=%s" % device.switch_state)
        if device.has_powermeter:
            print(" Powermeter:")
            print("  power=%s" % device.power)
            print("  energy=%s" % device.energy)
            print("  voltage=%s" % device.voltage)
        if device.has_temperature_sensor:
            print(" Temperature:")
            print("  temperature=%s" % device.temperature)
            print("  offset=%s" % device.offset)
        if device.has_thermostat:
            print(" Thermostat:")
            print("  battery_low=%s" % device.battery_low)
            print("  battery_level=%s" % device.battery_level)
            print("  actual=%s" % device.actual_temperature)
            print("  target=%s" % device.target_temperature)
            print("  comfort=%s" % device.comfort_temperature)
            print("  eco=%s" % device.eco_temperature)
            print("  window=%s" % device.window_open)
            print("  window_until=%s" % device.window_open_endtime)
            print("  boost=%s" % device.boost_active)
            print("  boost_until=%s" % device.boost_active_endtime)
            print("  adaptive_heating_running=%s" % device.adaptive_heating_running)
            print("  summer=%s" % device.summer_active)
            print("  holiday=%s" % device.holiday_active)
        if device.has_alarm:
            print(" Alert:")
            print("  alert=%s" % device.alert_state)
        if device.has_lightbulb:
            print(" Light bulb:")
            print("  state=%s" % ("Off" if device.state == 0 else "On"))
            if device.has_level:
                print("  level=%s" % device.level)
            if device.has_color:
                print("  hue=%s" % device.hue)
                print("  saturation=%s" % device.saturation)
        if device.has_blind:
            print(" Blind:")
            print("  level=%s" % device.level)
            print("  levelpercentage=%s" % device.levelpercentage)
            print("  endpositionset=%s" % device.endpositionsset)


def device_name(fritz, args):
    """Command that prints the device name."""
    print(fritz.get_device_name(args.ain))


def device_presence(fritz, args):
    """Command that prints the device presence."""
    print(int(fritz.get_device_present(args.ain)))


def device_statistics(fritz, args):
    """Command that prints the device statistics."""
    stats = fritz.get_device_statistics(args.ain)
    print(stats)


def blind_set_open(fritz, args):
    """Command to open the blinds."""
    fritz.set_blind_open(args.ain)


def blind_set_close(fritz, args):
    """Command close the blinds."""
    fritz.set_blind_close(args.ain)


def blind_set_level_percentage(fritz, args):
    """Command that sets the blind level as percentage."""
    fritz.set_level_percentage(args.ain, args.level)


def thermostat_set_target_temperature(fritz, args):
    """Command that sets the thermostat temperature."""
    fritz.set_target_temperature(args.ain, args.temperature)


def thermostat_set_window_open(fritz, args):
    """Command that sets the thermostats window state."""
    fritz.set_window_open(args.ain, args.timespan)


def thermostat_set_boost_mode(fritz, args):
    """Command that sets the thermostats into boost mode."""
    fritz.set_boost_mode(args.ain, args.timespan)


def switch_get(fritz, args):
    """Command that get the device switch state."""
    print(fritz.get_switch_state(args.ain))


def switch_on(fritz, args):
    """Command that set the device switch state to on."""
    fritz.set_switch_state_on(args.ain)


def switch_off(fritz, args):
    """Command that set the device switch state to off."""
    fritz.set_switch_state_off(args.ain)


def switch_toggle(fritz, args):
    """Command that toggles the device switch state."""
    fritz.set_switch_state_toggle(args.ain)


def list_templates(fritz, args):
    """Command that prints all template information."""
    templates = fritz.get_templates()
    devices = fritz.get_devices_as_dict()

    for template in templates:
        print("#" * 30)
        print("name=%s" % template.name)
        print("  ain=%s" % template.ain)

        print(" Apply:")
        print("  hkr_summer=%s" % template.apply_hkr_summer)
        print("  hkr_temperature=%s" % template.apply_hkr_temperature)
        print("  hkr_holidays=%s" % template.apply_hkr_holidays)
        print("  hkr_time_table=%s" % template.apply_hkr_time_table)
        print("  relay_manual=%s" % template.apply_relay_manual)
        print("  relay_automatic=%s" % template.apply_relay_automatic)
        print("  level=%s" % template.apply_level)
        print("  color=%s" % template.apply_color)
        print("  dialhelper=%s" % template.apply_dialhelper)

        print(" Devices:")
        for device_id in template.devices:
            print("  %s=%s" % (device_id, devices[device_id].name))


def template_apply(fritz, args):
    """Command that applies a template."""
    fritz.apply_template(args.ain)


def main(args=None):
    """Enter the main function of the CLI tool."""
    parser = argparse.ArgumentParser(description="Fritz!Box Smarthome CLI tool.")
    parser.add_argument(
        "-v", action="store_true", dest="verbose", help="be more verbose"
    )
    parser.add_argument(
        "-f",
        "--fritzbox",
        type=str,
        dest="host",
        help="Fritz!Box IP address",
        default="fritz.box",
    )
    parser.add_argument("-u", "--user", type=str, dest="user", help="Username")
    parser.add_argument("-p", "--password", type=str, dest="password", help="Username")
    parser.add_argument(
        "-a",
        "--ain",
        type=str,
        dest="ain",
        help="Actor/Template Identification",
        default=None,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="{version}".format(version=__version__),
        help="Print version",
    )

    _sub = parser.add_subparsers(title="Commands")

    # list all devices
    subparser = _sub.add_parser("list", help="List all available devices")
    subparser.set_defaults(func=list_all)

    # write actual temperature into file for long term history
    subparser = _sub.add_parser('writelongterm', help='writes actual temperature of thermostat devices into a csv file')
    subparser.set_defaults(func=write_temparature_longterm)

    # write actual temperature into influxdb for long term history
    subparser = _sub.add_parser('writelongterminflux', help='writes actual temperature of thermostat devices into a influxdb')
    subparser.add_argument("-url", type=str, metavar="url", dest="url", help="InfluxDB URL")
    subparser.add_argument("-org", type=str, metavar="org", dest="org", help="InfluxDB org")
    subparser.add_argument("-token", type=str, metavar="token", dest="token", help="InfluxDB token")
    subparser.add_argument("-bucket", type=str, metavar="bucket", dest="bucket", help="InfluxDB bucket")
    subparser.set_defaults(func=write_temparature_longterm_influx)

    # write actual power consumption into influxdb for long term history
    subparser = _sub.add_parser('writelongterminfluxpc', help='writes actual temperature of thermostat devices into a influxdb')
    subparser.add_argument("-url", type=str, metavar="url", dest="url", help="InfluxDB URL")
    subparser.add_argument("-org", type=str, metavar="org", dest="org", help="InfluxDB org")
    subparser.add_argument("-token", type=str, metavar="token", dest="token", help="InfluxDB token")
    subparser.add_argument("-bucket", type=str, metavar="bucket", dest="bucket", help="InfluxDB bucket")
    subparser.set_defaults(func=write_powerconsumption_longterm_influx)


    # list all thermostat devices
    subparser = _sub.add_parser('thermostats', help='List all available thermostat devices')
    subparser.set_defaults(func=list_thermostats)

    # device
    subparser = _sub.add_parser("device", help="Device/Actor commands")
    _sub_switch = subparser.add_subparsers()

    # device name
    subparser = _sub_switch.add_parser("name", help="get the device name")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=device_name)

    # device presence
    subparser = _sub_switch.add_parser("present", help="get the device presence")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=device_presence)

    # device stats
    subparser = _sub_switch.add_parser("stats", help="get the device statistics")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=device_statistics)

    # blind
    subparser = _sub.add_parser("blind", help="Blind commands")
    _sub_switch = subparser.add_subparsers()

    # blind open
    subparser = _sub_switch.add_parser("open", help="open blinds")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=blind_set_open)

    # blind close
    subparser = _sub_switch.add_parser("close", help="close blinds")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=blind_set_close)

    # blind set level in percentage
    subparser = _sub_switch.add_parser(
        "set_level", help="set level of blinds in percentage (0=open)"
    )
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.add_argument(
        "level", type=float, metavar="LEVEL", help="blind level in percentage (0=open)"
    )
    subparser.set_defaults(func=blind_set_level_percentage)

    # thermostat
    subparser = _sub.add_parser("thermostat", help="Thermostat commands")
    _sub_switch = subparser.add_subparsers()

    # thermostat target temperature
    subparser = _sub_switch.add_parser(
        "set_target_temperature", help="set target temperature"
    )
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.add_argument(
        "temperature",
        type=float,
        metavar="TEMPERATURE",
        help="target temperature in (C)",
    )
    subparser.set_defaults(func=thermostat_set_target_temperature)

    # thermostat window_open
    subparser = _sub_switch.add_parser(
        "set_window_open", help="set window state to open"
    )
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.add_argument(
        "timespan",
        type=int,
        metavar="TIMESPAN",
        nargs="?",
        default=300,
        help="Open timespan in seconds (default=300s)",
    )
    subparser.set_defaults(func=thermostat_set_window_open)

    # thermostat boost_mpde
    subparser = _sub_switch.add_parser("set_boost_mode", help="activate the boost mode")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.add_argument(
        "timespan",
        type=int,
        choices=range(0, 86400),
        metavar="TIMESPAN",
        nargs="?",
        default=300,
        help="Boost timespan in seconds (default=300s)",
    )
    subparser.set_defaults(func=thermostat_set_boost_mode)

    # switch
    subparser = _sub.add_parser("switch", help="Switch commands")
    _sub_switch = subparser.add_subparsers()

    # switch get
    subparser = _sub_switch.add_parser("get", help="get state")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=switch_get)

    # switch on
    subparser = _sub_switch.add_parser("on", help="set on state")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=switch_on)

    # switch off
    subparser = _sub_switch.add_parser("off", help="set off state")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=switch_off)

    # switch toggle
    subparser = _sub_switch.add_parser("toggle", help="set off state")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=switch_toggle)

    # templates
    subparser = _sub.add_parser("template", help="Template commands")
    _sub_switch = subparser.add_subparsers()

    # list templates
    subparser = _sub_switch.add_parser("list", help="List all available templates")
    subparser.set_defaults(func=list_templates)

    # apply templates
    subparser = _sub_switch.add_parser("apply", help="Apply template")
    subparser.add_argument("ain", type=str, metavar="AIN", help="Actor Identification")
    subparser.set_defaults(func=template_apply)

    args = parser.parse_args(args)

    logging.basicConfig()
    if args.verbose:
        logging.getLogger("pyfritzhome").setLevel(logging.DEBUG)

    fritzbox = None
    try:
        fritzbox = Fritzhome(host=args.host, user=args.user, password=args.password)
        fritzbox.login()
        args.func(fritzbox, args)
    finally:
        if fritzbox is not None:
            fritzbox.logout()


if __name__ == "__main__":
    main()
