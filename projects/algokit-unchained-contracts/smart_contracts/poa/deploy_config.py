import logging

import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    from smart_contracts.artifacts.poa.client import (
        ProofOfAttendanceClient,
    )

    app_client = ProofOfAttendanceClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )

    response = app_client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )  # Second bug

    print(response.app.app_id)

    # algokit_utils.ensure_funded(
    #     algod_client,
    #     algokit_utils.EnsureBalanceParameters(
    #         account_to_fund=app_client.app_address,
    #         min_spending_balance_micro_algos=10_000_000,
    #         min_funding_increment_micro_algos=10_000_000,
    #     ),
    # )

    # sp = algod_client.suggested_params()
    # sp.fee = 1000
    # response = app_client.confirm_attendance(
    #     transaction_parameters=algokit_utils.TransactionParameters(
    #         suggested_params=sp,
    #         boxes=[
    #             (
    #                 app_client.app_id,
    #                 algosdk.encoding.decode_address(deployer.address),  # type: ignore
    #             )
    #         ],
    #     )
    # )
    # print(response)

    # poa_id: int = (
    #     (
    #         app_client.compose()
    #         .get_poa_id(
    #             transaction_parameters=algokit_utils.TransactionParameters(
    #                 boxes=[
    #                     (
    #                         app_client.app_id,
    #                         algosdk.encoding.decode_address(deployer.address),  # type: ignore
    #                     )
    #                 ],
    #             )
    #         )
    #         .simulate()
    #     )
    #     .abi_results[0]
    #     .return_value
    # )

    # sp2 = algod_client.suggested_params()
    # sp2.fee = 0
    # sp2.flat_fee = True
    # response2 = app_client.claim_poa(
    #     opt_in_txn=TransactionWithSigner(
    #         algosdk.transaction.AssetTransferTxn(  # type: ignore
    #             sender=deployer.address,
    #             receiver=deployer.address,
    #             index=poa_id,
    #             amt=0,
    #             sp=sp2,
    #         ),
    #         signer=deployer.signer,
    #     ),  # type: ignore
    #     transaction_parameters=algokit_utils.TransactionParameters(
    #         suggested_params=sp,
    #         boxes=[
    #             (
    #                 app_client.app_id,
    #                 algosdk.encoding.decode_address(deployer.address),  # type: ignore
    #             )
    #         ],
    #         foreign_assets=[poa_id],
    #         signer=deployer.signer,
    #     ),
    # )

    # print(response2)
