import re, logging, os
import urllib.request
from urllib.parse import urlencode
from flask import redirect

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('SSI_LOGLEVEL', 'WARNING').upper())

class SteamSignIn:
    _provider = 'https://steamcommunity.com/openid/login'

    def redirect_user(self, str_post_data):
        logger.info('Invoked the Flask RedirectUser!')
        resp = redirect('{0}?{1}'.format(self._provider, str_post_data), 303)
        resp.headers["Content-Type"] = 'application/x-www-form-urlencoded'
        return resp

    def construct_url(self, response_url):

        auth_parameters = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': response_url,
            'openid.realm': response_url,
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
        }

        logger.info('Returning encoded URL.')
        return urlencode(auth_parameters)

    def validate_results(self, results):

        logger.info('Validating results of attempted log-in to Steam.')
        validation_args = {
            'openid.assoc_handle': results['openid.assoc_handle'],
            'openid.signed': results['openid.signed'],
            'openid.sig': results['openid.sig'],
            'openid.ns': results['openid.ns']
        }

        signed_args = results['openid.signed'].split(',')

        for item in signed_args:
            item_arg = 'openid.{0}'.format(item)
            if results[item_arg] not in validation_args:
                validation_args[item_arg] = results[item_arg]

        validation_args['openid.mode'] = 'check_authentication'
        parsed_args = urlencode(validation_args).encode("utf-8")
        logger.info('Encoded the validation arguments, prepped to send.')

        with urllib.request.urlopen(self._provider, parsed_args) as requestData:
            response_data = requestData.read().decode('utf-8')
            logger.info("Sent request to {0}, got back a response.".format(self._provider))

        if re.search('is_valid:true', response_data):
            matched64_id = re.search('https://steamcommunity.com/openid/id/(\d+)', results['openid.claimed_id'])
            if matched64_id is not None or matched64_id.group(1) is not None:
                return matched64_id.group(1)
            else:
                return False
        else:
            return False
