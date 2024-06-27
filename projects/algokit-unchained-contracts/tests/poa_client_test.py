import algokit_utils
import algosdk
import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.poa.client import (
    ProofOfAttendanceClient,
)


@pytest.fixture(scope="session")
def poa_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> ProofOfAttendanceClient:
    config.configure(
        debug=False,
        # trace_all=True,
    )

    client = ProofOfAttendanceClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )

    algokit_utils.ensure_funded(
        algod_client,
        algokit_utils.EnsureBalanceParameters(
            account_to_fund=client.app_address,
            min_spending_balance_micro_algos=10_000_000,
            min_funding_increment_micro_algos=10_000_000,
        ),
    )

    return client


def test_confirm_attendance(poa_client: ProofOfAttendanceClient) -> None:

    sp = poa_client.algod_client.suggested_params()
    sp.fee = 1000
    creator = get_localnet_default_account(poa_client.algod_client)
    response = poa_client.confirm_attendance(
        transaction_parameters=algokit_utils.TransactionParameters(
            suggested_params=sp,
            boxes=[
                (
                    poa_client.app_id,
                    algosdk.encoding.decode_address(creator.address),  # type: ignore
                )
            ],
        ),
    )

    assert response
