from cloudify.decorators import operation
from cloudify.exceptions import NonRecoverableError

from com.vmware.content.library_client import Item

def get_item_id_by_name(ctx, client, name):
    find_spec = Item.FindSpec(name=name)
    item_ids = client.library_item_service.find(find_spec)
    item_id = item_ids[0] if item_ids else None
    if item_id:
        ctx.logger.info('Library item ID: {0}'.format(item_id))
    else:
        ctx.logger.info("Library item with name '{0}' not found".format(name))
    return item_id

@operation
def my_task(ctx, **kwargs):
    session = get_unverified_session()
    connection_config = ctx.node.properties.get('connection_config', {})
    client = ServiceManagerFactory.get_service_manager(connection_config.get('host'),
                                                       connection_config.get('username'),
                                                       connection_config.get('password'),
                                                       True)
    library = get_item_id_by_name(ctx, client, 'test-ahmad')

    
    