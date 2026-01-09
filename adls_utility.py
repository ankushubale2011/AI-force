"""
=============================================================================
COPYRIGHT NOTICE
=============================================================================
© Copyright HCL Technologies Ltd. 2021, 2022, 2023
Proprietary and confidential. All information contained herein is, and
remains the property of HCL Technologies Limited. Copying or reproducing the
contents of this file, via any medium is strictly prohibited unless prior
written permission is obtained from HCL Technologies Limited.
"""
from typing import Iterable, List, Optional

import io
import os

import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
from detect_delimiter import detect
import pandavro as pdx


# ==============================
# Module-level constants/paths
# ==============================
DEFAULT_SCHEME: str = "https"
DFS_URL_TEMPLATE: str = "{scheme}://{account}.dfs.core.windows.net"

# Temporary file locations (kept to preserve original I/O behavior/encoding)
TEMP_DIR: str = "adls_file"
CSV_TEMP_FILENAME: str = "csv_file.txt"
AVRO_TEMP_FILENAME: str = "avro_file.avro"
CSV_TEMP_PATH: str = os.path.join(TEMP_DIR, CSV_TEMP_FILENAME)
AVRO_TEMP_PATH: str = os.path.join(TEMP_DIR, AVRO_TEMP_FILENAME)

# File type handling
CSV_EXTENSIONS: tuple = ("csv", "tsv")
PARQUET_EXTENSION: str = "parquet"
AVRO_EXTENSION: str = "avro"

# Parsing/reader options
DELIMITER_WHITELIST: List[str] = [",", ";", ":", "|", "\t"]
DEFAULT_CSV_DELIMITER: str = ","
PARQUET_ENGINE: str = "pyarrow"

# Global client as in the original implementation
service_client: Optional[DataLakeServiceClient] = None


def _build_account_url(
    storage_account_name: str,
    scheme: str = DEFAULT_SCHEME,
    template: str = DFS_URL_TEMPLATE,
) -> str:
    """
    Build the DFS endpoint URL for the given storage account.

    Args:
        storage_account_name: Azure Storage account name.
        scheme: URL scheme to use (e.g., 'https').
        template: URL template.

    Returns:
        The formatted account URL.
    """
    try:
        # Create and return URL using provided scheme and template
        return template.format(scheme=scheme, account=storage_account_name)
    except Exception as exc:
        # Provide context if formatting fails (should be rare)
        raise ValueError("Failed to construct Data Lake account URL.") from exc


def _ensure_dir_exists(path: str) -> None:
    """
    Ensure the directory for the given file path exists.

    Args:
        path: File path whose parent directory should exist.
    """
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    except Exception as exc:
        raise OSError(f"Failed to ensure directory exists for path: {path}") from exc


def _detect_delimiter_from_text(
    data: str,
    whitelist: Iterable[str],
    default_delimiter: str = DEFAULT_CSV_DELIMITER,
) -> str:
    """
    Detect the delimiter from text with a safe fallback.

    Args:
        data: Sample text to analyze.
        whitelist: Allowed delimiter characters.
        default_delimiter: Fallback delimiter if detection fails.

    Returns:
        The detected delimiter or the default.
    """
    try:
        detected = detect(text=data, default=None, whitelist=list(whitelist))
        return detected if detected else default_delimiter
    except Exception:
        # If detection unexpectedly errors, return the default to proceed
        return default_delimiter


def _get_file_extension(path_name: str) -> Optional[str]:
    """
    Extract a lowercase file extension (without leading dot) from a path.

    Args:
        path_name: The file path or name.

    Returns:
        The file extension without dot or None if not present.
    """
    try:
        _, ext = os.path.splitext(path_name)
        if not ext:
            return None
        return ext.lstrip(".").lower()
    except Exception as exc:
        raise ValueError(f"Failed to parse extension from path: {path_name}") from exc


def _download_file_to_bytes(file_client) -> bytes:
    """
    Download a file from ADLS to memory as bytes.

    Args:
        file_client: DataLake file client for the target file.

    Returns:
        File content as bytes.
    """
    try:
        downloader = file_client.download_file()
        # Using readall() to simplify reading into memory
        return downloader.readall()
    except Exception as exc:
        raise IOError("Failed to download file from ADLS.") from exc


def _safe_select_fields(df: pd.DataFrame, fields: Iterable[str]) -> pd.DataFrame:
    """
    Return a DataFrame with only the requested columns. Missing columns are filled with NaN.

    Args:
        df: Input DataFrame.
        fields: Desired column names.

    Returns:
        DataFrame reindexed to the requested columns.
    """
    try:
        fields_list = list(fields)
        # Reindex ensures missing columns are created with NaN instead of raising.
        return df.reindex(columns=fields_list)
    except Exception as exc:
        raise ValueError("Failed to select requested fields from DataFrame.") from exc


def initialize_storage_account(storage_account_name: str, storage_account_key: str) -> None:
    """
    Initialize the global DataLakeServiceClient using the provided credentials.

    Args:
        storage_account_name: Azure Storage account name.
        storage_account_key: Access key for the storage account.

    Raises:
        RuntimeError: If the client cannot be created.
    """
    try:
        global service_client
        scheme = DEFAULT_SCHEME  # function-level variable for hardcoded scheme
        url_template = DFS_URL_TEMPLATE  # function-level variable for URL template
        account_url = _build_account_url(storage_account_name, scheme=scheme, template=url_template)

        service_client = DataLakeServiceClient(
            account_url=account_url,
            credential=storage_account_key,
        )
    except Exception as exc:
        # Do not print; raise with context for proper handling upstream
        raise RuntimeError("Failed to initialize Azure Data Lake service client.") from exc


def get_field_value_from_adls(
    storage_name: str,
    storage_key: str,
    container_name: str,
    parent_folder_name: str,
    field_list: List[str],
) -> pd.DataFrame:
    """
    Retrieve specified fields from files stored in ADLS under a given folder.

    Supports CSV/TSV (delimiter auto-detection with safe fallback), Parquet, and Avro.
    Data from multiple files is concatenated into a single DataFrame.

    Args:
        storage_name: Azure Storage account name.
        storage_key: Azure Storage account key.
        container_name: ADLS container (file system) name.
        parent_folder_name: Parent directory path within the container to scan.
        field_list: List of column names to extract.

    Returns:
        A pandas DataFrame containing the requested fields from all matching files.

    Raises:
        RuntimeError: On failures initializing the client or accessing ADLS resources.
        OSError/IOError: On local temp file or download failures.
        ValueError: When parsing file metadata or selecting fields fails.
    """
    try:
        # Initialize client (raises if fails)
        initialize_storage_account(storage_name, storage_key)

        # Defensive check to satisfy type-checkers; initialize raises if failed
        if service_client is None:
            raise RuntimeError("Data Lake service client is not initialized.")

        # Obtain file system and list paths
        file_system_client = service_client.get_file_system_client(container_name)
        file_paths = file_system_client.get_paths(path=parent_folder_name)

        # Accumulate per-file DataFrames for efficient concatenation
        frames: List[pd.DataFrame] = []

        for path in file_paths:
            try:
                # Skip directories
                if getattr(path, "is_directory", False):
                    continue

                file_path_name = getattr(path, "name", None)
                if not file_path_name:
                    continue

                file_client = file_system_client.get_file_client(file_path_name)
                file_ext = _get_file_extension(file_path_name)

                # Skip files without a recognized extension
                if not file_ext:
                    continue

                processed_df: Optional[pd.DataFrame] = None

                # Branch by supported file types
                if file_ext in CSV_EXTENSIONS:
                    # Keep disk I/O to preserve original behavior and encoding handling
                    tmp_csv_path = CSV_TEMP_PATH  # function-level variable for temp csv path
                    _ensure_dir_exists(tmp_csv_path)

                    # Download and write bytes to temp file
                    content_bytes = _download_file_to_bytes(file_client)
                    with open(tmp_csv_path, "wb") as tmp_csv_file:
                        tmp_csv_file.write(content_bytes)

                    # Read text back for delimiter detection (default system encoding)
                    with open(tmp_csv_path, "r") as tmp_text_file:
                        text_data = tmp_text_file.read()

                    row_delimiter = _detect_delimiter_from_text(
                        text_data, whitelist=DELIMITER_WHITELIST, default_delimiter=DEFAULT_CSV_DELIMITER
                    )

                    processed_df = pd.read_csv(tmp_csv_path, sep=row_delimiter)

                elif file_ext == PARQUET_EXTENSION:
                    # Read parquet from in-memory buffer
                    content_bytes = _download_file_to_bytes(file_client)
                    stream = io.BytesIO(content_bytes)
                    processed_df = pd.read_parquet(stream, engine=PARQUET_ENGINE)

                elif file_ext == AVRO_EXTENSION:
                    # Keep disk I/O to preserve original behavior for pandavro
                    tmp_avro_path = AVRO_TEMP_PATH  # function-level variable for temp avro path
                    _ensure_dir_exists(tmp_avro_path)

                    content_bytes = _download_file_to_bytes(file_client)
                    with open(tmp_avro_path, "wb") as tmp_avro_file:
                        tmp_avro_file.write(content_bytes)

                    processed_df = pdx.read_avro(tmp_avro_path)

                # Unknown extension -> skip
                else:
                    continue

                # If a dataframe was produced, safely select requested fields and accumulate
                if processed_df is not None:
                    selected_df = _safe_select_fields(processed_df, field_list)
                    frames.append(selected_df)

            except Exception as file_exc:
                # Propagate with context for the specific file to maintain debuggability
                raise RuntimeError(f"Failed processing file: {getattr(path, 'name', '<unknown>')}") from file_exc

        # Concatenate all frames; return empty DataFrame if none
        if frames:
            return pd.concat(frames, ignore_index=True)
        return pd.DataFrame()

    except Exception as exc:
        # Single exit point with contextual error
        raise RuntimeError("Failed to retrieve field values from ADLS.") from exc
