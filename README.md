# DownloadSubs
Python script to download subtitles for movies and series

## Requirements
Please install both [subliminal](https://github.com/Diaoul/subliminal) and [mediainfo](https://mediaarea.net/nl/MediaInfo) in order for this script to function.

## Usage
Usage is as follows:
`python3 downloadSubs.py [commands] "/dir/to/videos" ["more/dirs"]`
The extra parameters are:
- `-R` for recursive search for video files
- `-l lang1,lang2,lang3,...` to override default languages. Languages have to be the default language codes (e.g. nl for Dutch) and they have to be separated by a comma, without spaces.
- `-print` to see the progress of the subtitle downloading

So `python3 downloadSubs.py -R -l nl,en,fr "~"` will download French, Dutch and English subtitles for all video files in the home map and all the maps in the home map.
