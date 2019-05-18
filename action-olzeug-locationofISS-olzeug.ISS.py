#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    import urllib.request,json
    response = json.loads(urllib.request.urlopen('http://api.open-notify.org/iss-now.json').read().decode())
    if(response['iss_position']['latitude'][0] == '-'):
        einheit1 = "West"
        wert1 = response['iss_position']['latitude'][1:-5]
    else:
        einheit1 = "Ost"
        wert1 = response['iss_position']['latitude'][0:-5]
    if(response['iss_position']['longitude'][0] == '-'):
        einheit2 = "Süd"
        wert2 = response['iss_position']['longitude'][1:-5]
    else:
        einheit2 = "Nord"
        wert2 = response['iss_position']['longitude'][0:-5]
    hermes.publish_end_session(intentMessage.session_id,'Die ISS ist gerade bei {} und {}'.format(str(wert2+' Grad '+einheit2),str(wert1+' Grad '+einheit1)))
    


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("olzeug:locationofISS", subscribe_intent_callback) \
         .start()
