PowerOne Plug-in for Smarthome.py
-------------------------------

Plug-in for PowerOne inverter with network interface for [SmartHome.py](http://mknx.github.io/smarthome/).

Currently running for my PowerOne TRIO-7.5-TL-OUTD.

Supported functions:

* Reading values from the inverter periodically

Plug-in can be used as command line tool (Python module argparse required).

Sample items.conf

```
[inverter]
    [[power_out]]
        type = num
        powerone_var = pout_KW 
        visu_acl=rw
    # Special item, to get power_out in watts
    [[power_out_watt]]
        type = num
        visu_acl=rw
        eval = sh.inverter.power_out() * 1000
        eval_trigger = inverter.power_out
    [[status]]
        type = str
        powerone_var = status 
        visu_acl=rw
    [[day_kwh]]
        type = num
        powerone_var = eday_KWh 
        visu_acl=rw
    [[yesterday_kwh]]
        type = num
        visu_acl=rw
        sqlite=yes
    [[week_kwh]]
        type = num
        powerone_var = eweek_KWh 
        visu_acl=rw
    [[month_kwh]]
        type = num
        powerone_var = emonth_KWh 
        visu_acl=rw
    [[year_kwh]]
        type = num
        powerone_var = eyear_KWh 
        visu_acl=rw
        
    [[iin1]]
        type = num
        powerone_var = iin1 
        visu_acl=rw
    [[vin1]]
        type = num
        powerone_var = vin1 
        visu_acl=rw
    [[pin1]]
        type = num
        powerone_var = pin1 
        visu_acl=rw
        
    [[iin2]]
        type = num
        powerone_var = iin2 
        visu_acl=rw
    [[vin2]]
        type = num
        powerone_var = vin2 
        visu_acl=rw
    [[pin2]]
        type = num
        powerone_var = pin2 
        visu_acl=rw
    
```

Configuration in SmartHome.py plugin.conf:

```
[powerone]
    class_name = Powerone
    class_path = plugins.powerone
    host = 192.168.1.1 # ip address of inverter
    cycle = 60 # default 300 seconds
```

