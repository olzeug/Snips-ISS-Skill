#!/usr/bin/env python3

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error):
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    import requests
    data = requests.get('http://api.open-notify.org/astros.json').json()
    amount = data['number']

    if not amount:
        answer = 'Es ist gerade niemand auf der ISS'
    elif amount == 1:
        answer = 'Auf der ISS ist gerade eine Person, {}.'.format(data['people'][0]['name'])
    else:
        people = '{} und {}'.format(', '.join(str(x['name']) for x in data['people'][:-1]), data['people'][-1]['name'])
        answer = 'Auf der ISS sind gerade {} Personen, {}'.format(amount, people)

    hermes.publish_end_session(intentMessage.session_id, answer)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("olzeug:getPeopleonISS", subscribe_intent_callback) \
         .start()
