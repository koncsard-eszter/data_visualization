import pandas as pd

years = [2007, 2008, 2009, 2010, 2011]
all_rows = []

for y in years:
    df = pd.read_excel("Most Profitable Hollywood Stories.xlsx", sheet_name=f"US {y}")
    df.columns = [str(c).strip() for c in df.columns]

    # Profit oszlop megkeresése (Profitability / Market Profitability / Proftitability)
    prof_col = [c for c in df.columns if "profit" in c.lower() or "proftit" in c.lower()][0]

    # Üres, összesítő ("Average") és "Source" sorok kiszűrése
    df_clean = df[
        df["Film"].notna()
        & ~df["Film"].astype(str).str.lower().isin(["average", "average:", "source"])
    ].copy()

    df_clean = df_clean[["Film", "Genre", "Story", prof_col]].copy()
    df_clean.rename(columns={prof_col: "Profitability"}, inplace=True)
    df_clean["Year"] = y
    df_clean["Profitability"] = pd.to_numeric(df_clean["Profitability"], errors="coerce")
    all_rows.append(df_clean)

full_df = pd.concat(all_rows, ignore_index=True).dropna(subset=["Profitability"])

# Szöveges oszlopok tisztítása és kis/nagybetűk egységesítése
for col in ["Film", "Genre", "Story"]:
    full_df[col] = full_df[col].astype(str).str.strip()
    full_df.loc[full_df[col].isin(["", "nan", "None", "NaN"]), col] = pd.NA

full_df["Genre"] = full_df["Genre"].apply(lambda x: x.title() if pd.notna(x) else x)
full_df["Story"] = full_df["Story"].apply(lambda x: x.title() if pd.notna(x) else x)

# Apró elírások / duplikátumok összevonása
full_df["Story"] = full_df["Story"].replace({
    "Journey & Return": "Journey And Return",
    "The Riddle": "Riddle",
})
full_df["Genre"] = full_df["Genre"].replace({"Biopic": "Biography"})

# Profitabilitás átváltása százalékra (2 tizedesjegyre kerekítve)
full_df["Profit_Pct"] = (full_df["Profitability"] * 100).round(2)

# Végső oszloprend és mentés CSV-be
full_df = full_df[["Year", "Film", "Genre", "Story", "Profit_Pct"]]
full_df.to_csv("hollywood_profit_2007_2011.csv", index=False)

print(f"Kész! Összesen {len(full_df)} film elmentve a 'hollywood_profit_2007_2011.csv' fájlba.")