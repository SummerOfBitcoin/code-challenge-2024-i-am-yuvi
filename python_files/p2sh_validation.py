import json
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1


def validate_p2sh_input(input_data):
    # Extract the redeem script from the scriptsig
    scriptsig_parts = input_data["scriptsig_asm"].split()
    redeem_script = scriptsig_parts[-1]

    # Convert the redeem script to bytes and slice the first 71 bytes
    redeem_script_bytes = bytes.fromhex(redeem_script)
    redeem_script_slice = redeem_script_bytes[:71]

    # Hash the redeem script using SHA-256 and RIPEMD-160
    redeem_script_hash = hashlib.new(
        "ripemd160", hashlib.sha256(redeem_script_slice).digest()
    ).hexdigest()

    # Extract the pubkey hash from the pubkey asm
    pubkey_asm_parts = input_data["prevout"]["scriptpubkey_asm"].split()
    pubkey_hash = pubkey_asm_parts[2]

    # Convert the pubkey hash to bytes and slice the first 20 bytes
    pubkey_hash_bytes = bytes.fromhex(pubkey_hash)
    pubkey_hash_slice = pubkey_hash_bytes[:20]

    # Compare the sliced redeem script and pubkey hash
    if redeem_script_hash != pubkey_hash_slice.hex():
        print(
            f"Redeem script and pubkey hash mismatch for input {input_data['txid']}:{input_data['vout']}"
        )
        return False

    print(
        f"Redeem script hash match for input {input_data['txid']}:{input_data['vout']}"
    )

    # Extract the public keys and signatures from the scriptsig
    scriptsig_parts = input_data["scriptsig_asm"].split()
    num_signatures = int(scriptsig_parts[0][9:])
    signatures = scriptsig_parts[1 : num_signatures + 1]
    num_public_keys = int(scriptsig_parts[num_signatures + 1][9:])
    public_keys = scriptsig_parts[num_signatures + 2 :]

    # Verify each signature against the corresponding public key
    for i in range(num_signatures):
        signature = bytes.fromhex(signatures[i])
        public_key = VerifyingKey.from_string(
            bytes.fromhex(public_keys[i]), curve=SECP256k1
        )

        # TODO: Implement the actual signature verification logic
        # This may involve constructing the transaction hash and verifying the signature against it

    return True


def validate_transaction(tx_json):
    # Parse the transaction JSON
    tx = json.loads(tx_json)

    # Iterate over the inputs
    for vin in tx["vin"]:
        if vin["prevout"]["scriptpubkey_type"] == "p2sh":
            if not validate_p2sh_input(vin):
                return False

    print("All P2SH inputs are valid!")
    return True


# Transaction JSON (replace with your transaction JSON)
tx_json = """
{
  "txid": "66724a7dc43fdba2647c5d453b7ceacd918334c716aa52cb6829cfef0a094a8f",
  "version": 1,
  "locktime": 0,
  "vin": [
    {
      "txid": "5032d895944fdb428e2aeeb022f32070c6db8b7421738bdee91444f3a8fa6465",
      "vout": 1,
      "prevout": {
        "scriptpubkey": "a914dfe791507cb5a44c9a527982f5a69ade6c5421c987",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 dfe791507cb5a44c9a527982f5a69ade6c5421c9 OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "3N6v1vW3gYLYttL2GmaJ28SDw6Y1ZNQX3e",
        "value": 179930847
      },
      "scriptsig": "00483045022100e1804c80eb6aecbb423d1a1223bedc3de5300ce32825a5fe979643727ebb56b00220351385c13fc79e7f8405e433bdd18c8630a446db06b693362f288a7615f7075701483045022100f4dda558ecfae6d2acb68a07f51d8314e6819afebc79fba2674f79320e60d3d002204e497fa8d610514e652939f07876589fa1f2ea36d4ae2570079251a46d4d2f600147522102fa3e97f867f6dd61c8f3870174a62212c568bbfa1d55fd57b8d355343d35a65c2103031d20b72222b1f6fe8217783c0adf898358afc24dee408e518e4af0dc899e7052ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_72 3045022100e1804c80eb6aecbb423d1a1223bedc3de5300ce32825a5fe979643727ebb56b00220351385c13fc79e7f8405e433bdd18c8630a446db06b693362f288a7615f7075701 OP_PUSHBYTES_72 3045022100f4dda558ecfae6d2acb68a07f51d8314e6819afebc79fba2674f79320e60d3d002204e497fa8d610514e652939f07876589fa1f2ea36d4ae2570079251a46d4d2f6001 OP_PUSHBYTES_71 522102fa3e97f867f6dd61c8f3870174a62212c568bbfa1d55fd57b8d355343d35a65c2103031d20b72222b1f6fe8217783c0adf898358afc24dee408e518e4af0dc899e7052ae",
      "is_coinbase": false,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 02fa3e97f867f6dd61c8f3870174a62212c568bbfa1d55fd57b8d355343d35a65c OP_PUSHBYTES_33 03031d20b72222b1f6fe8217783c0adf898358afc24dee408e518e4af0dc899e70 OP_PUSHNUM_2 OP_CHECKMULTISIG"
    },
    {
      "txid": "7f4a843ab6369ca729d17a79474c01d84b4d26650b68d12c036925b798f8d282",
      "vout": 1,
      "prevout": {
        "scriptpubkey": "a914c043d804601f24a42a50bdeb56d434067c3b3c0987",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 c043d804601f24a42a50bdeb56d434067c3b3c09 OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "3KDcwFEYhNkxBJjW9rB9kagj5nNXHnLPJL",
        "value": 68151499
      },
      "scriptsig": "0047304402204f6e0d65b3a7745fda01a98e792012188af3697421c9241795c546d4bfff58ad02203d4293f98afe992defecab5201cfb796cdf05da75fd1cb02405aa59bc7912ede0147304402201ba19b3b137f89382546f23a20d22b79056e8746654df9eb2b5efc3cfc59220102203468a76e79e1709690dd110764e12c6faee394f8603291da2c01f4b038a8306b014752210215a5b70d067d9a73658ea4da51b9f139f44b93c0b262544397db06a7d2d4bb5b2102538fba84abe5b92eadf5cb888c771fb65748585f8cd3d0a4f2e342f9a63226c052ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_71 304402204f6e0d65b3a7745fda01a98e792012188af3697421c9241795c546d4bfff58ad02203d4293f98afe992defecab5201cfb796cdf05da75fd1cb02405aa59bc7912ede01 OP_PUSHBYTES_71 304402201ba19b3b137f89382546f23a20d22b79056e8746654df9eb2b5efc3cfc59220102203468a76e79e1709690dd110764e12c6faee394f8603291da2c01f4b038a8306b01 OP_PUSHBYTES_71 52210215a5b70d067d9a73658ea4da51b9f139f44b93c0b262544397db06a7d2d4bb5b2102538fba84abe5b92eadf5cb888c771fb65748585f8cd3d0a4f2e342f9a63226c052ae",
      "is_coinbase": false,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 0215a5b70d067d9a73658ea4da51b9f139f44b93c0b262544397db06a7d2d4bb5b OP_PUSHBYTES_33 02538fba84abe5b92eadf5cb888c771fb65748585f8cd3d0a4f2e342f9a63226c0 OP_PUSHNUM_2 OP_CHECKMULTISIG"
    },
    {
      "txid": "9dacfe5a46f9d1cb94b04c0b998d7bb9c076c19e3e39e21fd087dad9d89644fa",
      "vout": 2,
      "prevout": {
        "scriptpubkey": "a91480e35cd20e03eb8f347fbb6afe5c5a595e15eeaf87",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 80e35cd20e03eb8f347fbb6afe5c5a595e15eeaf OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "3DSWnXXJZp1TRPKGEPkSzfRGmewRPuY1vr",
        "value": 166670221
      },
      "scriptsig": "0047304402200b302f82484f5f4de31e147df772edc96086f9641b2d2a613a7a3981e63eaf84022015fe54906c3ea06f531ba1de6415a6e7540f873905e299b699feb0b6e562334401473044022055a98030746e73ab97513ec837ceb23a867e6338aabe620379137bf7e9901bd602206c3a59addd5bbcc80f622918f9a833e76e1c1e40e248c1f6400da91f6c0cc00701475221036c240ffbba0ff16c1048dc6a42ca7b8a4a6c1cb3fe6d7798cf186fdaa75849d32103cd4e01550503d884f5d2c9866d87102be721e316bac7287cfb05eb4553865a0352ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_71 304402200b302f82484f5f4de31e147df772edc96086f9641b2d2a613a7a3981e63eaf84022015fe54906c3ea06f531ba1de6415a6e7540f873905e299b699feb0b6e562334401 OP_PUSHBYTES_71 3044022055a98030746e73ab97513ec837ceb23a867e6338aabe620379137bf7e9901bd602206c3a59addd5bbcc80f622918f9a833e76e1c1e40e248c1f6400da91f6c0cc00701 OP_PUSHBYTES_71 5221036c240ffbba0ff16c1048dc6a42ca7b8a4a6c1cb3fe6d7798cf186fdaa75849d32103cd4e01550503d884f5d2c9866d87102be721e316bac7287cfb05eb4553865a0352ae",
      "is_coinbase": false,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 036c240ffbba0ff16c1048dc6a42ca7b8a4a6c1cb3fe6d7798cf186fdaa75849d3 OP_PUSHBYTES_33 03cd4e01550503d884f5d2c9866d87102be721e316bac7287cfb05eb4553865a03 OP_PUSHNUM_2 OP_CHECKMULTISIG"
    },
    {
      "txid": "21cb714d7024c0f2249c173010d5637d7c68ce0bcd1330ccd1de9aab533f5971",
      "vout": 0,
      "prevout": {
        "scriptpubkey": "a9143e0ac1db76b0b5a1a566dd5cfc3450d212506b5687",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 3e0ac1db76b0b5a1a566dd5cfc3450d212506b56 OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "37M4hs6ATjUD7xZs5VDFXPKTGv484Hwivv",
        "value": 10165586
      },
      "scriptsig": "0047304402200e49eea1d31011af92e7b1936dfbbc96648e90d3171a3a641f557becdd363f1302205957dbb5dcf3465dea63c68ec23278954459811533d9322bf781202b333420f801473044022024d42ea0742e54fe88918a4d3dbf96fa1627451fd2e1ed805cebd86eca544190022000aa8dcdfe3918bbad591706a777e0d0c7111855fea1125fc46a843e8c0491bd014752210326a6434dc47a741065abddb8595f3b596681ade39d7ba55c1fd9b6de1abe78c72103962c64bd07cbfbd07f2c8fb48700ad38a4549364fe1fcd016dc80ad61c209b6252ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_71 304402200e49eea1d31011af92e7b1936dfbbc96648e90d3171a3a641f557becdd363f1302205957dbb5dcf3465dea63c68ec23278954459811533d9322bf781202b333420f801 OP_PUSHBYTES_71 3044022024d42ea0742e54fe88918a4d3dbf96fa1627451fd2e1ed805cebd86eca544190022000aa8dcdfe3918bbad591706a777e0d0c7111855fea1125fc46a843e8c0491bd01 OP_PUSHBYTES_71 52210326a6434dc47a741065abddb8595f3b596681ade39d7ba55c1fd9b6de1abe78c72103962c64bd07cbfbd07f2c8fb48700ad38a4549364fe1fcd016dc80ad61c209b6252ae",
      "is_coinbase": false,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 0326a6434dc47a741065abddb8595f3b596681ade39d7ba55c1fd9b6de1abe78c7 OP_PUSHBYTES_33 03962c64bd07cbfbd07f2c8fb48700ad38a4549364fe1fcd016dc80ad61c209b62 OP_PUSHNUM_2 OP_CHECKMULTISIG"
    },
    {
      "txid": "bbaeb508fec9f22fd926207f4ffc2746cefb6ee482f4498461481cd6619878ed",
      "vout": 1,
      "prevout": {
        "scriptpubkey": "a9141960aa3769bbe715debae0abf05438f44970953d87",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 1960aa3769bbe715debae0abf05438f44970953d OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "341Ccjb2pSiSsh73cVY1sYRwNy7ovTuECN",
        "value": 7878524
      },
      "scriptsig": "00483045022100e11070b283f3bdfad50ae358e4a6f27d23f37aa75dfa67f72185be9417f1dc8a02202f5e9cdbb2609bae4e94b2b99d7d9d33232a5ae0c720f1553443807782e9e40901483045022100e116b481b8b5be3427d5105f98ac9f02845dc63cf67e001533cd4c0af369912f022003681b5adcec83a6e1ba76d264fd1bf0e59ef5090259c858ce077041216ebb5e01475221024a0f7b6bfe8db713e5adf3b4f33c35f395781c435dc2dc7318ee8dee3993bd2221027ef1d499b8e4491ffd13ab6825931b961e7669e635fc4d9919d4a2ba70d9c48e52ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_72 3045022100e11070b283f3bdfad50ae358e4a6f27d23f37aa75dfa67f72185be9417f1dc8a02202f5e9cdbb2609bae4e94b2b99d7d9d33232a5ae0c720f1553443807782e9e40901 OP_PUSHBYTES_72 3045022100e116b481b8b5be3427d5105f98ac9f02845dc63cf67e001533cd4c0af369912f022003681b5adcec83a6e1ba76d264fd1bf0e59ef5090259c858ce077041216ebb5e01 OP_PUSHBYTES_71 5221024a0f7b6bfe8db713e5adf3b4f33c35f395781c435dc2dc7318ee8dee3993bd2221027ef1d499b8e4491ffd13ab6825931b961e7669e635fc4d9919d4a2ba70d9c48e52ae",
      "is_coinbase": false,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 024a0f7b6bfe8db713e5adf3b4f33c35f395781c435dc2dc7318ee8dee3993bd22 OP_PUSHBYTES_33 027ef1d499b8e4491ffd13ab6825931b961e7669e635fc4d9919d4a2ba70d9c48e OP_PUSHNUM_2 OP_CHECKMULTISIG"
    },
    {
      "txid": "b92e133f41e265385a72ebf2cd2b6eecdb6bb1094b1a561b88b154a877ed0ded",
      "vout": 1,
      "prevout": {
        "scriptpubkey": "a914c5e1b571a6df358baed6b1f3f1663ae703e2607787",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 c5e1b571a6df358baed6b1f3f1663ae703e26077 OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "3KjKRrW8HB5CHUmQzyqLfqAUDN9XQ5DHQw",
        "value": 78471734
      },
      "scriptsig": "00473044022027bee8a6049be822ae098b70cf75afa29206e9a99a268d0a4a6e0d208d4ba1f702201b07ad33a8dcc544d5721b6772f158fef53fcb49ef2ab22effe24fd9ebc9a125014730440220183097580f0353b2d0cc085b09d9406423e2825d27d43cf3595e7047923d74fb02206f0238bfb315618b02b248dba4bf19cbbbff93e882c0fe780ad81484248719f801475221029af3be7692ee27057a7ebf0854a5a1fb6c5ddd98f3193dbc65d88c3ed251bccb21039edc60b4e40e0d2d7fab21ce1e83832fba9109e3bd5ff82f44338f45a2a7ad8852ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_71 3044022027bee8a6049be822ae098b70cf75afa29206e9a99a268d0a4a6e0d208d4ba1f702201b07ad33a8dcc544d5721b6772f158fef53fcb49ef2ab22effe24fd9ebc9a12501 OP_PUSHBYTES_71 30440220183097580f0353b2d0cc085b09d9406423e2825d27d43cf3595e7047923d74fb02206f0238bfb315618b02b248dba4bf19cbbbff93e882c0fe780ad81484248719f801 OP_PUSHBYTES_71 5221029af3be7692ee27057a7ebf0854a5a1fb6c5ddd98f3193dbc65d88c3ed251bccb21039edc60b4e40e0d2d7fab21ce1e83832fba9109e3bd5ff82f44338f45a2a7ad8852ae",
      "is_coinbase": false,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 029af3be7692ee27057a7ebf0854a5a1fb6c5ddd98f3193dbc65d88c3ed251bccb OP_PUSHBYTES_33 039edc60b4e40e0d2d7fab21ce1e83832fba9109e3bd5ff82f44338f45a2a7ad88 OP_PUSHNUM_2 OP_CHECKMULTISIG"
    },
    {
      "txid": "9aaf5b8ab908d707e12380301e916ed906247f8e88bf6261cdcab5b8efedd291",
      "vout": 1,
      "prevout": {
        "scriptpubkey": "a9141a9e50f810893f0f7dd4eac896318421e6da438387",
        "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 1a9e50f810893f0f7dd4eac896318421e6da4383 OP_EQUAL",
        "scriptpubkey_type": "p2sh",
        "scriptpubkey_address": "347m9YFjvB5HfLhySoiqiP6SmTYtqiyssB",
        "value": 8154808
      },
      "scriptsig": "00483045022100982bf7968b1ec446814405a4f8a09058190e65207420cd5677297766eef0a47c02201fbee3f4e12849c6d826dbd8e1b06083bed367655e2301fd46ce66b586e9d0620147304402205b54ea3a49ba0efe6457ff1ab0ca49da16d8b63f21d41b215e128cbd97c54fdd02203ec4abb36dc69aae3e27637fc1611ae4d87003cf772681e55e62b99101ebddff014752210267d8f07eb04698afd67bcf030f0c1b6c1417fea5f6323b8d9af394b7d35f9a5421035bd8e75688f572f81096b64ea92ca0c44f3f8aec58c4adaa1176be9a58a5949352ae",
      "scriptsig_asm": "OP_0 OP_PUSHBYTES_72 3045022100982bf7968b1ec446814405a4f8a09058190e65207420cd5677297766eef0a47c02201fbee3f4e12849c6d826dbd8e1b06083bed367655e2301fd46ce66b586e9d06201 OP_PUSHBYTES_71 304402205b54ea3a49ba0efe6457ff1ab0ca49da16d8b63f21d41b215e128cbd97c54fdd02203ec4abb36dc69aae3e27637fc1611ae4d87003cf772681e55e62b99101ebddff01 OP_PUSHBYTES_71 52210267d8f07eb04698afd67bcf030f0c1b6c1417fea5f6323b8d9af394b7d35f9a5421035bd8e75688f572f81096b64ea92ca0c44f3f8aec58c4adaa1176be9a58a5949352ae",
      "is_coinbase": false,
      "sequence": 4294967295,
      "inner_redeemscript_asm": "OP_PUSHNUM_2 OP_PUSHBYTES_33 0267d8f07eb04698afd67bcf030f0c1b6c1417fea5f6323b8d9af394b7d35f9a54 OP_PUSHBYTES_33 035bd8e75688f572f81096b64ea92ca0c44f3f8aec58c4adaa1176be9a58a59493 OP_PUSHNUM_2 OP_CHECKMULTISIG"
    }
  ],
  "vout": [
    {
      "scriptpubkey": "76a91479d4762ab5e7fdfff9d612bcc971e798ddb10ac588ac",
      "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 79d4762ab5e7fdfff9d612bcc971e798ddb10ac5 OP_EQUALVERIFY OP_CHECKSIG",
      "scriptpubkey_type": "p2pkh",
      "scriptpubkey_address": "1C7BHJVEVWEaEVKkzR7Gc96bpjvMpcGD5t",
      "value": 519376269
    }
  ]
}
"""

validate_transaction(tx_json)
