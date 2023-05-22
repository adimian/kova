import subprocess


class NscException(Exception):
    pass


class NscWrapper:
    def __init__(self, nsc_path: str):
        self.nsc_path = nsc_path

    def get_version(self) -> str:
        output = subprocess.run(
            [self.nsc_path, "--version"],
            capture_output=True,
            text=True,
            shell=True,
        )

        if not output.returncode:
            return output.stderr.strip()
        else:
            raise NscException(output.stderr)
