import requests

from com.vmware.cis_client import Session

from vmware.vapi.lib.connect import get_requests_connector
from vmware.vapi.security.session import create_session_security_context
from vmware.vapi.security.user_password import \
    create_user_password_security_context
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory


def get_jsonrpc_endpoint_url(host):
    return "https://{}/api".format(host)


def connect(host, user, pwd, skip_verification=False, cert_path=None, suppress_warning=True):
    host_url = get_jsonrpc_endpoint_url(host)

    session = requests.Session()
    if skip_verification:
        session = create_unverified_session(session, suppress_warning)
    elif cert_path:
        session.verify = cert_path
    connector = get_requests_connector(session=session, url=host_url)
    stub_config = StubConfigurationFactory.new_std_configuration(connector)

    return login(stub_config, user, pwd)


def login(stub_config, user, pwd):
    user_password_security_context = create_user_password_security_context(user,
                                                                           pwd)
    stub_config.connector.set_security_context(user_password_security_context)

    session_svc = Session(stub_config)
    session_id = session_svc.create()
    session_security_context = create_session_security_context(session_id)
    stub_config.connector.set_security_context(session_security_context)

    return stub_config


def logout(stub_config):
    if stub_config:
        session_svc = Session(stub_config)
        session_svc.delete()


def create_unverified_session(session, suppress_warning=True):
    session.verify = False
    if suppress_warning:
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    return session
