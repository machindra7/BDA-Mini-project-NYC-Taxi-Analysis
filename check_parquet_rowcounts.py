import os
import glob
import pyarrow.parquet as pq

LOCAL_DATA_DIR = r"E:\nyc-taxi"

files = glob.glob(os.path.join(LOCAL_DATA_DIR, "*.parquet"))

if not files:
    print("No .parquet files found in", LOCAL_DATA_DIR)
else:
    total_rows = 0
    print(f"Found {len(files)} parquet file(s):\n")
    for f in sorted(files):
        pf = pq.ParquetFile(f)
        num_rows = pf.metadata.num_rows
        size_mb = os.path.getsize(f) / (1024 * 1024)
        total_rows += num_rows
        print(f"{os.path.basename(f):40s} | rows: {num_rows:>10,} | size: {size_mb:,.1f} MB")

    print("\n" + "=" * 60)
    print(f"TOTAL ROWS ACROSS ALL FILES: {total_rows:,}")
    print("=" * 60)