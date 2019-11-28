import subprocess
import simplejson as json


class CLIWallet:

    def __init__(
        self,
        name,
        password,
        home=None,
    ):
        self.name = name
        self.password = password
        self.home = home

    def offline_sign(
        self,
        payload,
        chain_id="-1",
        account_number="-1",
        sequence="-1",
    ):
        # Write out the payload as JSON into a temporary file
        with open("cli-to-sign.json", "w") as target:
            print(payload)
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
        print(str(result, "utf-8"))
        signed_tx = json.loads(str(result, "utf-8"))
        return signed_tx
