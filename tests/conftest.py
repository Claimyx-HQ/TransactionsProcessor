import pytest
import pandas as pd
import time

@pytest.fixture(autouse=True)
def pandas_display_settings(request):
    # Set pandas display options
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    # Timer setup
    start_time = time.time()

    yield

    # Timer end and log duration
    duration = time.time() - start_time
    node = request.node
    print(f"\nTest {node.nodeid} duration: < {duration:.4f} seconds >")
