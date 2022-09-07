# Configuration

The configuration file uses an INI format to define each music channel's settings. It defines various settings needed to set the sound of your channel.

Channels 1 through 3 have the same basic settings; notetype, intensity, tone, stereopanning, and vibrato, which includes settings for delay and extent. These values are defined using hexadecimal values. There is also support for custom commands on each channel if such commands are supported in the intended project.

Some channels have unique setting due to their channel type. Channels 1 and 2 have an additional setting for dutycycle for affecting the square waveform of the channel. The only accepted values are 0-3, which make the waveform 12.5%, 25%, 50% and 75% respectively.

Channel 4 is a dedicate noise channel. The only setting available for it in the configuration are note type, noise toggle, and stereopanning. Custom commands are also available if the intended project supports it.

```ini
[Channel 1]

volume = $77

notetype = $c

intensity = $95

dutycycle = $2

tone =

stereopanning = $ff

vibrato = false

vibrato_delay = $00

vibrato_extent = $00
```
