from decimal import Decimal, Context


def test_build_vote_tx(tx_builder, account_addrs, wei_value):
    feeder, validator = account_addrs

    txb = tx_builder("soju-0012", 45, 0)

    txb.append_votemsg(
        exchange_rate=Decimal("8000.0").quantize(
            wei_value,
            context=Context(prec=30),
        ),
        denom="ukrw",
        feeder=f"{feeder}",
        validator=f"{validator}",
        salt="1234",
    )
    result = txb.build_incomplete()

    expected = {
        "chain_id": "soju-0012",
        "account_number": "45",
        "sequence": "0",
        "fee": {
            "amount": [{
                "denom": "uluna",
                "amount": "1000",
            }],
            "gas": "200000",
        },
        "msgs": [{
            "type": r"oracle/MsgExchangeRateVote",
            "value": {
                "exchange_rate": "8000.000000000000000000",
                "salt": "1234",
                "denom": "ukrw",
                "feeder": f"{feeder}",
                "validator": f"{validator}",
            },
        }],
        "memo": "",
    }
    assert result == expected


def test_fully_build_vote_tx(
    tx_builder,
    feeder_wallet,
    account_addrs,
    wei_value,
):
    feeder, validator = account_addrs

    txb = tx_builder("soju-0012", 45, 0)
    txb.append_votemsg(
        exchange_rate=Decimal("8000.0").quantize(
            wei_value,
            context=Context(prec=30),
        ),
        denom="ukrw",
        feeder=f"{feeder}",
        validator=f"{validator}",
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
                    "feeder": f"{feeder}",
                    "validator": f"{validator}",
                },
            }],
            "fee": {
                "amount": [{
                    "denom": "uluna",
                    "amount": "1000",
                }],
                "gas": "200000",
            },
            "memo": "",
            "signatures": [],
        },
    }

    assert result == expected


def test_sign_built_vote_tx(
    tx_builder,
    feeder_wallet,
    account_addrs,
    wei_value,
):
    feeder, validator = account_addrs

    txb = tx_builder("soju-0012", 45, 0)
    txb.append_votemsg(
        exchange_rate=Decimal("8000.0").quantize(
            wei_value,
            context=Context(prec=30),
        ),
        denom="ukrw",
        feeder=f"{feeder}",
        validator=f"{validator}",
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
                    "feeder": f"{feeder}",
                    "validator": f"{validator}",
                },
            }],
            "memo": "",
            "fee": {
                "amount": [{
                    "denom": "uluna",
                    "amount": "1000",
                }],
                "gas": "200000",
            },
            "signatures": [{
                "pub_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AsyXH0ftWQ29WxzgwpfV2WJ7glylgPnaOPdcAfPQ+Fyk"
                },
                "signature": "ZOI24iYEoW4GmMCIaFvoCjSoBO1fZyuryaOwjaNavzYAjK9ebgs1PLkD6hhlZ7umIRCvLhNTZkspoEwKM1w/UQ=="
            }],
        },
    }

    assert result == expected
