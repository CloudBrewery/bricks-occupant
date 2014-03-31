#A libvirt VM agent

Needs two virtio devices to run:

    <channel type='file'>
      <source path='/tmp/instance123.log'/>
      <target type='virtio' name='org.clouda.1'/>
      <alias name='channel0'/>
      <address type='virtio-serial' controller='0' bus='0' port='2'/>
    </channel>
    <channel type='unix'>
      <source mode='bind' path='/tmp/instance123.socket'/>
      <target type='virtio' name='org.clouda.0'/>
      <alias name='channel1'/>
      <address type='virtio-serial' controller='0' bus='0' port='1'/>
    </channel>
