from urllib.parse import urlencode
from functools import partial
from aioresponses import CallbackResult
import simplejson as json


def mock_account_info(
  m,
  node_addr,
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
    url = f"{node_addr}/auth/accounts/{feeder_addr}"
    m.get(url, status=200, payload=template)


def mock_block_data(
    m,
    node_addr,
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
    url = f"{node_addr}/blocks/latest"
    m.get(url, status=200, payload=template)


def mock_active_denoms(
    m,
    node_addr,
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
    url = f"{node_addr}/oracle/denoms/actives"
    m.get(url, status=200, payload=payload)


def mock_onchain_rates(
    m,
    node_addr,
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
    url = f"{node_addr}/oracle/denoms/exchange_rates"
    m.get(url, status=200, payload=payload)


def mock_chain_prevotes(
    m,
    node_addr,
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
    url = f"{node_addr}/oracle/denoms/{denom}/prevotes/{validator_addr}"
    m.get(url, status=200, payload=payload)


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


def mock_broadcast_tx(
    m,
    node_addr,
    txhash,
    post_data=dict(),
    logs=list(),
):

    def process_post_req(txhash, post_data, logs, *args, **kwargs):
        raw_post_data = kwargs["data"]
        recv_post_data = json.loads(raw_post_data)
        # print("RECV")
        # print(recv_post_data)
        # print("POST")
        # print(post_data)
        assert recv_post_data == post_data
        payload = {
            "height": "0",
            "txhash": f"{txhash}",
            "logs": logs,
        }
        return CallbackResult(
            status=200,
            payload=payload,
        )
    processor = partial(process_post_req, txhash, post_data, logs)
    url = f"{node_addr}/txs"
    m.post(url, callback=processor)


def mock_query_tx(
    m,
    node_addr,
    height,
    txhash,
    logs=list(),
):
    payload = {
        "height": f"{height}",
        "txhash": f"{txhash}",
        "logs": logs,
    }

    url = f"{node_addr}/txs/{txhash}"
    m.get(url, payload=payload)
