import pandas as pd
import re


code = """
AAVE: POOL_ADDRESSES_PROVIDER = IPoolAddressesProvider(0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e);
AAVE: POOL = IPool(0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2);
AAVE: POOL_IMPL = 0x5FAab9E1adbddaD0a08734BE8a52185Fd6558E14;
AAVE: POOL_CONFIGURATOR = IPoolConfigurator(0x64b761D848206f447Fe2dd461b0c635Ec39EbB27);
AAVE: POOL_CONFIGURATOR_IMPL = 0xFDA7ffA872bDc906D43079EA134ebC9a511db0c2;
AAVE: ORACLE = IAaveOracle(0x54586bE62E3c3580375aE3723C145253060Ca0C2);
AAVE: PROTOCOL_DATA_PROVIDER = IPoolDataProvider(0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3);
AAVE: ACL_MANAGER = IACLManager(0xc2aaCf6553D20d1e9d78E365AAba8032af9c85b0);
AAVE: ACL_ADMIN = 0x5300A1a15135EA4dc7aD5a167152C01EFc9b192A;
AAVE: COLLECTOR = ICollector(0x464C71f6c2F760DdA6093dCB91C24c39e5d6e18c);
AAVE: DEFAULT_INCENTIVES_CONTROLLER = 0x8164Cc65827dcFe994AB23944CBC90e0aa80bFcb;
AAVE: DEFAULT_A_TOKEN_IMPL_REV_1 = 0x7EfFD7b47Bfd17e52fB7559d3f924201b9DbfF3d;
AAVE: DEFAULT_VARIABLE_DEBT_TOKEN_IMPL_REV_1 = 0xaC725CB59D16C81061BDeA61041a8A5e73DA9EC6;
AAVE: DEFAULT_STABLE_DEBT_TOKEN_IMPL_REV_1 = 0x15C5620dfFaC7c7366EED66C20Ad222DDbB1eD57;
AAVE: EMISSION_MANAGER = 0x223d844fc4B006D67c0cDbd39371A9F73f69d974;
AAVE: CAPS_PLUS_RISK_STEWARD = 0x82dcCF206Ae2Ab46E2099e663F70DeE77caE7778;
AAVE: FREEZING_STEWARD = 0x2eE68ACb6A1319de1b49DC139894644E424fefD6;
AAVE: DEBT_SWAP_ADAPTER = 0x8761e0370f94f68Db8EaA731f4fC581f6AD0Bd68;
AAVE: DELEGATION_AWARE_A_TOKEN_IMPL_REV_1 = 0x21714092D90c7265F52fdfDae068EC11a23C6248;
AAVE: CONFIG_ENGINE = 0xA3e44d830440dF5098520F62Ebec285B1198c51E;
AAVE: POOL_ADDRESSES_PROVIDER_REGISTRY = 0xbaA999AC55EAce41CcAE355c77809e68Bb345170;
AAVE: RATES_FACTORY = 0xcC47c4Fe1F7f29ff31A8b62197023aC8553C7896;
AAVE: REPAY_WITH_COLLATERAL_ADAPTER = 0x02e7B8511831B1b02d9018215a0f8f500Ea5c6B3;
AAVE: STATIC_A_TOKEN_FACTORY = 0x411D79b8cC43384FDE66CaBf9b6a17180c842511;
AAVE: SWAP_COLLATERAL_ADAPTER = 0xADC0A53095A0af87F3aa29FE0715B5c28016364e;
AAVE: UI_GHO_DATA_PROVIDER = 0x379c1EDD1A41218bdbFf960a9d5AD2818Bf61aE8;
AAVE: UI_INCENTIVE_DATA_PROVIDER = 0x162A7AC02f547ad796CA549f757e2b8d1D9b10a6;
AAVE: UI_POOL_DATA_PROVIDER = 0x91c0eA31b49B69Ea18607702c5d9aC360bf3dE7d;
AAVE: WALLET_BALANCE_PROVIDER = 0xC7be5307ba715ce89b152f3Df0658295b3dbA8E2;
AAVE: WETH_GATEWAY = 0x893411580e590D62dDBca8a703d61Cc4A8c7b2b9;
AAVE: WITHDRAW_SWAP_ADAPTER = 0x78F8Bd884C3D738B74B420540659c82f392820e0;
AAVE: SAVINGS_DAI_TOKEN_WRAPPER = 0xE28E2c8d240dd5eBd0adcab86fbD79df7a052034;
AAVE: WRAPPED_TOKEN_GATEWAY = 0xD322A49006FC828F9B5B37Ab215F99B4E5caB19C;
COMPOUND: POOL = 0xA17581A9E3356d9A858b789D68B4d866e593aE94;
PRISMA: POOL = 0xed8B26D99834540C5013701bB3715faFD39993Ba;
"""

# Split the string into lines
lines = code.split("\n")

known_addresses = {}
for line in lines:
    # Splitting the line into variable name and the rest
    parts = line.split("=")
    if len(parts) == 2:
        variable_name = parts[0].strip()
        # Extracting the Ethereum address
        ethereum_address = re.search(r"0x[a-fA-F0-9]{40}", parts[1])
        if ethereum_address:
            known_addresses[ethereum_address.group()] = variable_name


def generate_network(transaction_df: pd.DataFrame):
    # Create json dict from transaction df

    transaction_df = transaction_df.copy()
    # Filter out transactions with diminishingly small amounts
    transaction_df = transaction_df[transaction_df["Amount"] > 1e-10]

    nodes = set()
    edges = []

    # Iterate rows of df
    for idx, row in transaction_df.iterrows():
        # Drop NaN values from current transaction
        transaction_data = row.dropna().to_dict()

        if row["Event Type"] == "Withdraw(Prisma)":
            transaction_data["Event Type"] = "Withdraw"
            # Store nodes
            user = (
                (known_addresses[row["User"]])
                if row["User"] in known_addresses
                else row["User"]
            )
            address = (
                (known_addresses[row["Address"]])
                if row["Address"] in known_addresses
                else row["Address"]
            )
            nodes.add(user)
            nodes.add(address)

            # Store edge
            edge_data = {
                "source": address,
                "target": user,
                "weight": float(row["Amount"]),
            }
            edge_data.update(transaction_data)
            edges.append(edge_data)

        elif row["Event Type"] == "Withdraw":
            if row["User"] != row["To"]:
                # Store nodes
                address = (
                    (known_addresses[row["Address"]])
                    if row["Address"] in known_addresses
                    else row["Address"]
                )
                user = (
                    (known_addresses[row["User"]])
                    if row["User"] in known_addresses
                    else row["User"]
                )
                to = (
                    (known_addresses[row["To"]])
                    if row["To"] in known_addresses
                    else row["To"]
                )
                nodes.add(user)
                nodes.add(address)
                nodes.add(to)

                # Store edges
                # Address -> User
                edge1_data = {
                    "source": address,
                    "target": user,
                    "weight": float(row["Amount"]),
                }
                edge1_data.update(transaction_data)
                edges.append(edge1_data)

                # User -> To
                edge2_data = {
                    "source": user,
                    "target": to,
                    "weight": float(row["Amount"]),
                }
                edge2_data.update(transaction_data)
                edges.append(edge2_data)

            else:
                # Store nodes
                user = (
                    (known_addresses[row["User"]])
                    if row["User"] in known_addresses
                    else row["User"]
                )
                address = (
                    (known_addresses[row["Address"]])
                    if row["Address"] in known_addresses
                    else row["Address"]
                )
                nodes.add(user)
                nodes.add(address)

                # Store edge
                edge_data = {
                    "source": address,
                    "target": user,
                    "weight": float(row["Amount"]),
                }
                edge_data.update(transaction_data)
                edges.append(edge_data)

        elif row["Event Type"] == "Supply":
            # Store nodes
            user = (
                (known_addresses[row["User"]])
                if row["User"] in known_addresses
                else row["User"]
            )
            address = (
                (known_addresses[row["Address"]])
                if row["Address"] in known_addresses
                else row["Address"]
            )
            nodes.add(user)
            nodes.add(address)

            # Store edge
            edge_data = {
                "source": user,
                "target": address,
                "weight": float(row["Amount"]),
            }
            edge_data.update(transaction_data)
            edges.append(edge_data)

        elif row["Event Type"] == "Borrow":
            if row["User"] != row["On Behalf Of"]:
                # Store nodes
                user = (
                    (known_addresses[row["User"]])
                    if row["User"] in known_addresses
                    else row["User"]
                )
                address = (
                    (known_addresses[row["Address"]])
                    if row["Address"] in known_addresses
                    else row["Address"]
                )
                onBehalfOf = (
                    (known_addresses[row["On Behalf Of"]])
                    if row["On Behalf Of"] in known_addresses
                    else row["On Behalf Of"]
                )
                nodes.add(user)
                nodes.add(address)
                nodes.add(onBehalfOf)

                # Store edges
                # Address -> User
                edge1_data = {
                    "source": address,
                    "target": user,
                    "weight": float(row["Amount"]),
                }
                edge1_data.update(transaction_data)
                edges.append(edge1_data)

                # User -> On Behalf Of
                edge2_data = {
                    "source": user,
                    "target": onBehalfOf,
                    "weight": float(row["Amount"]),
                }
                edge2_data.update(transaction_data)
                edges.append(edge2_data)

            else:
                # Store nodes
                user = (
                    (known_addresses[row["User"]])
                    if row["User"] in known_addresses
                    else row["User"]
                )
                address = (
                    (known_addresses[row["Address"]])
                    if row["Address"] in known_addresses
                    else row["Address"]
                )
                nodes.add(user)
                nodes.add(address)

                # Store edge
                edge_data = {
                    "source": address,
                    "target": user,
                    "weight": float(row["Amount"]),
                }
                edge_data.update(transaction_data)
                edges.append(edge_data)

        elif row["Event Type"] == "Repay":
            if row["User"] != row["Repayer"]:
                # Store nodes
                user = (
                    (known_addresses[row["User"]])
                    if row["User"] in known_addresses
                    else row["User"]
                )
                address = (
                    (known_addresses[row["Address"]])
                    if row["Address"] in known_addresses
                    else row["Address"]
                )
                repayer = (
                    (known_addresses[row["Repayer"]])
                    if row["Repayer"] in known_addresses
                    else row["Repayer"]
                )
                nodes.add(user)
                nodes.add(address)
                nodes.add(repayer)

                # Store edges
                # User -> Repayer
                edge1_data = {
                    "source": user,
                    "target": repayer,
                    "weight": float(row["Amount"]),
                }
                edge1_data.update(transaction_data)
                edges.append(edge1_data)

                # Repayer -> Address
                edge2_data = {
                    "source": repayer,
                    "target": address,
                    "weight": float(row["Amount"]),
                }
                edge2_data.update(transaction_data)
                edges.append(edge2_data)

            else:
                # Store nodes
                user = (
                    (known_addresses[row["User"]])
                    if row["User"] in known_addresses
                    else row["User"]
                )
                address = (
                    (known_addresses[row["Address"]])
                    if row["Address"] in known_addresses
                    else row["Address"]
                )
                nodes.add(user)
                nodes.add(address)

                # Store edge
                edge_data = {
                    "source": address,
                    "target": user,
                    "weight": float(row["Amount"]),
                }
                edge_data.update(transaction_data)
                edges.append(edge_data)

        elif row["Event Type"] == "Flashloan":
            # Store nodes
            address = (
                (known_addresses[row["Address"]])
                if row["Address"] in known_addresses
                else row["Address"]
            )
            initiator = (
                (known_addresses[row["Initiator"]])
                if row["Initiator"] in known_addresses
                else row["Initiator"]
            )
            target = (
                (known_addresses[row["Target"]])
                if row["Target"] in known_addresses
                else row["Target"]
            )
            nodes.add(address)
            nodes.add(initiator)
            nodes.add(target)

            # Store edges
            # Address -> Initiator
            edge1_data = {
                "source": address,
                "target": initiator,
                "weight": float(row["Amount"]),
            }
            edge1_data.update(transaction_data)
            edges.append(edge1_data)

            # Initiator -> Target
            edge2_data = {
                "source": initiator,
                "target": target,
                "weight": float(row["Amount"]),
            }
            edge2_data.update(transaction_data)
            edges.append(edge2_data)

        elif row["Event Type"] == "SupplyCollateral":
            # Store nodes
            user = (
                (known_addresses[row["User"]])
                if row["User"] in known_addresses
                else row["User"]
            )
            address = (
                (known_addresses[row["Address"]])
                if row["Address"] in known_addresses
                else row["Address"]
            )
            nodes.add(user)
            nodes.add(address)

            # Store edge
            edge_data = {
                "source": user,
                "target": address,
                "weight": float(row["Amount"]),
            }
            edge_data.update(transaction_data)
            edges.append(edge_data)

        elif row["Event Type"] == "Provide":
            # Store nodes
            user = (
                (known_addresses[row["User"]])
                if row["User"] in known_addresses
                else row["User"]
            )
            address = (
                (known_addresses[row["Address"]])
                if row["Address"] in known_addresses
                else row["Address"]
            )
            nodes.add(user)
            nodes.add(address)

            # Store edge
            edge_data = {
                "source": user,
                "target": address,
                "weight": float(row["Amount"]),
            }
            edge_data.update(transaction_data)
            edges.append(edge_data)

    nodes_list = [{"id": node} for node in nodes]
    graph_data = {"nodes": nodes_list, "edges": edges}

    return graph_data
