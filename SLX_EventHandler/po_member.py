#!/usr/bin/env python
"""Registers this script as an event handler for specific log messages
and patterns.
The maximum number of triggers for an event is 100, and patterns can
defined as well.
"""
import argparse
import re
import json
import logging
import sys
from CLI import CLI

# Declaring the dictionary that holds the event information.
# Required keys are EVENT_NAME, LOG_MSGID_LIST, PATTERN_LIST, ACTION
# Optional keys can be removed, as the class will set them to the defaults.
# All keys are shown here for documentation purposes.
EVENT = {}
# This is the name of the event-handler instance.
# The script uses its filename without the .py for this.
# This value can be changed to a static string.
# The script/EVENT_NAME should NOT be named 'activate.py' or 'activate'
# as 'activate is a reserved keyword.
EVENT['EVENT_NAME'] = sys.argv[0].split('/')[-1].split('.')[0]
# This is the list syslog message the script will register for.
EVENT['LOG_MSGID_LIST'] = ['NSM-1019', 'NSM-1020']
# This is the patterns applied to the syslog message the script will
# register for. This list should be either empty/null, or contain the
# same number of entries as LOG_MSGID_LIST.
EVENT['PATTERN_LIST'] = ['Port-channel', 'Port-channel']
# Storing the script name for use in registering as the action.
EVENT['ACTION'] = sys.argv[0].split('/')[-1]
# DESCRIPTION is an optional string that describes the event-handler.
# It can be 0 to 128 characters long
EVENT['DESCRIPTION'] = 'Set port-channel member ports to port-channel state.'
# These are the policy options for the event:
# Check the SLX command reference and mgmt guide for more information
#  Number of minutes till the action is aborted, 0 for none
EVENT['ACTION_TIMEOUT'] = 0
#  Delay in seconds for the initial launch of the action
EVENT['DELAY'] = 0
#  Time in seconds between iterations of the action
EVENT['INTERVAL'] = 0
#  Number of times the action will be run on trigger.
EVENT['ITERATIONS'] = 1
#  TRIGGER_FUNCTION determines if any trigger ('OR'), or all
#  triggers ('AND') must be met. TRIGGER_FUNCTION_TIME applies to 'AND' only,
#  and specifies the time in seconds for all triggers to be met.
EVENT['TRIGGER_FUNCTION'] = 'OR'
EVENT['TRIGGER_FUNCTION_TIME'] = 0
#  TRIGGER_MODE determines if the action is run on 'each-instance',
#  'on-first-instance', or 'only-once'.
EVENT['TRIGGER_MODE'] = 'each-instance'


class EventHandler():
    """Event handler class.
    Handles the registration of the events, as well as the actions.
    """

    def __init__(self, event, raslog_triggers, force_overwrite=False):
        """Initializes the event handler class.
        contians the functions for the actions when triggered,
        as well as configuring the event-handler CLI.
        """
        self.logger = logging.getLogger(__name__)
        self.data = {}
        self.data['triggers_raw'] = raslog_triggers
        self.data['force'] = force_overwrite
        self.data['log_message'] = {}
        self.data['actions'] = ['action_one', 'action_two']
        self.config = {}
        self.patterns = {}
        self.__patterns_init()
        self.dflt_cnfg = {}
        self.__dflt_cnfg_init()
        self.__validate_event(event)
        for key in self.dflt_cnfg:
            if key not in event.keys():
                event[key] = self.dflt_cnfg[key]
        for key in event:
            if not key == 'LOG_MSGID_LIST' or key == 'PATTERN_LIST':
                self.data[key.lower()] = event[key]
        self.__munge_log_msgid_and_pattern(event)
        self.logger.info('Initialized %s', __name__)
        return

    def action(self, state):
        """Action for when the Port-channel changes admin state."""
        sub_key = self.data['log_message'].keys()[0]
        log_match = self.patterns['log_message'].search(
            self.data['log_message'][sub_key])
        if log_match:
            self.logger.info('admin %s for the po members of po: %s',
                             state, str(log_match.group['po_num']))
            output = CLI("show port-ch " + str(log_match.group['po_num'])
                         + ' | include Eth', False).get_output()
            config = ['configure terminal']
            line_pattern = re.compile(r'[ethE]+\s+(?P=<interface>[\d/]+)\s+')
            action = 'shutdown'
            if 'up' in state:
                action = 'no' + action
            for line in output:
                line_match = line_pattern.search(line)
                if line_match:
                    config.append('interface ethernet '
                                  + line_match.group['interface'], action)
            CLI('\n'.join(config), False)
        return

    def do_actions(self):
        """Sets the port-channel member status to match the port-channel's"""
        self.__get_logs()
        self.patterns['log_message'] = re.compile(r'Interface Port-channel '
                                                  + r'(?P=<po_num>[\d]+)')
        if 'NSM-1020' in self.data['log_message']:
            self.action('down')
        if 'NSM-1019' in self.data['log_message']:
            self.action('up')
        return

    # Past this is the initialization and registration code.
    def __patterns_init(self):
        """sets up the regex patterns for digging through the config."""
        self.patterns['event_handler_name'] = re.compile(
            r'event-handler\s+(\S+)')
        self.patterns['event_handler_activate'] = re.compile(
            r'event-handler\s+activate\s+(\S+)')
        self.patterns['trigger_wo'] = re.compile(
            r'trigger\s+(?P<ordinal>\d+)\s+raslog\s+(?P<msgid>[\w\d-]+)')
        self.patterns['trigger_w'] = re.compile(
            r'trigger\s+(?P<ordinal>\d+)\s+raslog\s+'
            + r'(?P<msgid>[\w\d-]+)[pattern\s]+?(?P<pattern>\S+?)$')
        self.patterns['action'] = re.compile(
            r'action\s+[\w-]+\s+(\S+)')
        self.patterns['description'] = re.compile(
            r'description\s+([\s\d\w-]+)')
        self.patterns['action_timeout'] = re.compile(
            r'action-timeout\s+(\S+)')
        self.patterns['delay'] = re.compile(
            r'delay\s+(\S+)')
        self.patterns['interval'] = re.compile(
            r'interval\s+(\S+)')
        self.patterns['iterations'] = re.compile(
            r'iterations\s+(\S+)')
        self.patterns['trigger_mode'] = re.compile(
            r'trigger-mode\s+(\S+)')
        self.patterns['trigger_function'] = re.compile(
            r'trigger-function\s+([ORAND]+)([\s\w\-]+([\d]+))?')
        return

    def __dflt_cnfg_init(self):
        """sets up the defaults for optional items, and validation."""
        self.dflt_cnfg['ACTION_TIMEOUT'] = {}
        self.dflt_cnfg['ACTION_TIMEOUT'] = {'default': 0, 'type': 'int',
                                            'min': 0, 'max': 4294967295}
        self.dflt_cnfg['DELAY'] = {}
        self.dflt_cnfg['DELAY'] = {'default': 0, 'type': 'int', 'min': 0,
                                   'max': 4294967295}
        self.dflt_cnfg['INTERVAL'] = {}
        self.dflt_cnfg['INTERVAL'] = {'default': 0, 'type': 'int', 'min': 0,
                                      'max': 4294967295}
        self.dflt_cnfg['ITERATIONS'] = {}
        self.dflt_cnfg['ITERATIONS'] = {'default': 1, 'type': 'int', 'min': 0,
                                        'max': 4294967295}
        self.dflt_cnfg['DESCRIPTION'] = {}
        self.dflt_cnfg['DESCRIPTION'] = {'default': '', 'type': 'str',
                                         'length': [0, 128]}
        self.dflt_cnfg['TRIGGER_FUNCTION'] = {}
        self.dflt_cnfg['TRIGGER_FUNCTION'] = {'default': 'OR', 'type': 'str',
                                              'choices': ['OR', 'AND']}
        self.dflt_cnfg['TRIGGER_FUNCTION_TIME'] = {}
        self.dflt_cnfg['TRIGGER_FUNCTION_TIME'] = {'default': 0,
                                                   'type': 'int',
                                                   'min': 0, 'max': 4294967295}
        self.dflt_cnfg['TRIGGER_MODE'] = {}
        self.dflt_cnfg['TRIGGER_MODE'] = {'default': 'each-instance',
                                          'type': 'str',
                                          'choices': ['each-instance',
                                                      'on-first-instance',
                                                      'only-once']}
        return

    def __validate_event(self, event):
        """validates that the event dictionary has correct information."""
        self.logger.info('Checking that the contents of EVENT are usable.')
        required_keys = ['EVENT_NAME', 'LOG_MSGID_LIST', 'PATTERN_LIST',
                         'ACTION']
        if not all(elem in event.keys() for elem in required_keys):
            raise ValueError('EVENT is missing a required key. Please '
                             + 'check that the required keys EVENT_NAME, '
                             + 'LOG_MSGID_LIST, PATTERN_LIST, and ACTION '
                             + 'are present.')
        self.__validate_event_name(event)
        self.__validate_pattern_list(event)
        self.__validate_action(event)
        for key in self.dflt_cnfg:
            if key in event.keys():
                self.__validate_type(event, key)
                self.__validate_int_type(event, key)
                self.__validate_str_type(event, key)
        self.logger.info('Contents of EVENT are usable.')
        return

    @staticmethod
    def __validate_event_name(event):
        if not 1 <= len(event['EVENT_NAME']) <= 32:
            raise ValueError('EVENT_NAME is to long, or too short. It must '
                             + 'string with a length between 1 and 32 '
                             + 'characters. Current value is: '
                             + event['EVENT_NAME'])
        if event['EVENT_NAME'] == 'activate':
            raise ValueError('EVENT["EVENT_NAME"] must not be "activate". '
                             + 'Please rename the script to something other '
                             + 'than "activate.py"')
        return

    @staticmethod
    def __validate_pattern_list(event):
        if event['PATTERN_LIST']:
            if len(event['PATTERN_LIST']) != len(event['LOG_MSGID_LIST']):
                raise ValueError('EVENT["LOG_MSGID_LIST"], and '
                                 + 'EVENT["PATTERN_LIST"] must contain the '
                                 + 'same number of entries.')
        return

    @staticmethod
    def __validate_action(event):
        """."""
        if not 1 <= len(event['ACTION']) <= 32:
            raise ValueError('ACTION is to long, or too short. It must '
                             + 'string with a length between 1 and 32 '
                             + 'characters. Current value is: '
                             + event['ACTION'])
        return

    def __validate_type(self, event, key):
        """."""
        if not self.__chk_dt_tp(event[key], self.dflt_cnfg[key]['type']):
            raise TypeError('EVENT[%s] does not have the correct '
                            + 'data type. Please check the value '
                            + 'entered.', key)
        return

    def __validate_int_type(self, event, key):
        """."""
        if self.dflt_cnfg[key]['type'] == 'int':
            if (not self.dflt_cnfg[key]['min'] <= event[key]
                    <= self.dflt_cnfg[key]['max']):
                raise ValueError('EVENT[%s] is outside the allowed '
                                 + 'range of %s - %s.', key,
                                 self.dflt_cnfg[key]['min'],
                                 self.dflt_cnfg[key]['max'])
        return

    def __validate_str_type(self, event, key):
        """."""
        if self.dflt_cnfg[key]['type'] == 'str':
            if 'choices' in self.dflt_cnfg[key]:
                if not event[key] in self.dflt_cnfg[key]['choices']:
                    raise ValueError('EVENT[%s] is not an allowed '
                                     + 'choice of: %s', key,
                                     ', '.join(
                                         self.dflt_cnfg[key]['choices']
                                     ))
            if 'length' in self.dflt_cnfg[key]:
                if (not self.dflt_cnfg[key]['length'][0]
                        <= len(event[key])
                        <= self.dflt_cnfg[key]['length'][1]):
                    raise ValueError('%s is to long, or too short. '
                                     + 'It must string with a length '
                                     + 'between %s and %s characters.'
                                     + ' Current value is: %s',
                                     key,
                                     self.dflt_cnfg[key]['length'][0],
                                     self.dflt_cnfg[key]['length'][1],
                                     event[key])
        return

    @staticmethod
    def __chk_dt_tp(value, expected_type):
        """returns a boolean if the value is of the expected type."""
        return str(type(value)) is not expected_type

    def __munge_log_msgid_and_pattern(self, event):
        """combines the two lists into a dictionary stored in
        self.data['trigger']."""
        self.data['trigger'] = {}
        if event['PATTERN_LIST']:
            for index, value in enumerate(event['LOG_MSGID_LIST']):
                self.data['trigger'][str(index + 1)] = {}
                self.data['trigger'][str(index + 1)] = {
                                                    'ordinal': str(index + 1),
                                                    'msgid': value,
                                                    'pattern': event[
                                                        'PATTERN_LIST'][index]}
        else:
            for index, value in enumerate(event['LOG_MSGID_LIST']):
                self.data['trigger'][str(index + 1)] = {}
                self.data['trigger'][str(index + 1)] = {
                                                    'ordinal': str(index + 1),
                                                    'msgid': value,
                                                    'pattern': ''}
        return

    def do_registration(self):
        """configures the event handlers for the msgid's in
        LOG_MSGID_LIST with the patterns in PATTERN_LIST.
        """
        self.__check_for_event_handler()
        self.__register_event_handler()
        self.__activate_event_handler()

    def __check_for_event_handler(self):
        """checks for the event handlers for the msgid's in LOG_MSGID_LIST.
        Returns either a list of the event handler names, or """
        self.__get_config()
        self.data['new_config'] = False
        self.data['fix_triggers'] = False
        self.data['fix_action'] = {'status': False, 'same_script': False}
        self.data['fix_description'] = False
        if self.config['event_handler_name']:
            self.logger.info('Checking existing config versus desired.')
            self.__check_trigger()
            self.__check_action()
            self.__check_description()
            self.__check_action_timeout()
            self.__check_delay()
            self.__check_interval()
            self.__check_iterations()
            self.__check_trigger_mode()
            self.__check_trigger_function()
        else:
            self.data['new_config'] = True
        return

    def __get_config(self):
        """gets the running configuration for the event."""
        self.__get_event_handler_config()
        self.__get_event_handler_policy()
        return

    def __get_event_handler_config(self):
        """Gets the event-handler config. Stores the parsed config in
        self.config"""
        self.logger.info('Getting the running config for the event %s: ',
                         self.data['event_name'])
        event_handler_config = CLI('show running-config event-handler %s'
                                   % self.data['event_name'],
                                   False).get_output()
        self.config['trigger'] = None
        self.config['event_handler_name'] = None
        self.config['action'] = None
        self.config['description'] = None
        if ('syntax error: element does not exist' not in
                event_handler_config and '% No entries found.' not
                in event_handler_config):
            for line in event_handler_config:
                self.__find_event_handler_name(line)
                self.__find_trigger(line)
                self.__find_action(line)
                self.__find_description(line)
            return

    def __find_event_handler_name(self, line):
        """."""
        event_handler_name = self.patterns[
            'event_handler_name'].search(line)
        if event_handler_name:
            self.config['event_handler_name'] = {
                'name': event_handler_name.group(1), 'line': str(line)}
            self.logger.info('Event handler %s has been configured.',
                             self.data['event_name'])
        return

    def __find_trigger(self, line):
        """."""
        trigger = self.patterns['trigger_w'].search(line)
        if trigger:
            if not self.config['trigger']:
                self.config['trigger'] = {}
            self.config['trigger'][str(trigger.group('ordinal'))] = {}
            self.config['trigger'][str(trigger.group('ordinal'))] = {
                'ordinal': trigger.group('ordinal'),
                'msgid': trigger.group('msgid'),
                'pattern': trigger.group('pattern'),
                'line': line}
        else:
            trigger = self.patterns['trigger_wo'].search(line)
            if trigger:
                if not self.config['trigger']:
                    self.config['trigger'] = {}
                self.config['trigger'][str(trigger.group('ordinal'))] = {}
                self.config['trigger'][str(trigger.group('ordinal'))] = {
                    'ordinal': trigger.group('ordinal'),
                    'msgid': trigger.group('msgid'),
                    'pattern': '',
                    'line': line}
        return

    def __find_action(self, line):
        """."""
        action = self.patterns['action'].search(line)
        if action:
            self.config['action'] = {
                'script': action.group(1), 'line': line}
        return

    def __find_description(self, line):
        """."""
        description = self.patterns['description'].search(line)
        if description:
            self.config['description'] = {
                'description': description.group(1), 'line': line}
        return

    def __get_event_handler_policy(self):
        """Gets the event-handler activation config. Stores the parsed config
        in self.config"""
        event_activate_config = CLI('show running-config event-handler '
                                    + 'activate ' + self.data['event_name'],
                                    False).get_output()
        self.config['event_handler_activate'] = {'status': False}
        self.config['action_timeout'] = {}
        self.config['delay'] = {}
        self.config['interval'] = {}
        self.config['iterations'] = {}
        self.config['trigger_mode'] = {}
        self.config['trigger_function'] = {}
        for line in event_activate_config:
            if line == '% No entries found.':
                return
            self.config['event_handler_activate']['status'] = True
            self.__find_event_handler_activate(line)
            self.__find_action_timeout(line)
            self.__find_delay(line)
            self.__find_interval(line)
            self.__find_iterations(line)
            self.__find_trigger_mode(line)
            self.__find_trigger_function(line)
        return

    def __find_event_handler_activate(self, line):
        """."""
        event_handler_activate = self.patterns[
            'event_handler_activate'].search(line)
        if event_handler_activate:
            self.logger.info('Event handler %s has been activated.',
                             self.data['event_name'])
            if not self.config['event_handler_activate']:
                self.config['event_handler_activate']['status'] = True
        return

    def __find_action_timeout(self, line):
        """."""
        action_timeout = self.patterns['action_timeout'].search(line)
        if action_timeout:
            self.config['action_timeout'] = {
                'value': action_timeout.group(1), 'update': False,
                'line': line}
            if (self.config['action_timeout']['value']
                    != self.data['action_timeout']):
                self.config['action_timeout']['update'] = True
        return

    def __find_delay(self, line):
        """."""
        delay = self.patterns['delay'].search(line)
        if delay:
            self.config['delay'] = {'value': delay.group(1),
                                    'update': False, 'line': line}
            if self.config['delay']['value'] != self.data['delay']:
                self.config['delay']['update'] = True
        return

    def __find_interval(self, line):
        """."""
        interval = self.patterns['interval'].search(line)
        if interval:
            self.config['interval'] = {
                'value': interval.group(1), 'update': False, 'line': line}
            if self.config['interval']['value'] != self.data['interval']:
                self.config['interval']['update'] = True
        return

    def __find_iterations(self, line):
        """."""
        iterations = self.patterns['iterations'].search(line)
        if iterations:
            self.config['iterations'] = {
                'value': iterations.group(1), 'line': line}
            if (self.config['iterations']['value']
                    != self.data['iterations']):
                self.config['iterations']['update'] = True
        return

    def __find_trigger_mode(self, line):
        """."""
        trigger_mode = self.patterns['trigger_mode'].search(line)
        if trigger_mode:
            self.config['trigger_mode'] = {
                'value': trigger_mode.group(1), 'line': line,
                'update': False}
            if (self.config['trigger_mode']['value']
                    != self.data['trigger_mode']):
                self.config['trigger_mode']['update'] = True
        return

    def __find_trigger_function(self, line):
        """."""
        trigger_function = self.patterns['trigger_function'].search(line)
        if trigger_function:
            self.config['trigger_function'] = {
                'function': trigger_function.group(1),
                'time_window': trigger_function.group(2),
                'line': line, 'update': False}
            if (self.config['trigger_function']['function']
                    != self.data['trigger_function']
                    or self.config['trigger_function']['time_window']
                    != self.data['trigger_function_time']):
                self.config['trigger_function']['update'] = True
        return

    def __check_trigger(self):
        """."""
        if not self.__check_trigger_values():
            self.logger.warning('Configured triggers are different from '
                                + 'requested')
            if not self.data['force']:
                print('Configured triggers are different from requested.')
                user_override = ''
                while 'y'not in user_override and 'n' not in user_override:
                    user_override = input('Do you want to over write '
                                          + 'them? (y)es or (n)o: ').lower()
                    if 'y' in user_override:
                        self.data['fix_triggers'] = True
                    elif 'n' in user_override:
                        self.data['fix_triggers'] = False
                    else:
                        print('ERROR: Please use a (y)es or (n)o.')
            else:
                print('Configured triggers are different from '
                      + 'requested, and force-overwrite is enabled')
                self.logger.warning('Configured triggers are different '
                                    + 'from requested, and force-overwrite'
                                    + ' is enabled'.format())
                self.data['fix_triggers'] = True
        return

    def __check_trigger_values(self):
        """checking the configured triggers vs the desired.
        This has an issue and does not check properly."""
        all_triggers = True
        if self.config['trigger']:
            if (len(self.config['trigger'].keys())
                    != len(self.config['trigger'].keys())):
                self.logger.warning('The number of triggers specfied is '
                                    + 'different then configured.')
                all_triggers = False
            for key in self.config['trigger'].keys():
                if key in self.data['trigger'].keys():
                    check_one = self.config[
                        'trigger'][key]['msgid'] == self.data[
                            'trigger'][key]['msgid']
                    check_two = self.config[
                        'trigger'][key]['pattern'] == self.data[
                            'trigger'][key]['pattern']
                    if check_one and check_two:
                        self.data['trigger'][key]['configured'] = True
                    else:
                        self.data['trigger'][key]['configured'] = False
                        all_triggers = False
        else:
            all_triggers = False
        return all_triggers

    def __check_action(self):
        """."""
        self.__check_action_diff()
        self.__check_action_same()
        return

    def __check_action_diff(self):
        """."""
        if self.config['action']:
            if self.config['action']['script'] != self.data['action']:
                if not self.data['force']:
                    print('Configured action is different from requested.')
                    user_override = ''
                    while ('y' not in user_override
                           and 'n' not in user_override):
                        user_override = input('Do you want to over write '
                                              + 'the action? (y)es or '
                                              + '(n)o: ').lower()
                        if 'y' in user_override:
                            self.data['fix_action'] = {'status': True,
                                                       'same_script': False}
                        elif 'n' in user_override:
                            self.data['fix_action'] = {'status': False,
                                                       'same_script': False}
                        else:
                            print('ERROR: Please use a (y)es or (n)o')
                else:
                    print('Configured action is different from '
                          + 'requested, and force-overwrite is enabled')
                    self.logger.warning('An outdated script may be '
                                        + 'registered, and force-overwrite '
                                        + 'is enabled'.format())
                    self.data['fix_action'] = {'status': True,
                                               'same_script': False}
        else:
            self.data['fix_action'] = {'status': False, 'same_script': True}
        return

    def __check_action_same(self):
        """."""
        if self.config['action']:
            if self.config['action']['script'] == self.data['action']:
                if not self.data['force']:
                    print('Configured action is same as from requested. '
                          + 'This can cause a known issue with the '
                          + 'event-handler.')
                    user_override = ''
                    while ('y' not in user_override
                           and 'n' not in user_override):
                        user_override = input('Do you want to re-register '
                                              + 'this script? (y)es or '
                                              + '(n)o: ').lower()
                        if 'y' in user_override:
                            self.data['fix_action'] = {'status': True,
                                                       'same_script': True}
                        elif 'n' in user_override:
                            self.data['fix_action'] = {'status': False,
                                                       'same_script': True}
                        else:
                            print('ERROR: Please use a (y)es or (n)o')
                else:
                    print('Configured action are different from '
                          + 'requested, and force-overwrite is enabled')
                    self.logger.warning('An outdated script may be '
                                        + 'registered, and force-overwrite '
                                        + 'is enabled'.format())
                    self.data['fix_action'] = {'status': True,
                                               'same_script': True}
        else:
            self.data['fix_action'] = {'status': False, 'same_script': True}
        return

    def __check_description(self):
        """."""
        if self.config['description']:
            if (self.config['description']['description']
                    != self.data['description']):
                self.logger.warning('Configured description does not match '
                                    + 'desired.')
                self.data['fix_description'] = True
                if not self.data['force']:
                    print('Configured description is different from '
                          + 'requested.')
                    user_override = ''
                    while ('y' not in user_override
                           and 'n' not in user_override):
                        user_override = input('Do you want to overwrite the '
                                              + 'description? (y)es or '
                                              + '(n)o: ').lower()
                        if 'y' in user_override:
                            self.data['fix_description'] = True
                        elif 'n' in user_override:
                            self.data['fix_description'] = False
                        else:
                            print('ERROR: Please use a (y)es or (n)o')
                else:
                    print('Configured description is different from '
                          + 'requested, and force-overwrite is enabled.')
                    self.logger.warning('Configured description is '
                                        + 'different from requested, and '
                                        + 'force-overwrite is '
                                        + 'enabled.'.format())
                    self.data['fix_description'] = True
        else:
            self.data['fix_description'] = True
        return

    def __check_action_timeout(self):
        """."""
        if self.config['action_timeout']:
            if self.config['action_timeout']['update']:
                self.logger.warning('Configured action-timeout does not '
                                    + 'match desired.')
                self.data['fix_action_timeout'] = True
                if not self.data['force']:
                    print('Configured action-timeout is different from '
                          + 'requested.')
                    user_override = ''
                    while ('y' not in user_override
                           and 'n' not in user_override):
                        user_override = input('Do you want to overwrite the '
                                              + 'action-timeout? (y)es or '
                                              + '(n)o: ').lower()
                        if 'y' in user_override:
                            self.data['fix_action_timeout'] = True
                        elif 'n' in user_override:
                            self.data['fix_action_timeout'] = False
                        else:
                            print('ERROR: Please use a (y)es or (n)o')
                else:
                    print('Configured action-timeout is different from '
                          + 'requested, and force-overwrite is enabled.')
                    self.logger.warning('Configured action-timeout is '
                                        + 'different from requested, and '
                                        + 'force-overwrite is '
                                        + 'enabled.'.format())
                    self.data['fix_action_timeout'] = True
        else:
            self.data['fix_action_timeout'] = True
        return

    def __check_delay(self):
        """."""
        if self.config['delay']:
            if self.config['delay']['update']:
                self.logger.warning('Configured delay does not match desired.')
                self.data['fix_delay'] = True
                if not self.data['force']:
                    print('Configured delay is different from requested.')
                    user_override = ''
                    while ('y' not in user_override
                           and 'n' not in user_override):
                        user_override = input('Do you want to overwrite the '
                                              + 'delay? (y)es or '
                                              + '(n)o: ').lower()
                        if 'y' in user_override:
                            self.data['fix_delay'] = True
                        elif 'n' in user_override:
                            self.data['fix_delay'] = False
                        else:
                            print('ERROR: Please use a (y)es or (n)o')
                else:
                    print('Configured delay is different from '
                          + 'requested, and force-overwrite is enabled.')
                    self.logger.warning('Configured delay is different '
                                        + 'from requested, and force-overwrite'
                                        + ' is enabled.'.format())
                    self.data['fix_delay'] = True
        else:
            self.data['fix_delay'] = True
        return

    def __check_interval(self):
        """."""
        if self.config['interval']:
            if self.config['interval']['update']:
                self.logger.warning('Configured interval does not '
                                    + 'match desired.')
                self.data['fix_interval'] = True
                if not self.data['force']:
                    print('Configured interval is different from '
                          + 'requested.')
                    user_override = ''
                    while ('y' not in user_override
                           and 'n' not in user_override):
                        user_override = input('Do you want to overwrite the '
                                              + 'interval? (y)es or '
                                              + '(n)o: ').lower()
                        if 'y' in user_override:
                            self.data['fix_interval'] = True
                        elif 'n' in user_override:
                            self.data['fix_interval'] = False
                        else:
                            print('ERROR: Please use a (y)es or (n)o')
                else:
                    print('Configured interval is different from '
                          + 'requested, and force-overwrite is enabled.')
                    self.logger.warning('Configured interval is different '
                                        + 'from requested, and '
                                        + 'force-overwrite is '
                                        + 'enabled.'.format())
                    self.data['fix_interval'] = True
        else:
            self.data['fix_interval'] = True
        return

    def __check_iterations(self):
        """."""
        if self.config['iterations']:
            if self.config['iterations']['update']:
                self.logger.warning('Configured iterations does not match '
                                    + 'desired.')
                self.data['fix_iterations'] = True
                if not self.data['force']:
                    print('Configured iterations is different from '
                          + 'requested.')
                    user_override = ''
                    while ('y' not in user_override
                           and 'n' not in user_override):
                        user_override = input('Do you want to overwrite the '
                                              + 'iterations? (y)es or '
                                              + '(n)o: ').lower()
                        if 'y' in user_override:
                            self.data['fix_iterations'] = True
                            break
                        elif 'n' in user_override:
                            self.data['fix_iterations'] = False
                            break
                        else:
                            print('ERROR: Please use a (y)es or (n)o')
                else:
                    print('Configured iterations is different from '
                          + 'requested, and force-overwrite is enabled.')
                    self.logger.warning('Configured iterations is different '
                                        + 'from requested, and '
                                        + 'force-overwrite is '
                                        + 'enabled.'.format())
                    self.data['fix_iterations'] = True
        else:
            self.data['fix_iterations'] = True
        return

    def __check_trigger_mode(self):
        """."""
        if self.config['trigger_mode']:
            if self.config['trigger_mode']['update']:
                self.logger.warning('Configured trigger-mode does not match '
                                    + 'desired.')
                self.data['fix_trigger_mode'] = True
                if not self.data['force']:
                    print('Configured trigger-mode is different from '
                          + 'requested.')
                    user_override = ''
                    while ('y' not in user_override
                           and 'n' not in user_override):
                        user_override = input('Do you want to overwrite the '
                                              + 'trigger-mode? (y)es or'
                                              + ' (n)o: ').lower()
                        if 'y' in user_override:
                            self.data['fix_trigger_mode'] = True
                        elif 'n' in user_override:
                            self.data['fix_trigger_mode'] = False
                        else:
                            print('ERROR: Please use a (y)es or (n)o')
                else:
                    print('Configured trigger-mode is different from '
                          + 'requested, and force-overwrite is enabled.')
                    self.logger.warning('Configured trigger-mode is '
                                        + 'different from requested, and '
                                        + 'force-overwrite is '
                                        + 'enabled.'.format())
                    self.data['fix_trigger_mode'] = True
        else:
            self.data['fix_trigger_mode'] = True
        return

    def __check_trigger_function(self):
        """."""
        if self.config['trigger_function']:
            if self.config['trigger_function']['update']:
                self.logger.warning('Configured trigger-function does '
                                    + 'not match desired.')
                self.data['fix_trigger_function'] = True
                if not self.data['force']:
                    print('Configured trigger-function is different from '
                          + 'requested.')
                    user_override = ''
                    while ('y' not in user_override
                           and 'n' in user_override):
                        user_override = input('Do you want to overwrite the '
                                              + 'trigger-function? (y)es or '
                                              + '(n)o: ').lower()
                        if 'y' in user_override:
                            self.data['fix_trigger_function'] = True
                        elif 'n' in user_override:
                            self.data['fix_trigger_function'] = False
                        else:
                            print('ERROR: Please use a (y)es or (n)o')
                else:
                    print('Configured trigger-function is different from '
                          + 'requested, and force-overwrite is enabled.')
                    self.logger.warning('Configured trigger-function is '
                                        + 'different from requested, and '
                                        + 'force-overwrite is enab'
                                        + 'led.'.format())
                    self.data['fix_trigger_function'] = True
        else:
            self.data['fix_trigger_function'] = True
        return

    def __register_event_handler(self):
        """Creates or modifies the event handler."""
        config = ['configure terminal']
        config.append('event-handler %s' % self.data['event_name'])
        config = config + self.__build_triggers()
        config = config + self.__build_action()
        config = config + self.__build_description()
        config.append('end')
        config.append('copy run start')
        config.append('y')
        CLI('\n'.join(config), False)
        return

    def __build_triggers(self):
        config = []
        if not self.data['new_config']:
            if self.data['fix_triggers']:
                if self.config['trigger']:
                    for key in self.config['trigger'].keys():
                        config.append('no '
                                      + self.config['trigger'][key]['line'])
                for trigger in self.data['trigger'].keys():
                    config.append('trigger {0} raslog {1} {2}'.format(
                        trigger, self.data['trigger'][trigger]['msgid'],
                        self.data['trigger'][trigger]['pattern']))
        else:
            for trigger in self.data['trigger'].keys():
                config.append('trigger {0} raslog {1} {2}'.format(
                    trigger, self.data['trigger'][trigger]['msgid'],
                    self.data['trigger'][trigger]['pattern']))
        return config

    def __build_action(self):
        config = []
        if not self.data['new_config']:
            if self.data['fix_action']['status']:
                if self.config['event_handler_activate']['status']:
                    config.append('top no event-handler activate %s'
                                  % self.data['event_name'])
                config.append('no action python-script %s'
                              % self.config['action']['script'])
                config.append('action python-script %s' % self.data['action'])
        else:
            config.append('action python-script %s' % self.data['action'])
        return config

    def __build_description(self):
        config = []
        if not self.data['new_config']:
            if self.data['fix_description']:
                config.append('description %s' % self.data['description'])
        else:
            config.append('description %s' % self.data['description'])
        return config

    def __activate_event_handler(self):
        """activates the event_handler."""
        config = ['configure terminal']
        config.append('event-handler activate %s' % self.data['event_name'])
        config.append(self.__build_action_timeout())
        config.append(self.__build_delay())
        config.append(self.__build_interval())
        config.append(self.__build_iterations())
        config.append(self.__build_trigger_mode())
        config.append(self.__build_trigger_function())
        config.append('end')
        config.append('copy run start')
        config.append('y')
        CLI('\n'.join(config), False)
        return

    def __build_action_timeout(self):
        if not self.data['new_config']:
            if self.data['fix_action_timeout']:
                value = 'action-timeout %s' % self.data['action_timeout']
            else:
                value = self.config['action_timeout']['line']
        else:
            value = 'action-timeout %s' % self.data['action_timeout']
        return value

    def __build_delay(self):
        if not self.data['new_config']:
            if self.data['fix_delay']:
                value = 'delay  %s' % self.data['delay']
            else:
                value = self.config['delay']['line']
        else:
            value = 'delay  %s' % self.data['delay']
        return value

    def __build_interval(self):
        if not self.data['new_config']:
            if self.data['fix_interval']:
                value = 'interval  %s' % self.data['interval']
            else:
                value = self.config['interval']['line']
        else:
            value = 'interval  %s' % self.data['interval']
        return value

    def __build_iterations(self):
        if not self.data['new_config']:
            if self.data['fix_iterations']:
                value = 'iterations %s' % self.data['iterations']
            else:
                value = self.config['iterations']['line']
        else:
            value = 'iterations %s' % self.data['iterations']
        return value

    def __build_trigger_mode(self):
        if not self.data['new_config']:
            if self.data['fix_trigger_mode']:
                value = 'trigger-mode %s' % self.data['trigger_mode']
            else:
                value = self.config['trigger_mode']['line']
        else:
            value = 'trigger-mode %s' % self.data['trigger_mode']
        return value

    def __build_trigger_function(self):
        if not self.data['new_config']:
            if self.data['fix_trigger_function']:
                if self.data['trigger_function'] == 'OR':
                    value = ('trigger-function %s'
                             % self.data['trigger_function'])
                else:
                    value = ('trigger-function %s time-window %s' % (
                             self.data['trigger_function'],
                             self.data['trigger_function_time']))
            else:
                value = self.config['trigger_function']['line']
        else:
            if self.data['trigger_function'] == 'OR':
                value = 'trigger-function %s' % self.data['trigger_function']
            else:
                value = ('trigger-function %s time-window %s' % (
                         self.data['trigger_function'],
                         self.data['trigger_function_time']))
        return value

    def __get_log_message(self):
        """Returns the latest log message text for the msgid(s) in
        LOG_MSGID_LIST."""
        self.logger.info('Executing show log raslog reverse.')
        log_output = CLI('show log raslog reverse | include '
                         + '|'.join(self.data['log_msgid_list']),
                         False).get_output()[0]
        msgid = log_output.split(', ')[1][1:-1]
        message = ', '.join(log_output.split(', ')[6:])
        self.data['log_message'][msgid] = message
        return

    def __get_logs(self):
        """Fetch the logs from either the raslog-triggers from the
        event-handler, or if that is not present, pull the most recent log
        from the show log raslog reverse.
        """
        if self.data['triggers_raw']:
            self.logger.info('Event-handler passed some data.')
            try:
                self.data['log_message'] = json.load(self.data['triggers_raw'])
            except NameError:
                self.__get_log_message()
            except ValueError:
                self.__get_log_message()
            except TypeError:
                self.__get_log_message()
        else:
            self.__get_log_message()
        return

    def do_unregistration(self):
        self.logger.info('removing the config for the event %s: ',
                         self.data['event_name'])
        config = ['configure terminal']
        config.append('no event-handler activate %s' % self.data['event_name'])
        config.append('no event-handler %s' % self.data['event_name'])
        config.append('end')
        config.append('copy run start')
        config.append('y')
        CLI('\n'.join(config), False)
        return


def main():
    """Creates an event handler with the same name as this script,
    or executes the actions desired on triggering.
    Usage:
    1. Copy the script to the SLX:
    copy scp://user:extreme@10.25.101.102//event_handler_template.py
        flash://event_handler.py
    2. Execute the script with the --register option:
    python event_handler.py -r
    3. Verify all is in order with 'show run event'.
    4. To Deactivate, use the --unregister option.

    Inline help and all options for the script can be gotten with --help
    """
    parser = argparse.ArgumentParser(
        description='Event handler script for the following syslogs: '
        + ', '.join(EVENT['LOG_MSGID_LIST']),
        usage="""Creates an event handler with the same name as this script,
        or executes the actions desired on triggering.
        Usage:
        1. Copy the script to the SLX:
        copy scp://user:extreme@HOST//event_handler_template.py
            flash://event_handler.py
        2. Execute the script with the --register option using python:
        python event_handler.py --register
        3. Verify all is in order with 'show run event'.
        4. To Deactivate, use the --unregister option.""")
    parser.add_argument('--register', '-r', action='store_true',
                        help='Register the script with the system.')
    parser.add_argument('--force-overwrite', '-f', action='store_true',
                        help='forcibly overwrite when registering the '
                        + 'script with the system.')
    parser.add_argument('--unregister', '-u', action='store_true',
                        help='Register the script with the system.')
    parser.add_argument('--raslog-triggers', nargs=argparse.REMAINDER,
                        help='Register the script with the system.')
    args = parser.parse_args()
    log_filename = sys.argv[0].split('/')[-1].split('.')[0] + '.log'
    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S%z')
    logging.info('Passed args where: %s', sys.argv[1:])
    the_event = EventHandler(EVENT, args.raslog_triggers,
                             args.force_overwrite)
    if args.register:
        the_event.do_registration()
    elif args.unregister:
        the_event.do_unregistration()
    else:
        the_event.do_actions()
    return


if __name__ == "__main__":
    main()
