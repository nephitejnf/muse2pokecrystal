# Running the Script

Running the script is pretty simple.

```
muse2pokecrystal -h
```
This shows the short flags to remind you incase you forget.

`--score` or `-i` both take input.
`--code` or `-o` both are your output.


```
muse2pokecrystal --score <musicxml> --code <asm>
```
This is just the long form of
```
muse2pokecrystal -i <musicxml> -o <asm>
```

If you want don't want to parse the noise channel or file doesn't have a drumset,
use the `--noiseless` option:
```
muse2pokecrystal -i <musicxml> -o <asm> --noiseless
```
This will only output channels 1 through 3 and edit the header accordingly.

This can be run locally in your folder of placed in your binaries.
It requires Python 3 to run (sorry Python 2 bois).

You will need to manually tweak your code once processed by the script.
This only provides a basic skeleton to work with for finishing with your perfections.
The asm should open in GBNote just fine.
