import json
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1


def validate_transaction(tx_json):
    # Parse the transaction JSON
    tx = json.loads(tx_json)

    # Iterate over the inputs
    for vin in tx["vin"]:
        # Get the scriptPubKey and scriptSig
        scriptpubkey = vin["prevout"]["scriptpubkey"]
        scriptsig = vin["scriptsig"]

        # Extract the public key hash from the scriptPubKey
        pubkey_hash = scriptpubkey[6:-4]

        # Extract the signature and public key from the scriptSig
        sig_len = int(scriptsig[2:4], 16)
        sig_start = 4
        sig_end = sig_start + sig_len * 2
        signature = scriptsig[sig_start:sig_end]
        pubkey_start = sig_end + 2
        pubkey = scriptsig[pubkey_start:]

        # Verify the public key hash matches the hash of the public key
        hash_object = hashlib.sha256(bytes.fromhex(pubkey))
        pubkey_hash_new = hashlib.new("ripemd160", hash_object.digest()).hexdigest()
        if pubkey_hash_new != pubkey_hash:
            print(f"Public key hash mismatch for input {vin['txid']}:{vin['vout']}")
            return False

        # Verify the signature
        try:
            # Decode the public key hash
            decoded_hash = bytes.fromhex(pubkey_hash)

            # Decode the public key
            public_key = VerifyingKey.from_string(
                bytes.fromhex(pubkey), curve=SECP256k1
            )

            # Verify the signature
            public_key.verify_digest(
                bytes.fromhex(signature),
                decoded_hash,
                sigdecode=VerifyingKey.from_string(
                    bytes.fromhex(pubkey), curve=SECP256k1, hashfunc=hashlib.sha256
                ).verify_digest,
            )
        except Exception as e:
            print(
                f"Signature verification failed for input {vin['txid']}:{vin['vout']}"
            )
            print(f"Error: {str(e)}")
            return False

    print("All inputs are valid!")
    return True
