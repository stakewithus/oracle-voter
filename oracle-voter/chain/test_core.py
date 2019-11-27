from decimal import Decimal


def test_build_vote_tx(tx_builder):
    txb = tx_builder(
        "soju-0012",
        45
    )

    txb.append_votemsg(
        exchange_rate=Decimal("8000.0"),
        demon="ukrw",
        feeder="terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
        validator="terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
        salt="1234",
    )
    result = txb.export()

    expected = {
        "chain_id": "soju-0012",
        "account_number": "45",
        "fee": {"amount": [], "gas": "200000"},
        "msgs": [{
            "type": "oracle/MsgExchangeRateVote",
            "value": {
                "exchange_rate": "8000.000000000000000000",
                "salt": "1234",
                "demon": "ukrw",
                "feeder": "terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
                "validator": "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
            },
        }],
        "memo": "",
    }
    assert result == expected


def test_build_and_sign_vote_tx(tx_builder, feeder_wallet):
    txb = tx_builder(
        "soju-0012",
        45
    )

    txb.append_votemsg(
        exchange_rate=Decimal("8000.0"),
        demon="ukrw",
        feeder="terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
        validator="terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
        salt="1234",
    )

    txb.sign(feeder_wallet)

    result = txb.export()

    expected = {
        "chain_id": "soju-0012",
        "account_number": "45",
        "fee": {"amount": [], "gas": "200000"},
        "msgs": [{
            "type": "oracle/MsgExchangeRateVote",
            "value": {
                "exchange_rate": "8000.000000000000000000",
                "salt": "1234",
                "demon": "ukrw",
                "feeder": "terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm",
                "validator": "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu",
            },
        }],
        "signatures": [{
            "pub_key": {
                "type": "tendermint/PubKeySecp256k1",
                "value": "AsyXH0ftWQ29WxzgwpfV2WJ7glylgPnaOPdcAfPQ+Fyk"
            },
            "signature": "SfNv0+GCQTw48YPZLrFVeCp4mdF0G5SwL6M9Rqzp4IZQE8JKqulN8cEIplFGhGeEGodgaZxIseLRxC6OUScNPw=="
        }],
        "memo": "",
    }
    assert result == expected
