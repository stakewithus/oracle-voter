# oracle-voter

## Usage

```
Usage:
  python oracle-voter/main.py start <validator> <wallet> [--node <lcd_node_addr> --vote-period <vote_period> --password <password>]
  python oracle-voter/main.py ( -h | --help )
  python oracle-voter/main.py version
Options:
  -h --help    Show this screen.

```

## Testing

```
pytest --cov=oracle-voter

```

## Install Dependencies

- Requires Python 3.7 +
```
virtualenv -p python3 venv
```
- Pip Packages

```
source venv/bin/activate
(venv) pip install -r requirements.txt
```

## Requirements
- Validator Address
- Working LCD Node 
- `terracli` is in the user's path
   It is used for account management

- Valid Account Name and Password stored in home folder for `terracli`


## Common Problems

1. I Started the `oracle-voter`, nothing shows
- Are you able to connect to the LCD Node?
