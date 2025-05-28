from pprint import pprint

import pandas as pd


train = pd.read_csv("affen-trainingsdaten.csv", encoding="iso-8859-15", index_col="mD#Nummer")

merkmale = []

cols = ["Auge links", "Auge rechts", "Mund", "Accessoire"]

for col in cols:
    unique_vals = train[f"D#{col}"].unique()
    # print(col, unique_vals)
    for val in unique_vals:
        merkmale.append((col, val))

# print(train)

def recursive_tree(df: pd.DataFrame, merkmale_done: list):
    if len(df) == 0:
        return "error"
    # pprint(merkmale)

    merkmale_mit_werten = []

    for merkmal in merkmale:
        if merkmal in merkmale_done:
            continue
        (col, val) = merkmal

        beißen_df = df[df["cD#Beschriftung"]=="beißt"]
        nbeißen_df = df[df["cD#Beschriftung"]=="beißt nicht"]

        beißen_absolut = len(beißen_df[beißen_df[f"D#{col}"]==val])
        nbeißen_absolut = len(nbeißen_df[nbeißen_df[f"D#{col}"]==val])
        beißen_relativ = 0 if len(beißen_df) == 0 else beißen_absolut/len(beißen_df)
        nbeißen_relativ = 0 if len(nbeißen_df) == 0 else nbeißen_absolut/len(nbeißen_df)
        # print(merkmal, "x:", beißen_absolut)
        # print(merkmal, "y:", nbeißen_absolut)
        entscheidungskraft = abs(beißen_relativ-nbeißen_relativ)
        merkmale_mit_werten.append((col, val, entscheidungskraft))

        max_merkmal = max(merkmale_mit_werten, key=lambda t: t[2])
        max_col, max_val, *_ = max_merkmal

        yes_df = df[df[f"D#{max_col}"]==max_val]
        no_df = df[df[f"D#{max_col}"]!=max_val]

        print(max_merkmal, len(yes_df), len(no_df))

        return (
            max_merkmal[:2],
            "yes" if len(yes_df)==0 else recursive_tree(yes_df, [*merkmale_done, max_merkmal[:2]]),
            "no" if len(no_df)==0 else recursive_tree(no_df, [*merkmale_done, max_merkmal[:2]]),
        )

pprint(recursive_tree(train, []))