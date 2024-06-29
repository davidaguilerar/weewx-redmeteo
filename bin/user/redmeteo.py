# 2020/2024 by Red Meteorologica Aficionada de Chile (Chilean Hobbyist Weather Network).
# Portions of code from WEEWX-WINDGURU

"""
ENGLISH
This WeeWX extension uploads data to Redmeteo.cl
http://redmeteo.cl/
To join, you have to write an email to redmeteoaficionadachile@gmail.com (ideally in Spanish)
It's allowed to submit data on 10-minute intervals.

Minimal configuration:

[StdRESTful]
    [[Redmeteo]]
        idestacion = WEATHERSTATIONID
        claveestacion = STATIONKEY

Redmeteo.cl does not have a well documented API, but sending an email, the Redmeteo team are able to quickly respond your questions.

EXAMPLE: http://redmeteo.cl/subir.php?ID=WEATHERSTATIONID&PASSWORD=STATIONKEY&tempf=outTemp&humidity=RH&dewptf=DewPoint&baromin=Pressure&baromabsin=AbsolutePressure&windspeedmph=WindSpeed&winddir=WindDir&dailyrain=DailyRain&windgustmph=WindGust&solarradiation=radiation&UV=UV&rainrate=rainRate


ESPAÑOL
Esta extension de WeeWX sube datos a Redmeteo.cl.
http://redmeteo.cl/
Para registrarte, debes escribir a redmeteoaficionadachile@gmail.com
Se admite envios cada 10 minutos (post_interval)
Configuracion minima:

[StdRESTful]
    [[Redmeteo]]
        idestacion = ID_ESTACION_MET_REDMETEO
        claveestacion = CLAVE_ESTACION

Redmeteo.cl no tiene una API documentada pero escribiendo al correo,
 pueden responder rapidamente con las dudas
 
"""

try:
    # Python 3
    import queue
except ImportError:
    # Python 2
    import Queue as queue
try:
    # Python 3
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib import urlencode
import re
import sys
import time

import weewx
import weewx.restx
import weewx.units

VERSION = "0.2"

if weewx.__version__ < "3":
    raise weewx.UnsupportedFeature("WeeWX 3 is required, you have %s" %
                                   weewx.__version__)


try:
    # Test for new-style weewx logging by trying to import weeutil.logger
    import weeutil.logger
    import logging
    log = logging.getLogger(__name__)

    def logdbg(msg):
        log.debug(msg)

    def loginf(msg):
        log.info(msg)

    def logerr(msg):
        log.error(msg)

except ImportError:
    # Old-style weewx logging
    import syslog

    def logmsg(level, msg):
        syslog.syslog(level, 'Redmeteo.cl: %s' % msg)

    def logdbg(msg):
        logmsg(syslog.LOG_DEBUG, msg)

    def loginf(msg):
        logmsg(syslog.LOG_INFO, msg)

    def logerr(msg):
        logmsg(syslog.LOG_ERR, msg)

def _mps_to_knot(v):
    from_t = (v, 'meter_per_second', 'group_speed')
    return weewx.units.convert(from_t, 'knot')[0]

class Redmeteo(weewx.restx.StdRESTbase):
    def __init__(self, engine, config_dict):
        """Este servicio reconoce el siguiente login

        idestacion: ID de usuario o estacion en Redmeteo.cl / 
        clave: Clave de la estación en Redmeteo.cl / Station Key

        """
        super(Redmeteo, self).__init__(engine, config_dict)
        loginf("service version is %s" % VERSION)
        site_dict = weewx.restx.get_site_dict(config_dict, 'Redmeteo', 'idestacion', 'claveestacion')
        if site_dict is None:
            return

        try:
            site_dict['manager_dict'] = weewx.manager.get_manager_dict_from_config(config_dict, 'wx_binding')
            #dbm = self.engine.db_binder.get_manager('wx_binding')
        except weewx.UnknownBinding:
            pass

        self.archive_queue = queue.Queue()
        self.archive_thread = RedmeteoThread(self.archive_queue, **site_dict)
        self.archive_thread.start()
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)
        loginf("Data will be uploaded for %s" % site_dict['idestacion'])

    def new_archive_record(self, event):
        self.archive_queue.put(event.record)


class RedmeteoThread(weewx.restx.RESTThread):
    _SERVER_URL = 'https://redmeteo.cl/subir.php'
    _DATA_MAP = {'tempf': ('outTemp', '%.1f'),              # F
                 'winddir': ('windDir', '%.0f'),            # degree
                 'windspeedmph': ('windSpeed', '%.1f'),     # mph
                 'windgustmph': ('windGust', '%.1f'),       # mph
                 'baromin': ('barometer', '%.3f'),          # inHg
                 'baromabsin': ('pressure', '%.3f'),        # inHg
                 'humidity': ('outHumidity', '%.0f'),       # %
                 'dailyrainin': (('dayRain'), '%.3f'),      # in
                 'monthlyrainin': (('monthRain'), '%.3f'),  # in
                 'yearlyrainin': (('yearRain'), '%.3f'),    # in
                 'rainin': (('hourRain'), '%.3f'),          # in
                 'rainratein': (('rainRate'), '%.3f'),      # in/h
                 'dewptf': ('dewpoint', '%.1f'),            # F
                 'UV': ('uv', '%.0f'),                      # index (dimensionless)
                 'solarradiation': ('radiation', '%.0f')    # W/m^2
                 }

    def __init__(self, queue, idestacion, manager_dict,
                 server_url=_SERVER_URL, skip_upload=False,
                 post_interval=600, max_backlog=sys.maxsize, stale=None,
                 log_success=True, log_failure=True,
                 timeout=600, max_tries=2, retry_wait=5):
        super(RedmeteoThread, self).__init__(queue,
                                             protocol_name='Redmeteo',
                                             manager_dict=manager_dict,
                                             post_interval=post_interval,
                                             max_backlog=max_backlog,
                                             stale=stale,
                                             log_success=log_success,
                                             log_failure=log_failure,
                                             timeout=timeout,
                                             max_tries=max_tries,
                                             retry_wait=retry_wait,
                                             skip_upload=skip_upload)
        self.idestacion = idestacion
        self.claveestacion = claveestacion
        self.server_url = server_url

    def check_response(self, response):
        lines = []
        for line in response:
            lines.append(line)
        msg = b''.join(lines)
        if not msg.decode('utf-8').endswith('OK'):
            raise weewx.restx.FailedPost("Server response: %s" % msg)

    def format_url(self, in_record):
        # put everything into the right units and scaling
        record = weewx.units.to_US(in_record)
        if 'windSpeed' in record and record['windSpeed'] is not None:
            record['windSpeed'] = _mps_to_knot(record['windSpeed'])
        if 'windGust' in record and record['windGust'] is not None:
            record['windGust'] = _mps_to_knot(record['windGust'])

        # put data into expected structure and format
        time_tt = time.localtime(record['dateTime'])
        values = {
            'ID': self.idestacion,
            'PASSWORD': self.claveestacion
        }

        for key in self._DATA_MAP:
            rkey = self._DATA_MAP[key][0]
            if rkey in record and record[rkey] is not None:
                values[key] = self._DATA_MAP[key][1] % record[rkey]
        url = self.server_url + '?' + urlencode(values)
        if weewx.debug >= 2:
            logdbg('url: %s' % (url))
        return url
