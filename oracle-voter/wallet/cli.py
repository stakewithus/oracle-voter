import subprocess
import os
import simplejson as json
from decimal import Decimal, Context


MICRO_VALUE = Decimal("10.0") ** 6
MICRO_UNIT = Decimal("10.0") ** -6


class CLIWallet:
    account_addr = None
    account_num = 0
    account_seq = 0

    def __init__(
        self,
        name,
        password,
        account_addr,
        home=None,
        lcd_node={},
        gas_prices="0.1uluna",
        home_dir=None,
    ):
        self.name = name
        self.password = password
        self.home = home
        self.lcd_node = lcd_node
        # Get the account address
        # self.get_addr()
        self.account_addr = account_addr
        self.gas_prices = gas_prices
        # If no home directory is given, default to terracli default
        self.home_dir = home_dir or os.path.expanduser("~/.terracli")
        self.account_balance = Decimal("0.0")

    """
    @staticmethod
    def get_addr(name):
        result = subprocess.check_output((
            "terracli",
            "keys",
            "show",
            f"{name}",
            "-a",
            "--home",
            f"{self.home_dir}"
        ))
        account_addr = str(result, "utf-8").strip()
        return account_addr
    """

    async def sync_state(self):
        account_raw = await self.lcd_node.get_account(self.account_addr)
        self.account_num = account_raw["result"]["value"]["account_number"]
        if int(self.account_num) <= 0:
            raise ValueError(
                f"Account Number is not more than 0 for wallet {self.name}"
            )
        new_seq = int(account_raw["result"]["value"]["sequence"])
        raw_balances = account_raw["result"]["value"]["coins"]
        raw_balance = Decimal("0.0")
        for bal in raw_balances:
            denom = bal["denom"]
            amt = bal["amount"]
            if denom == "uluna":
                raw_balance = Decimal(amt)

        balance = Decimal(raw_balance / MICRO_VALUE).quantize(
            MICRO_UNIT,
            context=Context(prec=40),
        )
        if new_seq > self.account_seq:
            self.account_seq = new_seq

        self.account_balance = balance
        """ Print Summary """
        print(f"""Account: {self.name}
Balance: {self.account_balance}
Number: {self.account_num}
Sequence: {self.account_seq}
""")

    def offline_sign(
        self,
        payload,
        chain_id="-1",
        account_number="-1",
        sequence="-1",
    ):
        # Write out the payload as JSON into a temporary file
        with open("cli-to-sign.json", "w") as target:
            target.write(json.dumps(payload))
        #
        ps = subprocess.Popen(
            ("printf", f"{self.password}\n"),
            stdout=subprocess.PIPE,
        )
        try:
            result = subprocess.check_output((
                "terracli",
                "tx",
                "sign",
                "cli-to-sign.json",
                "--from",
                f"{self.name}",
                "--offline",
                "--account-number",
                f"{account_number}",
                "--sequence",
                f"{sequence}",
                "--chain-id",
                f"{chain_id}",
                "--gas-prices",
                f"{self.gas_prices}",
                "--home",
                f"{self.home_dir}",
                "--output",
                "json",
            ), stdin=ps.stdout)
            ps.wait()
            """
            1. Wrong Password Error (Return Code 1)
            Throws subprocess.CalledProcessError
            ERROR: invalid account password
            """
            signed_tx = json.loads(str(result, "utf-8"))
            # Remove Signing File
            os.remove("cli-to-sign.json")
            return signed_tx
        except subprocess.CalledProcessError as err:
            error_out = str(err.output, "utf-8")
            raise ValueError(f"terracli threw error: {error_out}")
