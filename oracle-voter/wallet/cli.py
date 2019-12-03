import subprocess
import os
import simplejson as json


class CLIWallet:
    account_addr = None
    account_num = 0
    account_seq = 0

    def __init__(
        self,
        name,
        password,
        home=None,
        lcd_node={},
    ):
        self.name = name
        self.password = password
        self.home = home
        self.lcd_node = lcd_node
        # Get the account address
        self.get_addr()

    async def sync_state(self):
        account_raw = await self.lcd_node.get_account(self.account_addr)
        self.account_num = account_raw["result"]["value"]["account_number"]
        new_seq = int(account_raw["result"]["value"]["sequence"])
        if new_seq > self.account_seq:
            self.account_seq = new_seq

    def get_addr(self):
        result = subprocess.check_output((
            "terracli",
            "keys",
            "show",
            f"{self.name}",
            "-a",
        ))
        self.account_addr = str(result, "utf-8").strip()

    def offline_sign(
        self,
        payload,
        chain_id="-1",
        account_number="-1",
        sequence="-1",
    ):
        # Write out the payload as JSON into a temporary file
        with open("cli-to-sign.json", "w") as target:
            # print(json.dumps(payload, indent=2))
            target.write(json.dumps(payload))
        #
        ps = subprocess.Popen(
            ("printf", f"{self.password}\n"),
            stdout=subprocess.PIPE,
        )
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
