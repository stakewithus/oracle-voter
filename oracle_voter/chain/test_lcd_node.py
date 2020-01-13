from oracle_voter import _version
import asyncio
import pytest
from unittest.mock import Mock, patch
from oracle_voter.common.util import (
    async_stubber,
    async_raiser,
    not_found
)


@patch('oracle_voter.common.client.http_get')
def test_get_tx(http_mock, lcd_node):
    http_mock.return_value = async_stubber("")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        lcd_node.get_tx(
            "36F6ABBE0A686D4DAC5F557EE562B421D7C47AB6DE77B986AA6D925E41645AFA")
    )
    http_mock.assert_called_once_with(
        "http://127.0.0.1:1317/txs/36F6ABBE0A686D4DAC5F557EE562B421D7C47AB6DE77B986AA6D925E41645AFA", params={})


@patch('oracle_voter.common.client.http_post')
def test_broadcast_tx_async(http_mock, lcd_node):
    http_mock.return_value = async_stubber("")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        lcd_node.broadcast_tx_async(
            "36F6ABBE0A686D4DAC5F557EE562B421D7C47AB6DE77B986AA6D925E41645AFA")
    )
    http_mock.assert_called_once_with(
        "http://127.0.0.1:1317/txs",
        params={},
        post_data='36F6ABBE0A686D4DAC5F557EE562B421D7C47AB6DE77B986AA6D925E41645AFA'
    )


@patch('oracle_voter.common.client.http_get')
def test_get_latest_block(http_mock, lcd_node):
    http_mock.return_value = async_stubber("")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        lcd_node.get_latest_block()
    )
    http_mock.assert_called_once_with(
        "http://127.0.0.1:1317/blocks/latest", params={})


@patch('oracle_voter.common.client.http_get')
def test_get_account(http_mock, lcd_node):
    http_mock.return_value = async_stubber("")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        lcd_node.get_account("terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm")
    )
    http_mock.assert_called_once_with(
        "http://127.0.0.1:1317/auth/accounts/terra1tngw4yusyas9ujlcmxdn7xkx6az07hej72rssm", params={})


@patch('oracle_voter.common.client.http_get')
def test_get_oracle_rates(http_mock, lcd_node):
    http_mock.return_value = async_stubber("")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        lcd_node.get_oracle_rates()
    )
    http_mock.assert_called_once_with(
        "http://127.0.0.1:1317/oracle/denoms/exchange_rates", params={})


@patch('oracle_voter.common.client.http_get')
def test_get_oracle_active_denoms(http_mock, lcd_node):
    http_mock.return_value = async_stubber("")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        lcd_node.get_oracle_active_denoms()
    )
    http_mock.assert_called_once_with(
        "http://127.0.0.1:1317/oracle/denoms/actives", params={})


@patch('oracle_voter.common.client.http_get')
def test_get_oracle_prevotes_validator(http_mock, lcd_node):
    http_mock.return_value = async_stubber("")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        lcd_node.get_oracle_prevotes_validator(
            "mnt", "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu")
    )
    http_mock.assert_called_once_with(
        "http://127.0.0.1:1317/oracle/denoms/mnt/prevotes/terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu", params={})


@patch('oracle_voter.common.client.http_get')
def test_get_oracle_votes_validator(http_mock, lcd_node):
    http_mock.return_value = async_stubber("")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        lcd_node.get_oracle_votes_validator(
            "mnt", "terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu")
    )
    http_mock.assert_called_once_with(
        "http://127.0.0.1:1317/oracle/denoms/mnt/votes/terravaloper1lsgzqmtyl99cxjs2rdrwvda3g6g6z8d3g8tfzu", params={})
