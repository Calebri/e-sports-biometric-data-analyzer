import data_import

DATA_PATH = "./data/esports_gaming_biometrics_250k.csv"

def main() -> None:
    df = data_import.get_clean_data(DATA_PATH)

    print()
    print(df.head())

if __name__ == "__main__":
    main()