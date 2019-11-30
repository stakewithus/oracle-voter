

def vp_0_mock_account(
    m,
    node_addr="",
    feeder_addr="",
):
    payload = {
        "height": "76777",
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
    url = f"http://{node_addr}/auth/accounts/{feeder_addr}"
    m.get(url, status=200, payload=payload)


def voting_e2e_3_periods(
    m,
    node_addr,
    cli_accounts,
):
    feeder_addr = cli_accounts[1]
    # Mock the Initial Wallet Sync State Call
    vp_0_mock_account(m, node_addr, feeder_addr)
