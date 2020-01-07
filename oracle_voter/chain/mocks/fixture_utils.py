import asyncio
from unittest.mock import MagicMock
from urllib.parse import urlencode


def async_stubber(res):
    f = asyncio.Future()
    f.set_result(res)
    return f

def mock_account_info(
    feeder_addr,
    public_key,
    account_num,
    height,
    account_seq,
):
    template = {
        "height": f"{height}",
        "result": {
            "type": "core/Account",
            "value": {
                "address": f"{feeder_addr}",
                "coins": [{
                    "denom": "uluna",
                    "amount": "100000000",
                }],
                "public_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": f"{public_key}",
                },
                "account_number": f"{account_num}",
                "sequence": f"{account_seq}",
            }
        }
    }
    return template


def mock_block_data(
    height,
    current_hash,
    prev_hash,
    chain_id="soju-0013",
):
    template = {
        "block_meta": {
            "block_id": {
                "hash": f"{current_hash}",
                "parts": {
                    "total": "1",
                    "hash": "xxx",
                }
            },
            "header": {
                "version": {"block": "10", "app": "0"},
                "chain_id": "f{chain_id}",
                "height": f"{height}",
                "time": "2019-12-05T10:24:23.453048756Z",
                "num_txs": "1",
                "total_txs": "47517",
                "last_block_id": {
                    "hash": f"{prev_hash}",
                    "parts": {
                        "total": "1",
                        "hash": "xxx",
                    },
                },
            },
        },
    }
    return template


def mock_active_denoms(
    height,
):
    payload = {
        "height": f"{height}", "result": [
            "ukrw",
            "umnt",
            "usdr",
            "uusd",
        ],
    }
    return payload


def mock_onchain_rates(
    height,
    ukrw="",
    umnt="",
    usdr="",
    uusd="",
):
    payload = {
        "height": f"{height}",
        "result": [{
            "denom": "ukrw",
            "amount": f"{ukrw}"
        }, {
            "denom": "umnt",
            "amount": f"{umnt}"
        }, {
            "denom": "usdr",
            "amount": f"{usdr}"
        }, {
            "denom": "uusd",
            "amount": f"{uusd}"
        }],
    }
    return payload


def mock_chain_prevotes(
    validator_addr,
    height,
    denom,
    submit_height=0,
    submit_hash="",
):
    payload_result = []
    if submit_hash != "":
        payload_result = [{
            "hash": f"{submit_hash}",
            "denom": f"{denom}",
            "voter": f"{validator_addr}",
            "submit_block": f"{submit_height}",
        }]

    payload = {
        "height": f"{height}",
        "result": payload_result,
    }
    return payload


def mock_broadcast_tx(txhash):
    return {
        "height": "0",
        "txhash": f"{txhash}",
        "logs": [{
            "msg_index": 0,
            "success": True,
            "log": "",
        }, {
            "msg_index": 1,
            "success": True,
            "log": "",
        }, {
            "msg_index": 2,
            "success": True,
            "log": "",
        }, {
            "msg_index": 3,
            "success": True,
            "log": "",
        }],
    }


def mock_query_tx(height, txhash):
    logs = [{
        "msg_index": 0,
        "success": True,
        "log": "",
    }, {
        "msg_index": 1,
        "success": True,
        "log": "",
    }, {
        "msg_index": 2,
        "success": True,
        "log": "",
    }, {
        "msg_index": 3,
        "success": True,
        "log": "",
    }]
    return {
        "height": f"{height}",
        "txhash": f"{txhash}",
        "logs": logs,
    }


def mock_feed_coinone_orderbook(
    m,
    feed_url,
    currency,
    asks=dict(),
    bids=dict(),
):
    payload = {
        "errorCode": "0",
        "currency": " luna",
        "result": "success",
        "ask": asks,
        "bid": bids,
        "timestamp": "1575003770",
    }

    url_params = urlencode({"currency": currency, "format": "json"})
    url = f"{feed_url}/orderbook/?{url_params}"
    m.get(url, status=200, payload=payload)


def mock_feed_ukfx_px(
    m,
    feed_url,
    currency,
    payload
):

    url_params = urlencode({"t": 1})
    url = f"{feed_url}/pairs/krw/{currency}/livehistory/chart?{url_params}"
    m.get(url, status=200, payload=payload)
