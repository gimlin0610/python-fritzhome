##!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
import logging
import argparse
import distutils.dir_util
import os
import datetime as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as pyplot
import pandas as pandas
from settings import *


try:
    from version import __version__
except ImportError:
    __version__ = 'dev'

from pyfritzhome import Fritzhome

_LOGGER = logging.getLogger(__name__)

def generate_dataset(startdate, enddate, datafile):

    # Load DataSet
    dataset = pandas.read_csv(datafile, sep=",", header=0, usecols=['Time', 'actualTemperature', 'targetTemperature'],
                              parse_dates=['Time'])
    print('loading %s' % datafile)
    dataset.set_index('Time', inplace=True)
    dataset.index = pandas.to_datetime(dataset.index)
    dataset = dataset.loc[startdate:enddate]
    # clear dataframes from missing values
    dataset['actualTemperature'] = pandas.to_numeric(dataset['actualTemperature'], errors='coerce')
    dataset['targetTemperature'] = pandas.to_numeric(dataset['targetTemperature'], errors='coerce')
    var1 = dataset.groupby('Time').actualTemperature.sum()
    var2 = dataset.groupby('Time').targetTemperature.sum()
    return (var1, var2)


def save_graph(enddate, startdate, var1, var2, filename):
    # Build the graph
    now = datetime.now()
    starttimestamp = startdate.strftime("%d-%m-%Y")
    endtimestamp = enddate.strftime("%d-%m-%Y")
    report_file = output_dir_name + filename + "_" + starttimestamp + "_" + endtimestamp + ".svg"
    fig = pyplot.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = ax1.twinx()
    ax1.set_xlabel('Zeit')
    ax1.set_ylabel('actualTemperature')
    ax2.set_ylabel('targetTemperature')
    ax1.axes.yaxis.set_ticklabels([])
    var1.plot(kind='line')
    var2.plot(kind='line')
    pyplot.title(filename)
    pyplot.setp(ax1.get_xticklabels(), rotation=30)
    pyplot.savefig(report_file)


def show_graph(var1, var2, filename):
    # Build the graph
    fig = pyplot.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = ax1.twinx()
    ax1.set_xlabel('Zeit')
    ax1.set_ylabel('actualTemperature')
    ax2.set_ylabel('targetTemperature')
    ax1.axes.yaxis.set_ticklabels([])
    var1.plot(kind='line')
    var2.plot(kind='line')
    pyplot.title(filename)
    pyplot.setp(ax1.get_xticklabels(), rotation=30)
    pyplot.show()


def get_list_of_files(datasource_dir_name):
    # create a list of file and sub directories
    # names in the given directory
    all_data_files = os.listdir(datasource_dir_name)
    return all_data_files

def write_temparature_longterm(fritz, args):
    """Command that write actual thermostat temperature to a file"""
    targetpath = "/var/fritzhome"
    devices = fritz.get_thermostat_devices()
    year = dt.date.today().year
    month = dt.date.today().month
    timestamp = dt.datetime.utcnow()
    distutils.dir_util.mkpath('%s/%s/%s' % (targetpath,year,month))
    """Create csv file per device if not present"""
    for device in devices:
        if os.path.isfile('%s/%s/%s/%s' % (targetpath,year,month,device.name)):
            f = open('%s/%s/%s/%s' % (targetpath,year,month,device.name), 'a')
            f.write('%s,%s,%s,%s\n' % (timestamp,device.name,device.actual_temperature,device.target_temperature))
            f.close()
        else:
            f = open('%s/%s/%s/%s' % (targetpath,year,month,device.name), 'w+')
            f.write('Time,SensorName,actualTemperature,targetTemperature\n')
            f.close()
            f = open('%s/%s/%s/%s' % (targetpath,year,month,device.name), 'a')
            f.write('%s,%s,%s,%s\n' % (timestamp,device.name,device.actual_temperature,device.target_temperature))
            f.close()


def list_alert_sensors(fritz, args):
    """Command that prints all alert sensor device information."""
    devices = fritz.get_alert_sensors()
    for device in devices:
        print('#' * 30)
        print("Alert Sensor:")
        print('name=%s' % device.name)
        print('  ain=%s' % device.ain)
        print('  id=%s' % device.identifier)
        print('  productname=%s' % device.productname)
        print('  manufacturer=%s' % device.manufacturer)
        print("  present=%s" % device.present)
        print("  lock=%s" % device.lock)
        print("  devicelock=%s" % device.device_lock)
        if device.present is False:
            continue
        if device.has_alarm:
            print(" Alert:")
            print("  alert=%s" % device.alert_state)


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
        print('#' * 30)
        print('name=%s' % device.name)
        print('  ain=%s' % device.ain)
        print('  id=%s' % device.identifier)
        print('  productname=%s' % device.productname)
        print('  manufacturer=%s' % device.manufacturer)
        print("  present=%s" % device.present)
        print("  lock=%s" % device.lock)
        print("  devicelock=%s" % device.device_lock)

        if device.present is False:
            continue

        if device.has_switch:
            print(" Switch:")
            print("  switch_state=%s" % device.switch_state)
        if device.has_switch:
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
            print("  summer=%s" % device.summer_active)
            print("  holiday=%s" % device.holiday_active)
        if device.has_alarm:
            print(" Alert:")
            print("  alert=%s" % device.alert_state)


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


def switch_get(fritz, args):
    """Command that get the device switch state."""
    print(fritz.get_switch_state(args.ain))


def alert_get(fritz, args):
    """Command that get the device switch state."""
    print(fritz.get_alert_state(args.ain))


def switch_on(fritz, args):
    """Command that set the device switch state to on."""
    fritz.set_switch_state_on(args.ain)


def switch_off(fritz, args):
    """Command that set the device switch state to off."""
    fritz.set_switch_state_off(args.ain)


def switch_toggle(fritz, args):
    """Command that toggles the device switch state."""
    fritz.set_switch_state_toggle(args.ain)


def main(args=None):
    """The main function."""
    year = dt.date.today().year
    month = dt.date.today().month
    dayofmonth = dt.date.today().day
    distutils.dir_util.mkpath('%s/' % (output_dir_name))

    parser = argparse.ArgumentParser(
        description='Fritz!Box Smarthome CLI tool.')

    parser.add_argument('-d','--day', action='store_true', dest='day',
                        help='create temerature report for last 24h')

    parser.add_argument('-w','--week', action='store_true', dest='week',
                        help='create temerature report for last 7 days')

    parser.add_argument('-m','--month',
                        type=int,
                        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        action='store',
                        nargs='?',
                        dest='month',
                        help='create temerature report for given month 1-12')

    parser.add_argument('-s', action='store_true', dest='show',
                        help='show graph')


    #parser = argparse.ArgumentParser(
    #   description='Fritz!Box Smarthome CLI tool.')
    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='be more verbose')
    parser.add_argument('-f', '--fritzbox', type=str, dest='host',
                        help='Fritz!Box IP address', default='fritz.box')
    parser.add_argument('-u', '--user', type=str, dest='user',
                        help='Username')
    parser.add_argument('-p', '--password', type=str, dest='password',
                        help='Username')
    parser.add_argument('-a', '--ain', type=str, dest='ain',
                        help='Actor Identification', default=None)
    parser.add_argument('-V', '--version', action='version',
                        version='{version}'.format(version=__version__),
                        help='Print version')

    _sub = parser.add_subparsers(title='Commands')

    # list all devices
    subparser = _sub.add_parser('list', help='List all available devices')
    subparser.set_defaults(func=list_all)

    # write actual temperature into file for long term history
    subparser = _sub.add_parser('writelongterm', help='writes actual temperature of thermostat devices into a csv file')
    subparser.set_defaults(func=write_temparature_longterm)

    # show optical sensor state
    subparser = _sub.add_parser('alertsensors', help='return state of alert sensor')
    subparser.set_defaults(func=list_alert_sensors)

    # list all thermostat devices
    subparser = _sub.add_parser('thermostats', help='List all available thermostat devices')
    subparser.set_defaults(func=list_thermostats)

    # device
    subparser = _sub.add_parser('device', help='Device/Actor commands')
    _sub_switch = subparser.add_subparsers()

    # device name
    subparser = _sub_switch.add_parser('name', help='get the device name')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=device_name)

    # device presence
    subparser = _sub_switch.add_parser('present',
                                       help='get the device presence')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=device_presence)

    # device stats
    subparser = _sub_switch.add_parser('stats',
                                       help='get the device statistics')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=device_statistics)

    # switch
    subparser = _sub.add_parser('switch', help='Switch commands')
    _sub_switch = subparser.add_subparsers()

    # switch get
    subparser = _sub_switch.add_parser('get', help='get state')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=switch_get)

    # switch on
    subparser = _sub_switch.add_parser('on', help='set on state')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=switch_on)

    # switch off
    subparser = _sub_switch.add_parser('off', help='set off state')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=switch_off)

    # switch toggle
    subparser = _sub_switch.add_parser('toggle', help='set off state')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=switch_toggle)

    # alert
    subparser = _sub.add_parser('alert', help='alert commands')
    _sub_alert = subparser.add_subparsers()

    # alert get
    subparser = _sub_alert.add_parser('get', help='alert get returns state')
    subparser.add_argument('ain', type=str, metavar="AIN",
                           help='Actor Identification')
    subparser.set_defaults(func=alert_get)


    args = parser.parse_args(args)

    logging.basicConfig()
    if args.verbose:
        logging.getLogger('pyfritzhome').setLevel(logging.DEBUG)

    fritzbox = None
    try:
        fritzbox = Fritzhome(host=args.host, user=args.user,
                             password=args.password)
        fritzbox.login()
        args.func(fritzbox, args)
    finally:
        if fritzbox is not None:
            fritzbox.logout()

    elif args.day:
        N = 1
        startdate = datetime.now() - timedelta(days=N)
        enddate = datetime.now()
        datasource_dir_name = datasource_datebased_dir_name + str(year) + "/" + str(month) + "/"

    elif args.week:
        N = 7
        startdate = datetime.now() - timedelta(days=N)
        enddate = datetime.now()
        datasource_dir_name = datasource_datebased_dir_name + str(year) + "/" + str(month) + "/"

    elif args.month:
        month=args.month
        datasource_dir_name = datasource_datebased_dir_name + str(year) + "/" + str(month) + "/"
        startdate = datetime(year,month,1)
        enddate = datetime(year,month+1,1)
        print startdate
        print enddate

    else:
        startdate = "2019-01-01 00:00:00.000000"
        enddate = "2019-12-31 23:59:59.999999"

    all_data_files = get_list_of_files(datasource_dir_name)


if __name__ == '__main__':
    main()
