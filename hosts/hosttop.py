from taskdo.utils.base.ansible_api import ANSRunner
from hosts.models import Host

while 1:
    hosts = []
    hostnames = []
    all_hosts = Host.objects.all()
    for host in all_hosts:
        host = dict(host)
        hosts.append(host)
        hostnames.append(host['hostname'])

    resource = dict()

    resource['test'] = dict()
    resource['test']['hosts'] = hosts

    rbt = ANSRunner(resource)

    # rbt.run_model(host_list=[hostname, ], module_name='ping', module_args="")
    rbt.run_model(host_list=hostnames, module_name='setup', module_args="filter=ansible_*_mb")

    data = rbt.get_model_result()
    for hostname in hostnames:
        host = Host.objects.filter(hostname=hostname)[0]
        hostname = hostname.replace('.', '_')
        try:
            freememory =  data['success'][hostname]['ansible_facts']['ansible_memfree_mb']
            host.freememory = freememory
            allmemory = data['success'][hostname]['ansible_facts']['ansible_memtotal_mb']
            host.allmemory = allmemory
            host.save()
        except Exception:
            pass



    print(1)
