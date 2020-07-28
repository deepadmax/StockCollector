# Stock Collector
Use the [scheduler](#scheduler) for downloading stock data and the [sanitizer](#sanitizer) to process it.

## Scheduler
This will schedule to download stock data of certain symbols every set period.

```sh
python scheduler.py --sym BTC-USD ETH-USD --period 7 -v
```

### Flags
| flags | description | default | required |
|-------|-------------|---------|----------|
| `--sym` | list of symbols | - | yes |
| `--period` | interval in days | 28 | no |
| `--path` | download directory | "~/.remus/stock-data/raw" | no |
| `--verbose` `-v` | be verbose | false | no |

### Choose your stocks
Which stocks are saved, are entered into the `--sym` argument.<br>
Make sure that all stocks you list are available
at [Yahoo! Finance](https://finance.yahoo.com/).

```sh
--sym BTC-USD ETH-USD LTC-USD
```

### How often to download
If you want to change how often the program is scheduled, use the `--period` flag.

```sh
--period 14
```

### Custom directory
All stocks are stored in their own individual folders,
but their collective directory depends on the argument of `--path`.

```sh
--path /path/to/your/directory
```

### Verbose
If you want the program to detail the progress, printing the beginning
and end of each time frame for each symbol whenever it is downloaded,
use the `--verbose` flag.

```
Acquired timeframe 2020-01-01 -> 2020-01-28 for LTC-USD
```


## Sanitizer
It reads through and processes the raw stock data that has been downloaded with the scheduler.

```sh
python sanitizer.py --sym ETH-USD
```

### Flags
| aliases | description | default | required |
|---------|-------------|---------|----------|
| `--sym` | list of symbols  | all | no |
| `-s` `--src` | source directory | "~/.remus/stock-data/raw" | no |
| `-d` `--dest` | output directory | "~/.remus/stock-data/clean" | no |
| `--verbose` `-v` | be verbose | false | no |

### Stocks to process
Just [as with the scheduler](#choose-your-stocks), stock symbols are entered following `--sym` flag.<br>
Folders with these names must exist in the source directory.

### Source and destination
By default, the program looks for downloaded data in [the default folder for the scheduler](#custom-directory). You can set this using `--src`.<br>
Select in which folder to store the processed data, with `--dest`.