# oracle-voter

## Usage

```
"""terra-oracle-voter
usage: main.py [-h] [--from wallet_name] [--node node] [--chain-id chain_id]
               [--vote-period vote_period] [--password password]
               [--home home_dir] [--gas-prices gas_prices] [--version]
               validator
"""
```

## Sample Output

```
----------(139137)---------
----------Votes ---------
1. [DC086A618A2D6EA9C7A3404294FC4E1077907434233F02B6AC50020B7B5C3D0D]
-- Msgs
-- Px 308.013000000000000000 Salt: e804 Denom: ukrw 
-- Px 697.569000000000000000 Salt: 43fc Denom: umnt 
-- Px 0.188793000000000000 Salt: 4428 Denom: usdr 
-- Px 0.259340000000000000 Salt: ced1 Denom: uusd 
-- Result: True Height: 139132
2. [15A307ADCBBA2C8D378251AEA49CBCF353C49BE043BFE0464D35F039D9E80319]
-- Msgs
-- Px 307.752000000000000000 Salt: 5438 Denom: ukrw 
-- Px 696.978000000000000000 Salt: 7473 Denom: umnt 
-- Px 0.188633000000000000 Salt: c36e Denom: usdr 
-- Px 0.259120000000000000 Salt: 0457 Denom: uusd 

----------PreVotes ---------
1. [E64311DBA13ED06D788D13613790467F8B2D4690D0839D463F768CD6F9A5A51A]
-- Msgs
-- Hash e15e9283e0f58c6a1d5d1a16c2e67688c2a9ada7 Denom: ukrw Salt: e804
-- Hash 3937a67d864315c393b729b66ca33a45bff10bf0 Denom: umnt Salt: 43fc
-- Hash faffbb862aec8891eb6c662af4425f76739c459d Denom: usdr Salt: 4428
-- Hash 9bb85b5a2eb31d13b0b69a1ec0bf43c1458371aa Denom: uusd Salt: ced1
-- Result: True Height: 139129
2. [3FA75E9BE216ED9C3DB2DF1EF7E6D1BC1A3E374FA80C55F242640B58A718B22D]
-- Msgs
-- Hash ef9404df89468e0dc8865d1ada2d5344c0aafb12 Denom: ukrw Salt: 5438
-- Hash 43b89e7bb230f3d52dcaa86f9a0741e7879e8473 Denom: umnt Salt: 7473
-- Hash 6465e79296650fc5a5444fb5820fef003f359893 Denom: usdr Salt: c36e
-- Hash 8de522faf1be1721704afd19b756879d4c1cd3e6 Denom: uusd Salt: 0457
-- Result: True Height: 139132
3. [1CDE750756A1E2F1F162FBE3E07DDCD7FADECEF3BF54B599CDD6DD87F7100FFA]
-- Msgs
-- Hash 6bcbac47fafc9c491175d0ec05117f797203cb6e Denom: ukrw Salt: df9f
-- Hash bdcc3347f1bba38e9c685cfcef8165d8eb76d140 Denom: umnt Salt: 61d1
-- Hash 2df9177841a322ab1d31166e05bb435331ca3de3 Denom: usdr Salt: beb1
-- Hash 0d811a7ab9c3aae3db68fb3e902b89eb4749159c Denom: uusd Salt: ef3f
----------(139137)---------

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
