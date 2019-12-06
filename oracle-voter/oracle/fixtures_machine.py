from urllib.parse import urlencode


def vp_0_mock_account(
    m,
    node_addr="",
    cli_accounts=list(),
):
    validator_addr, feeder_addr = cli_accounts
    h1 = 76777
    p1 = {
        "height": f"{h1}",
        "result": {
            "type": "core/Account",
            "value": {
                "address": f"{feeder_addr}",
                "coins": [{
                    "denom": "uluna",
                    "amount": "300000000",
                }],
                "public_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "A0DrlsGKykR3p5gtNElez5qpeuHwhuRfDaeOEj4TDkfT",
                },
                "account_number": "52",
                "sequence": "2502",
            }
        }
    }
    # url_qs = urlencode({})
    url = f"{node_addr}/auth/accounts/{feeder_addr}"
    # call wallet.sync_status #1
    m.get(url, status=200, payload=p1)
    # call wallet.sync_status #2
    m.get(url, status=200, payload=p1)
    
    # call get active denominations
    # all denominations are against uluna
    p2 = {
        "height": f"{h1}", "result": [
            "ukrw",
            "umnt",
            "usdr",
            "uusd",
        ],
    }
    url = f"{node_addr}/oracle/denoms/actives"
    m.get(url, status=200, payload=p2)

    p3 = {
        "height": f"{h1}", "result": [{
            "denom": "ukrw",
            "amount": "314.875000000000000000"
        }, {
          "denom": "umnt",
          "amount": "725.237798765437332804"
        }, {
          "denom": "usdr",
          "amount": "0.194791705799000000"
        }, {
          "denom": "uusd",
          "amount": "0.266655379666469144"
        }],
    }
    url = f"{node_addr}/oracle/denoms/exchange_rates"
    m.get(url, status=200, payload=p3)

    p4 = {
        "height": f"{h1}", "result": [],
    }
    url = f"{node_addr}/oracle/denoms/ukrw/prevotes/{validator_addr}"
    m.get(url, status=200, payload=p4)

    p5 = {
        "height": f"{h1}", "result": [{
            "exchange_rate": "314.410000000000000000",
            "denom": "ukrw",
            "voter": f"{feeder_addr}"
        }],
    }
    url = f"{node_addr}/oracle/denoms/ukrw/votes/{validator_addr}"
    m.get(url, status=200, payload=p5)

    p6 = {
        "errorCode": "0",
        "currency": " luna",
        "result": "success",
        "ask": [
            {"price": "316.0", "qty": "445.1199"},
            {"price": "317.0", "qty": "182.7279"},
            {"price": "318.0", "qty": "2377.9791"},
            {"price": "319.0", "qty": "147.2411"},
        ],
        "bid": [
            {"price": "314.0", "qty": "190.3975"},
            {"price": "313.0", "qty": "898.9228"},
            {"price": "312.0", "qty": "10595.197"},
            {"price": "311.0", "qty": "980.0"},
        ],
        "timestamp": "1575003770",
    }
    url_params = urlencode({"currency": "LUNA", "format": "json"})
    url = f"https://api.coinone.co.kr/orderbook/?{url_params}"
    m.get(url, status=200, payload=p6)


def voting_e2e_3_periods(
    m,
    node_addr,
    cli_accounts,
):
    # feeder_addr = cli_accounts[1]
    # Mock the Initial Wallet Sync State Call
    vp_0_mock_account(m, node_addr, cli_accounts)
