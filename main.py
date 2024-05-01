import os
import json


def count_transaction_types(folder_path):
    p2pkh_count = 0
    p2wpkh_count = 0
    p2tr_count = 0

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            # Read the JSON file
            with open(file_path, "r") as file:
                data = json.load(file)

            is_p2pkh = False
            is_p2wpkh = False
            is_p2tr = False

            # Check the transaction type for each input (vin)
            for input_data in data["vin"]:
                if "prevout" in input_data:
                    if input_data["prevout"]["scriptpubkey_type"] == "p2pkh":
                        is_p2pkh = True
                    elif input_data["prevout"]["scriptpubkey_type"] == "v0_p2wpkh":
                        is_p2wpkh = True
                    elif input_data["prevout"]["scriptpubkey_type"] == "v1_p2tr":
                        is_p2tr = True

            # Increment the count based on the transaction type
            if is_p2pkh:
                p2pkh_count += 1
            elif is_p2wpkh:
                p2wpkh_count += 1
            elif is_p2tr:
                p2tr_count += 1

    return p2pkh_count, p2wpkh_count, p2tr_count


# Specify the folder path containing the JSON transaction files
folder_path = "mempool_valid"

# Count the number of p2pkh, p2wpkh & p2tr_count transactions
p2pkh_count, p2wpkh_count, p2tr_count = count_transaction_types(folder_path)

# Print the results
print(f"Number of P2PKH transactions: {p2pkh_count}")
print(f"Number of P2WPKH transactions: {p2wpkh_count}")
print(f"Number of P2TR transactions: {p2tr_count}")
