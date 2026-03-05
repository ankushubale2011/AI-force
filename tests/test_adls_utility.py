import os
import time
import pytest
from adls_utility import (
    initialize_adls_client,
    download_file_from_adls,
    detect_csv_delimiter,
    read_csv_from_adls,
    read_parquet_from_adls,
    read_avro_from_adls
)


def test_initialize_adls_client_positive():
    """Test successful initialization of ADLS client."""
    try:
        account_name = os.getenv("ADLS_ACCOUNT_NAME", "dummy_account")
        account_key = os.getenv("ADLS_ACCOUNT_KEY", "dummy_key")
        client = initialize_adls_client(account_name, account_key)
        assert client is not None
    except Exception as e:
        pytest.fail(f"Unexpected error during initialization: {e}")


def test_initialize_adls_client_negative():
    """Test initialization failure with invalid credentials."""
    try:
        with pytest.raises(Exception):
            initialize_adls_client("", "")
    except Exception as e:
        pytest.fail(f"Unexpected error handling for invalid creds: {e}")


def test_download_file_from_adls_positive(tmp_path):
    """Test downloading a file from ADLS successfully."""
    try:
        account_name = "dummy_account"
        account_key = "dummy_key"
        client = initialize_adls_client(account_name, account_key)
        remote_path = "test_data/sample.csv"
        local_path = tmp_path / "sample.csv"
        result_path = download_file_from_adls(client, remote_path, str(local_path))
        assert os.path.exists(result_path)
    except Exception as e:
        pytest.fail(f"Unexpected error during file download: {e}")


def test_download_file_from_adls_negative(tmp_path):
    """Test handling error when downloading non-existent file."""
    try:
        account_name = "dummy_account"
        account_key = "dummy_key"
        client = initialize_adls_client(account_name, account_key)
        remote_path = "invalid/path/file.csv"
        local_path = tmp_path / "file.csv"
        with pytest.raises(Exception):
            download_file_from_adls(client, remote_path, str(local_path))
    except Exception as e:
        pytest.fail(f"Unexpected error handling invalid file download: {e}")


def test_detect_csv_delimiter_positive():
    """Test detection of valid CSV delimiter."""
    try:
        sample_csv = "col1,col2,col3\nval1,val2,val3"
        delimiter = detect_csv_delimiter(sample_csv)
        assert delimiter == ","
    except Exception as e:
        pytest.fail(f"Unexpected error during delimiter detection: {e}")


def test_detect_csv_delimiter_boundary():
    """Test detection with minimal CSV data."""
    try:
        sample_csv = "col1|col2"
        delimiter = detect_csv_delimiter(sample_csv)
        assert delimiter == "|"
    except Exception as e:
        pytest.fail(f"Unexpected error detecting boundary delimiter: {e}")


def test_read_csv_from_adls_positive(tmp_path):
    """Test reading a CSV file from ADLS successfully."""
    try:
        account_name = "dummy_account"
        account_key = "dummy_key"
        client = initialize_adls_client(account_name, account_key)
        remote_path = "test_data/sample.csv"
        df = read_csv_from_adls(client, remote_path)
        assert not df.empty
    except Exception as e:
        pytest.fail(f"Unexpected error reading CSV: {e}")


def test_read_parquet_from_adls_positive():
    """Test reading a Parquet file from ADLS successfully."""
    try:
        account_name = "dummy_account"
        account_key = "dummy_key"
        client = initialize_adls_client(account_name, account_key)
        remote_path = "test_data/sample.parquet"
        df = read_parquet_from_adls(client, remote_path)
        assert not df.empty
    except Exception as e:
        pytest.fail(f"Unexpected error reading Parquet: {e}")


def test_read_avro_from_adls_positive():
    """Test reading an Avro file from ADLS successfully."""
    try:
        account_name = "dummy_account"
        account_key = "dummy_key"
        client = initialize_adls_client(account_name, account_key)
        remote_path = "test_data/sample.avro"
        df = read_avro_from_adls(client, remote_path)
        assert not df.empty
    except Exception as e:
        pytest.fail(f"Unexpected error reading Avro: {e}")


def test_performance_download_file(tmp_path):
    """Performance test for ADLS file download."""
    try:
        start_time = time.time()
        account_name = "dummy_account"
        account_key = "dummy_key"
        client = initialize_adls_client(account_name, account_key)
        remote_path = "test_data/sample.csv"
        local_path = tmp_path / "sample.csv"
        download_file_from_adls(client, remote_path, str(local_path))
        elapsed_time = time.time() - start_time
        assert elapsed_time < 2
    except Exception as e:
        pytest.fail(f"Unexpected error in performance test: {e}")


def test_security_invalid_access():
    """Security test to ensure unauthorized access fails."""
    try:
        with pytest.raises(Exception):
            initialize_adls_client("invalid_account", "invalid_key")
    except Exception as e:
        pytest.fail(f"Unexpected error during security test: {e}")


def test_usability_detect_csv_delimiter():
    """Usability test to ensure delimiter detection works for end users."""
    try:
        sample_csv = "a;b;c\n1;2;3"
        delimiter = detect_csv_delimiter(sample_csv)
        assert delimiter == ";"
    except Exception as e:
        pytest.fail(f"Unexpected error in usability test: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
