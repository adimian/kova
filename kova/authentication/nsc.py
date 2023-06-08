import subprocess
from pathlib import Path

from loguru import logger


class NscException(Exception):
    pass


class NscWrapper:
    def __init__(
        self,
        keystore_dir: str,
        data_dir: str,
        nsc_path: str = "nsc",
    ):
        self.nsc_path = nsc_path
        self.keystore_dir = keystore_dir
        self.data_dir = data_dir

    def _execute(self, *args, **kwargs) -> subprocess.CompletedProcess:
        command = [
            self.nsc_path,
            "--keystore-dir",
            f'"{self.keystore_dir}"',
            "--data-dir",
            f'"{self.data_dir}"',
        ]
        command.extend(args)

        kw = {
            "capture_output": True,
            "text": True,
            "shell": True,
        }
        kw.update(kwargs)

        output = subprocess.run(args=" ".join(command), **kw)  # type: ignore
        logger.warning(output.stderr)

        if not output.returncode:
            logger.success(output.stdout)
            return output
        else:
            logger.error(output.stdout)
            raise NscException(output.stderr)

    def _get_argument(self, **kwargs):
        arguments = []
        for arg in kwargs:
            var = arg.replace("_", "-")
            arguments.append(f"--{var}")
            arguments.append(f'"{kwargs[arg]}"')
        return arguments

    def create_operator(self, name: str):
        try:
            self._execute("add", "operator", name)
            logger.success(f"operator {name} created")
        except NscException as exception:
            if str(exception).startswith(
                f"[ERR ] operator named {name} exists already"
            ):
                logger.debug(f"operator {name} already created")
            else:
                raise NscException(str(exception))

    def create_account(self, name: str):
        try:
            self._execute("add", "account", name)
            logger.success(f"account {name} created")
        except NscException as exception:
            if str(exception).startswith(
                f'Error: the account "{name}" already exists'
            ):
                logger.debug(f"account {name} already created")
            else:
                raise NscException(str(exception))

    def create_user(self, name: str, **kwargs):
        arguments = self._get_argument(**kwargs)
        self._execute("add", "user", name, " ".join(arguments))

        logger.success(f"user {name} created")

    def edit_user(self, name: str, **kwargs):
        arguments = self._get_argument(**kwargs)
        self._execute("edit", "user", name, " ".join(arguments))

        logger.success(f"user {name} edited")

    def get_version(self) -> str:
        output = self._execute("--version")
        return output.stdout.strip()

    def get_operator_jwt(self, name: str) -> str:
        operator_jwt = Path(self.data_dir) / name / f"{name}.jwt"
        with operator_jwt.open(mode="r") as f:
            return f.read()

    def get_account_jwt(self, name: str, operator: str) -> str:
        account_jwt = (
            Path(self.data_dir) / operator / "accounts" / name / f"{name}.jwt"
        )
        with account_jwt.open(mode="r") as f:
            return f.read()

    def get_user_jwt(self, name: str, account: str, operator: str) -> str:

        user_jwt = (
            Path(self.data_dir)
            / operator
            / "accounts"
            / account
            / "users"
            / f"{name}.jwt"
        )
        with user_jwt.open(mode="r") as f:
            return f.read()

    def get_user_credentials(
        self, name: str, account: str, operator: str
    ) -> str:
        user_credentials = (
            Path(self.keystore_dir)
            / "creds"
            / operator
            / account
            / f"{name}.creds"
        )
        with user_credentials.open(mode="r") as f:
            return f.read()
