# Starting the Process in Musescore
Open the Template.musicxml file in Musescore.

Alternatively, start up Musescore and create a new score. It's pretty simple, just start an empty score and pick your instruments.

### Channels
The script is very strict about the order and quantity of the instruments. Three instruments are required with the drumset being optional.
If you have a drumset, make sure it's at the bottom.
While technically any instrument can be used for channels 1-3, it is _strongly_ recommended picking channels 1 and 2 as square instruments
(under the electronic instuments) as those are the first two channels on a Gameboy.
For channel 3, a sine wave or saw wave instrument is heavily advised.
There is only one drumset under percussion for channel 4. It can be omited if you don't need it.
Using anything other than a drumset will not work or work as expected.

Instruments can be changed at any time in Musescore by pressing `i`.
The template file is set up with the four recommended instruments by default.

### Writing your score
Musescore has an interactive tour/tutorial that you can follow to learn to use it, very handy.
It'll show you how to enter notes on the score and how to make minor changes to it.

If you have music material you are sourcing, you may need to make some creative changes to make it work for pokecrystal.
You cannot have chords in a single channel on the GameBoy, so you need to make sure that there is **only one note at a time per channel**.
Because of the way this works, you can still make chords, but using multiple channels.
Alternatively, notes in a chord can be played sequentially in a channel if the chord is heavily repeated.

Tuplets are currently unsupported. They can be faked by alternating between lengths every other note.
For example, ` 1/4 - 1/4 - 1/4` in a triplet could be `1/8 - 1/4 - 1/8`.

Tied notes are supported. However, **any tie lasting longer than a whole note is wholly unsupported at this time**.

Notes must be no smaller than `1/16`.

### Music Sources
In most cases, the music you source will not fulfil every requirement needed to convert the score correctly. The best approach is to copy/paste
measures from the source that contain the desired melody and harmony and edit them to spec in the score to be exported.

#### Importing MIDIs *(Recommended)*
You can import MIDIs into Musescore albeit with varying degrees of success. Note lengths can be garbled and much of the data
(such as the scores key, time signature, and a staff's clef) will not be there. More often than not, MIDIs are simply extremely basic groundwork
to help you get started.

#### Native Musescore Sources
Sourcing from a native Musescore or MusicXML file will generally give the cleanest results. [Musescore has a website](https://musescore.com)
but recently put up a paywall to restrict downloading access. If you have a Musescore.com account **use this method!**

#### Importing PDFs
[Musescore's website](https://musescore.com/import) offers free experimental functionality to convert PDFs to scores.
Often times this process causes more problems than it's worth. Unless this is the only way to get the source music you want, use a midi.

#### Importing from Finale NotePad (*.mus)
Some sites only offer downloads for `.mus` files, which can't be directly opened in Musescore. The file has to be opened in Finale NotePad
and then exported to MusicXML within Finale. This method should also work for the trial version of Finale. This has not yet been tested.

### Saving your MusicXML
You can save the project in Musescore's format, but I recommend just exporting as MusicXML from the file menu > export.
You can still open the MusicXML in Musescore for later editing; that way you leave less artifacts later.
The MusicXML won't be edited by the script, just read.

