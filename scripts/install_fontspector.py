"""Install the audited official Fontspector release into the project venv."""
import hashlib
import io
from pathlib import Path
import platform
import subprocess
import tarfile
import urllib.request

VERSION = "1.9.0"
RELEASES = {
    ("Darwin", "arm64"): (
        "aarch64-apple-darwin",
        "0d34d5f85ac7a2efe57157c31f454e56a759edf888879b53af50b76bb1d6b617",
    ),
    ("Linux", "x86_64"): (
        "x86_64-unknown-linux-gnu",
        "0d4a7fbc577f7f99a084dec2a7acc13f64f923cbe44c0e3c5e3d76469786b8e2",
    ),
}


def main():
    key = (platform.system(), platform.machine())
    if key not in RELEASES:
        raise SystemExit(f"Install Fontspector {VERSION} manually for {key}; "
                         "set FONTSPECTOR to its executable path.")
    target, checksum = RELEASES[key]
    stem = f"fontspector-{VERSION}-{target}"
    url = ("https://github.com/fonttools/fontspector/releases/download/"
           f"fontspector-v{VERSION}/{stem}.tar.gz")
    with urllib.request.urlopen(url, timeout=60) as response:
        archive = response.read()
    if hashlib.sha256(archive).hexdigest() != checksum:
        raise SystemExit("Fontspector archive checksum mismatch")
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        member = tar.getmember(f"{stem}/fontspector")
        if not member.isfile():
            raise SystemExit("Expected regular executable in Fontspector archive")
        data = tar.extractfile(member).read()
    destination = Path(__file__).resolve().parents[1] / ".venv/bin/fontspector"
    destination.write_bytes(data)
    destination.chmod(0o755)
    subprocess.run([str(destination), "--version"], check=True)


if __name__ == "__main__":
    main()
