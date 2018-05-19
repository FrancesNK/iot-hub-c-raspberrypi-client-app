import bluetooth
import os
  
print("performing inquiry...")
  
nearby_devices = bluetooth.discover_devices(lookup_names = True)
  
#print("found %d devices" % len(nearby_devices))
  
for addr, name in nearby_devices:
    #print("  %s - %s" % (addr, name))
    if name == 'techfair':
        os.system('/opt/Citrix/ICAClient/util/pnabrowse -L "Windows 2012 R2 Desktop" -U administrator -P citrix -D tf.local http://10.158.141.214/citrix/store/pnagent/config.xml')
        exit
