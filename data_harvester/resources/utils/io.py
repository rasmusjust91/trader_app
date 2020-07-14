import pandas as pd
import os


def load_csv_files(files_dir, sep="|"):
    files = (
        pd.read_csv(os.path.join(files_dir, f), sep=sep)
        for f in os.listdir(files_dir)
        if f.endswith(".csv")
    )
    df = pd.concat(files, ignore_index=True)

    return df.drop_duplicates()
