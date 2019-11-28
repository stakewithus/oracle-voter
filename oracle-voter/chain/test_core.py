from decimal import Decimal


def test_build_vote_tx(tx_builder):
    txb = tx_builder("soju-0012", 45, 0)

    txb.append_votemsg(
        exchange_rate=Decimal("8000.0"),
        denom="ukrw",
        feeder="terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
        validator="terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
        salt="1234",
    )
    result = txb.build_incomplete()

    expected = {
        "chain_id": "soju-0012",
        "account_number": "45",
        "sequence": "0",
        "fee": {"amount": [], "gas": "200000"},
        "msgs": [{
            "type": r"oracle/MsgExchangeRateVote",
            "value": {
                "exchange_rate": "8000.000000000000000000",
                "salt": "1234",
                "denom": "ukrw",
                "feeder": "terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
                "validator": "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
            },
        }],
        "memo": "",
    }
    assert result == expected


def test_fully_build_vote_tx(tx_builder, feeder_wallet):
    txb = tx_builder("soju-0012", 45, 0)
    txb.append_votemsg(
        exchange_rate=Decimal("8000.0"),
        denom="ukrw",
        feeder="terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
        validator="terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
        salt="1234",
    )

    result = txb.build()

    expected = {
        "type": "core/StdTx",
        "value": {
            "msg": [{
                "type": "oracle/MsgExchangeRateVote",
                "value": {
                    "exchange_rate": "8000.000000000000000000",
                    "salt": "1234",
                    "denom": "ukrw",
                    "feeder": "terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
                    "validator": "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
                },
            }],
            "fee": {"amount": [], "gas": "200000"},
            "memo": "",
            "signatures": [],
        },
    }

    assert result == expected


def test_sign_built_vote_tx(tx_builder, feeder_wallet):
    txb = tx_builder("soju-0012", 45, 0)
    txb.append_votemsg(
        exchange_rate=Decimal("8000.0"),
        denom="ukrw",
        feeder="terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
        validator="terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
        salt="1234",
    )

    result = txb.sign(feeder_wallet)

    expected = {
        "type": "core/StdTx",
        "value": {
            "msg": [{
                "type": "oracle/MsgExchangeRateVote",
                "value": {
                    "exchange_rate": "8000.000000000000000000",
                    "salt": "1234",
                    "denom": "ukrw",
                    "feeder": "terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
                    "validator": "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
                },
            }],
            "memo": "",
            "fee": {"amount": [], "gas": "200000"},
            "signatures": [{
                "pub_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AsyXH0ftWQ29WxzgwpfV2WJ7glylgPnaOPdcAfPQ+Fyk"
                },
                "signature": "SfNv0+GCQTw48YPZLrFVeCp4mdF0G5SwL6M9Rqzp4IZQE8JKqulN8cEIplFGhGeEGodgaZxIseLRxC6OUScNPw=="
            }],
        },
    }

    assert result == expected
