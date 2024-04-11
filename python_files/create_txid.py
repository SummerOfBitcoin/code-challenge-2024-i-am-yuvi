import json
import struct
import hashlib
import os


def compact_size(size):
    if size < 253:
        return struct.pack("<B", size)
    elif size < 2**16:
        return struct.pack("<B", 253) + struct.pack("<H", size)
    elif size < 2**32:
        return struct.pack("<B", 254) + struct.pack("<I", size)
    else:
        return struct.pack("<B", 255) + struct.pack("<Q", size)


def create_txid(json_data):
    data = json.loads(json_data)
    tx_data = struct.pack("<I", data["version"])
    tx_data += compact_size(len(data["vin"]))
    for vin in data["vin"]:
        tx_data += bytes.fromhex(vin["txid"])[::-1]
        tx_data += struct.pack("<I", vin["vout"])
        script_sig = bytes.fromhex(vin["scriptsig"])
        tx_data += compact_size(len(script_sig))
        tx_data += script_sig
        tx_data += struct.pack("<I", vin["sequence"])
    tx_data += compact_size(len(data["vout"]))
    for vout in data["vout"]:
        tx_data += struct.pack("<q", vout["value"])
        script_pubkey = bytes.fromhex(vout["scriptpubkey"])
        tx_data += compact_size(len(script_pubkey))
        tx_data += script_pubkey
    tx_data += struct.pack("<I", data["locktime"])
    return tx_data


# Specify the folder path containing the JSON files
folder_path = "./mempool_valid/"

# Iterate over the JSON files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)

        # Read the JSON file
        with open(file_path, "r") as file:
            json_data = file.read()

        # Create the txid for the transaction
        tx_bytes = create_txid(json_data)
        txid = hashlib.sha256(hashlib.sha256(tx_bytes).digest()).digest()[::-1].hex()

        # Load the JSON data into a dictionary
        data = json.loads(json_data)

        # Create a new dictionary with txid as the first property
        updated_data = {"txid": txid}
        updated_data.update(data)

        # Write the updated JSON data back to the same file
        with open(file_path, "w") as file:
            json.dump(updated_data, file, indent=2)
