# cowrie-snort-log-analyzer

This project was part of my bachelor thesis.
My goal was to create an application which simplifies analysing LOG-Data.

The application is able to upload LOG-Data from [cowrie](https://github.com/cowrie/cowrie)
and [snort](https://www.snort.org/) to a local MySQL database and run different querys on it.
It was never intended that this application is used by some other than me. This means that the error
handling is not bulletproof.

## Installing / Getting started

Please run the setup file to install all dependencies.

```shell
pip install .
log_analyzer --help
```

Before running the application make sure, that the database credentials
are set in constants.py.

```python
HOST = "localhost"
USER = ""  # Add you db username here
PASSWORD = ""  # Add your db password here
DATABASE = ""  # Add your db name here
COWRIE_TABLE = ""  # Add name of cowrie table here
SNORT_TABLE = ""  # Add name of snort table here
```
Path: log_analyzer/constants.py

Make sure to add cowrie (.json) and snort LOG-files to the dedicated directory in /data.


## Features

* Upload cowrie and snort LOG-Data to a local MySQL database
* Fetch data from local MySQL database
* Add additional information (e.g., location information for each ip address)
* Run various querys on the database

## Configuration

#### Argument 1
Type: `String`
Example: `-a`

Options:
```bash
    log_analyzer -a # Upload Cowrie-Logs to database
    log_analyzer -b # Upload SNORT-Logs to database
    log_analyzer -c # Plot: x=country, y=attack_count
    log_analyzer -d # Plot x=datetime, y=SSH connections
    log_analyzer -e # Get total SSH connections from each country
    log_analyzer -f # Get total SSH connections per day

```

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

## Licensing

This project is licensed under GNU General Public License v3.0. 

This site or product includes IP2Location LITE data available
from <a href="https://lite.ip2location.com">https://lite.ip2location.com.