# Running the Script

Running the script is pretty simple.

## Help and Basic Usage
```
muse2pokecrystal.py -h
```
This shows the short flags to remind you in case you forget.

Unless Muse2pokecrystal is installed as a system package, you likely don't have it
in your PATH and will likely get a `command not found` error.
If running it this way doesn't work, you can try the varying ways below.
```sh
# Run directly
./muse2pokecrystal.py
# Run explicitly with the Python interpreter you choose
python muse2pokecrystal.py
py muse2pokecrystal.py
```

Basic usage is simple, give your input musicxml score and specify the output file name.
```
muse2pokecrystal.py <musicxml> <asm>
```

## Configuration Options

### Override Detected Song Name
If the script fails to detect the song name or you want to export it using a different name,
use the `--name` parameter:
```
muse2pokecrystal.py <musicxml> <asm> --name "<Your Song Name>"
```

### Don't Parse Noise Channel
If you want don't want to parse the noise channel or file doesn't have a drumset,
use the `--noiseless` parameter. This will only output channels 1 through 3 and edit
the header accordingly.
```
muse2pokecrystal.py <sicxml> <asm> --noiseless
```

### Override Detected Tempo
If you want to manually specify a tempo, use the `--tempo` parameter:
```
muse2pokecrystal.py <musicxml> <asm> --tempo <bpm>
```

### Parse with Selected Configuration File
Muse2pokecrystal uses configuration files alongside MusicXML files to specify pokecrystal
specific commands that run at the very beginning of each music channel. (Better solution?)
An example configuration file can be found in the root of the repository.
```
muse2pokecrystal.py <musicxml> <asm> --config <config>
```

### Don't Do Optimizations
Rudimentary optimization is currently done by default for output files.
This can be disabled if you prefer to do optimization by hand or using other tools.
```
muse2pokecrystal.py <musicxml> <asm> --no-optimizations
```

### Force Overwriting Destination File
Sometimes you don't want to be prompted to overwrite files when creating new songs.
Take when using this option as it will overwrite **any** existing file.
If you use this option, especially as root, you run risks of breaking things or loosing
precious work.
```
muse2pokecrystal.py <musicxml> <asm> --overwrite
```

## Runtime Options

### Color Output
Color output is supported by toggling the respective flag.
```
muse2pokecrystal.py <musicxml> <asm> --colored-output
```
