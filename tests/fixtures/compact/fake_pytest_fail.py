import sys

sys.stdout.write("collected 6 items\n\n")
sys.stdout.write("test_x.py .....F [100%]\n\n")
sys.stdout.write("=================================== FAILURES ===================================\n")
sys.stdout.write("_______________________________ test_duplicate_callback ________________________\n\n")
sys.stdout.write("    def test_duplicate_callback():\n")
sys.stdout.write('>       assert 1 == 2, "Expected one event, found two"\n')
sys.stdout.write("E       AssertionError: Expected one event, found two\n\n")
sys.stdout.write("test_x.py:42: AssertionError\n")
sys.stdout.write("------------------------------- short test summary info -------------------------\n")
sys.stdout.write("FAILED test_x.py::test_duplicate_callback - AssertionError: Expected one event, found two\n")
sys.stdout.write("======================= 1 failed, 5 passed in 0.02s =======================\n")
sys.exit(1)
