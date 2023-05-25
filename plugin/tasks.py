import requests

from cloudify.decorators import operation
from cloudify.exceptions import NonRecoverableError

from vmware.vapi.vsphere.client import create_vsphere_client


def get_unverified_session():
    session = requests.session()
    session.verify = False
    requests.packages.urllib3.disable_warnings()
    return session

@operation
def my_task(ctx, **kwargs):
    session = get_unverified_session()
    connection_config = ctx.node.properties.get('connection_config', {})
    client = create_vsphere_client(
        server=connection_config.get('host'),
        username=connection_config.get('username'),
        password=connection_config.get('password'),
        session=session)
    list_of_vms = client.vcenter.VM.list()

    ctx.logger.info('list_of_vms {0}'.format(list_of_vms))
    
    