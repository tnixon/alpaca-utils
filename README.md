# alpaca-utils
A collection of utilities to interact with the Alpaca API

### Installation
1) Clone the repository:
```commandline
git clone https://github.com/tnixon/alpaca-utils.git
```
2) Install the required packages:
```commandline
pip install -r requirements.txt
```

### Configuration
Before using the scripts in this repository, you need to set up your Alpaca API keys. 
You can obtain your API keys by signing up for an Alpaca account and navigating to the API Management page.

Once you have your API keys, you need to create a file named `alpaca.secrets` in the root of the repository 
and add the following lines:

```text
[DEFAULT]
key=<your API key ID>
secret=<your API secret key>
```
Replace `<your API key ID>` and `<your API secret key>` with your actual API keys.

### Usage
To run the script, use the following command:
```commandline
python data_downloader.py [--secrets <secrets file>] 
                          [--symbols <symbols file>] 
                          [--start_time <start time>] 
                          [--end_time <end time>]
                          [--output_dir <output directory>]
```
The arguments are as follows:
* `--secrets`: The path to the secrets file. If not specified, the script will look for a file named `alpaca.secrets` in the root of the repository.
* `--symbols`: The path to the file containing the symbols to download data for. If not specified, the script will look for a file named `symbols.txt` in the root of the repository.
* `--start_time`: The start time of the data to download. If not specified, the script will download data for the current day.
* `--end_time`: The end time of the data to download. If not specified, the script will download data up to the current time.
* `--output_dir`: The directory to save the downloaded data to. If not specified, the script will save the data to the `data` directory in the current working directory.

### Contributing
If you find a bug or have a suggestion for a new feature, feel free to open an issue or submit a pull request.

### License
This repository is licensed under the MIT License. See the LICENSE file for more details.