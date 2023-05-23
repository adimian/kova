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

    def create_operator(self, name: str):
        self._execute("add", "operator", name)
        logger.success(f"operator {name} created")

    def get_version(self) -> str:
        output = self._execute()
        return output.stderr.strip()

    def get_operator_jwt(self, name: str) -> str:
        operator_jwt = Path(self.data_dir) / name / f"{name}.jwt"
        with operator_jwt.open(mode="r") as f:
            return f.read()
