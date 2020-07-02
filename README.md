# Live Stock Tracker

A piece of code to track live stock prices and to get notifications for the changes in stock prices on your linux pc using [yahoo_fin](http://theautomatic.net/yahoo_fin-documentation/) package.

## Quick Setup

You can quickly download the dependencies using the command given below.

```shell
pip install -r requirements.txt
```

Install [SoX](http://sox.sourceforge.net/), with MP3 support on Ubuntu or Debian derivatives:

```shell
sudo apt-get install sox libsox-fmt-mp3
```

## Getting Started

### For tracking a single company

```shell
python3 stock_tracker.py --single --company 'Microsoft' --abbreviation 'msft' --delay 5
```

### For tracking multiple companies

```shell
python3 stock_tracker.py --multi --companies 'Microsoft' 'Netflix' 'Facebook' --delay 5
```

## Stop tracking

To stop the program just press `Ctrl+Esc` keys together.
