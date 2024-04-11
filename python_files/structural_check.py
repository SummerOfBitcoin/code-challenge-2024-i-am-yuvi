import json
import os
import shutil


def check_transaction(tx_data):

    required_fields = ["version", "locktime", "vin", "vout"]
    if not all(field in tx_data for field in required_fields):
        return False  # Missing fields

    # Basic checks for specific field types
    if not isinstance(tx_data["version"], int):
        return False
    if not isinstance(tx_data["locktime"], int):
        return False

    # Call the vin and vout checker functions
    if not validate_vin(tx_data["vin"]):
        return False
    if not validate_vout(tx_data["vout"]):
        return False

    return True  # Passes basic checks


def validate_vin(vin_list):
    # Validates a list of vin elements with specific checks
    for vin in vin_list:
        # Check txid
        if not vin.get("txid") or not isinstance(vin["txid"], str):
            return False, "txid is empty or invalid type"

        # Check vout
        if not vin.get("vout") or not isinstance(vin["vout"], int):
            return False, "vout is empty or invalid type"

        # Check prevout
        prevout = vin.get("prevout")
        if not prevout:
            return False, "prevout is missing"
        required_prevout_fields = [
            "scriptpubkey",
            "scriptpubkey_asm",
            "scriptpubkey_type",
            "scriptpubkey_address",
            "value",
        ]
        for field in required_prevout_fields:
            if field not in prevout:
                return False, f"prevout is missing '{field}'"

        # Check scriptsig/scriptsig_asm and witness if applicable
        scriptsig = vin.get("scriptsig")
        scriptsig_asm = vin.get("scriptsig_asm")

        if not scriptsig and not scriptsig_asm:
            # Both empty, check for witness
            if not vin.get("witness"):
                return (
                    False,
                    "Both scriptsig and scriptsig_asm are empty, and witness is missing",
                )

        # Check is_coinbase
        if not isinstance(vin.get("is_coinbase"), bool):
            return False  # is_coinbase must be true or false

        # Check sequence
        if not vin.get("sequence") or not isinstance(vin["sequence"], int):
            return False  # sequence is empty or invalid type

    # All checks passed
    return True


def validate_vout(vout_list):
    # Validates a list of vout elements with specific checks
    for vout in vout_list:
        # Check non-emptiness of fields
        required_fields = [
            "scriptpubkey",
            "scriptpubkey_asm",
            "scriptpubkey_type",
            "scriptpubkey_address",
        ]
        for field in required_fields:
            if not vout.get(field) or not isinstance(vout[field], str):
                return False, f"'{field}' is empty or invalid type"

        # Check value is non-empty integer
        if not vout.get("value") or not isinstance(vout["value"], int):
            return False, "value is empty or invalid type"

    # All checks passed
    return True, "vout is valid"


def check_structure_transactions(mempool_folder, valid_folder):
    for filename in os.listdir(mempool_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(mempool_folder, filename)
            try:
                with open(filepath) as f:
                    tx_data = json.load(f)
                if check_transaction(tx_data):
                    print(f"Transaction: {filename} - Valid Structure")
                    # Move the valid transaction file to the mempool_valid folder
                    shutil.copy(filepath, os.path.join(valid_folder, filename))
                else:
                    print(f"Transaction: {filename} - Missing or Invalid Fields")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error processing {filename}: {e}")


# validate the signature script
def validate_signature_script(script):
    """Validates a Bitcoin signature script.

    Args:
      script: The signature script to validate.

    Returns:
      True if the signature script is valid, False otherwise.
    """

    # Check if the script is empty.
    if not script:
        return False

    # Check if the script is a valid push data script.
    if script[0] >= 0x01 and script[0] <= 0x4B:
        return True

    # Check if the script is a valid opcode.
    if script[0] in OP_CODES:
        return True

    # Check if the script is a valid combination of push data and opcodes.
    for i in range(len(script)):
        if script[i] >= 0x01 and script[i] <= 0x4B:
            continue

        if script[i] not in OP_CODES:
            return False

    # The script is valid.
    return True


# Specify the input and output folders
mempool_folder = "./mempool"
valid_folder = "./mempool_valid"

# Check the structure of transactions in the mempool folder
check_structure_transactions(mempool_folder, valid_folder)
