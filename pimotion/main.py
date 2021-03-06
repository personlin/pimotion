from pimotion import PiMotion
from cloudapp import CloudAppAPI
from cloudapp.exceptions import CloudAppHttpError
from m2x.client import M2XClient
from requests.exceptions import HTTPError, RequestException
import ConfigParser


Config = ConfigParser.ConfigParser()
Config.read('settings.cfg')


def callback(path):
    try:
        api = CloudAppAPI(Config.get('cloudapp', 'username'), Config.get('cloudapp', 'password'))
        url = api.upload(path)
        print 'Public URL: ' + url

        client = M2XClient(Config.get('m2x', 'api_key'))
        stream = client.device(Config.get('m2x', 'device_id')).stream(Config.get('m2x', 'stream'))
        result = stream.add_value(url)
        print "Posted URL to M2X stream %s" % Config.get('m2x', 'stream')
    except HTTPError, e:
        print 'ERROR: ' + e.message
    except RequestException, e:
    except CloudAppHttpError, e:
        print 'CloudApp ERROR:' + e.message


motion = PiMotion(verbose=True, post_capture_callback=callback)
motion.start()
