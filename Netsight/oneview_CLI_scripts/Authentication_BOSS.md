# Authentication on BOSS - How To

Script does configure authentication on ports and Radius on BOSS devices

## Special preparation for Extreme Management Center 8.1.2 and 8.1.3
There are two unhandled prompts for ERS devices. If the radius is configured the ERS will ask for shared secret. The scripting engine does timeout.

Example (there is space behind the column):
```
radius server host 192.168.0.1 key acct-enable
Enter key: 
Confirm key: 
radius server host 192.168.0.1 secondary key acct-enable
Enter key: 
Confirm key: 
```

If you want to use this script with Extreme Management Center then you need to edit `appdata/scripting/CLIRules.xml` and modify the prompt definition.

### Original:
```xml
    <Rule name="Avaya (SynOptics)">
        <ShellPrompt>
            <defaultPrompt>
                <prompt>(?:\((.+?)\))?[>#]?$</prompt>
            </defaultPrompt>
```
### Modified:
```xml
    <Rule name="Avaya (SynOptics)">
        <ShellPrompt>
            <defaultPrompt>
                <prompt>(?:\((.+?)\))?[>#:]\s?$</prompt>
            </defaultPrompt>
```

# Support
_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).
>Be Extreme