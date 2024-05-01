import hashlib
from ecdsa import VerifyingKey, SECP256k1


def hash256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def verify_p2wpkh_transaction(transaction):
    # Extract relevant data from the transaction
    version = transaction["version"]
    inputs = transaction["vin"]
    outputs = transaction["vout"]
    locktime = transaction["locktime"]

    # Create the preimage
    preimage = b""
    preimage += version.to_bytes(4, byteorder="little")

    # Hash256 of inputs (txid + vout)
    input_data = b""
    for input_tx in inputs:
        input_data += bytes.fromhex(input_tx["txid"])[::-1]
        input_data += input_tx["vout"].to_bytes(4, byteorder="little")
    preimage += hash256(input_data)

    # Hash256 of sequence
    sequence_data = b""
    for input_tx in inputs:
        sequence_data += input_tx["sequence"].to_bytes(4, byteorder="little")
    preimage += hash256(sequence_data)

    # Inputs
    for input_tx in inputs:
        preimage += bytes.fromhex(input_tx["txid"])[::-1]
        preimage += input_tx["vout"].to_bytes(4, byteorder="little")

    # ScriptCode
    scriptcode = b""
    for input_tx in inputs:
        public_key_hash = input_tx["prevout"]["scriptpubkey"][-42:-4]
        scriptcode = b"\x19\x76\xa9\x14" + bytes.fromhex(public_key_hash) + b"\x88\xac"
        preimage += scriptcode

    # Amount
    for input_tx in inputs:
        amount = input_tx["prevout"]["value"]
        preimage += amount.to_bytes(8, byteorder="little")

    # Sequence
    for input_tx in inputs:
        preimage += input_tx["sequence"].to_bytes(4, byteorder="little")

    # Hash256 of outputs
    output_data = b""
    for output in outputs:
        output_data += output["value"].to_bytes(8, byteorder="little")
        output_data += len(output["scriptpubkey"]).to_bytes(1, byteorder="little")
        output_data += bytes.fromhex(output["scriptpubkey"])
    preimage += hash256(output_data)

    # Locktime
    preimage += locktime.to_bytes(4, byteorder="little")

    # Add SIGHASH_ALL (0x01)
    preimage += b"\x01"

    # Create the message
    message = hash256(preimage)

    # Verify the signature
    for input_tx in inputs:
        signature = bytes.fromhex(input_tx["witness"][0])
        public_key = bytes.fromhex(input_tx["witness"][1])

        verifying_key = VerifyingKey.from_string(public_key, curve=SECP256k1)
        if not verifying_key.verify(signature, message):
            return False

    return True
