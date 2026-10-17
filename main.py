import pytest
import subprocess
import sys
from plot import main

if __name__ == "__main__":
    result = pytest.main(["-s", "test/test_lab.py"])

    if result != pytest.ExitCode.OK:
        sys.exit(result)

    subprocess.run([sys.executable, "test_time.py"], check=True)

    main()
