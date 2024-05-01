# Design Approach

## Check Structure of Transactions

First of all we need to check the structure of the transaction which includes version, locktime, inputs and outputs.

## Transaction Structure Validation Algorithms.md

### Main Validation Function: `check_transaction(tx_data)`
- Verifies required fields: `"version"`, `"locktime"`, `"vin"`, and `"vout"`.
- Checks field types: `"version"` and `"locktime"` must be integers.
- Calls `validate_vin()` and `validate_vout()` for further validation.

### Vin Validation Function: `validate_vin(vin_list)`
- Checks each `"vin"` element for required fields and types.
- Verifies `"txid"`, `"vout"`, `"prevout"`, `"scriptsig"`/`"scriptsig_asm"`, `"witness"`, `"is_coinbase"`, and `"sequence"`.

### Vout Validation Function: `validate_vout(vout_list)`
- Checks each `"vout"` element for required fields and types.
- Verifies `"scriptpubkey"`, `"scriptpubkey_asm"`, `"scriptpubkey_type"`, `"scriptpubkey_address"`, and `"value"`.

### Signature Script Validation Function: `validate_signature_script(script)`
- Checks if the script is empty, a valid push data script, a valid opcode, or a valid combination of push data and opcodes.

### Checking Transaction Structure in Mempool: `check_structure_transactions(mempool_folder, valid_folder)`
- Iterates through JSON files in the `mempool_folder`.
- Loads transaction data and calls `check_transaction()` for validation.
- Moves valid transactions to the `valid_folder` and prints messages for valid and invalid transactions.
- Handles errors during file processing.

These algorithms work together to validate the structure of Bitcoin transactions, checking the presence and types of required fields, validating `"vin"` and `"vout"` lists, and verifying the signature script. The code also provides a function to validate multiple transaction files in the mempool folder and move valid transactions to a [separate folder](./mempool_valid/).

## Creating Transaction ID(TXID)

Step by step implementation for creating TXID and then updating the json file in `mempool_valid` folder.

1. **Initialize necessary modules and functions:**
   - Import the required modules: `json`, `struct`, `hashlib`, and `os`.
   - Define the `compact_size` function to serialize the size of data in the transaction.
   - Define the `create_txid` function to create the transaction ID (txid) based on the JSON data.

2. **Specify the folder path:**
   - Set the `folder_path` variable to the path of the folder containing the JSON files (e.g., `"./mempool"`).

3. **Iterate over the JSON files in the folder:**
   - Use `os.listdir(folder_path)` to get a list of files in the specified folder.
   - Iterate over each file in the folder using a loop.
   - Check if the file has a `.json` extension using the `endswith()` method.

4. **Read the JSON file:**
   - Construct the full file path by joining the `folder_path` and the current `filename` using `os.path.join()`.
   - Open the JSON file in read mode using `open()` and the `"r"` flag.
   - Read the contents of the file using `file.read()` and store it in the `json_data` variable.

5. **Create the txid:**
   - Call the `create_txid` function, passing the `json_data` as an argument.
   - Inside the `create_txid` function:
     - Parse the JSON data into a dictionary using `json.loads()`.
     - Serialize the transaction data using `struct.pack()` and `compact_size()` functions.
     - Concatenate the serialized data to create the `tx_data` bytes.
   - Calculate the double SHA-256 hash of the `tx_data` using `hashlib.sha256()`.
   - Reverse the byte order of the hash using `[::-1]` and convert it to a hexadecimal string using `hex()`.
   - Store the resulting txid in the `txid` variable.

6. **Append the txid to the JSON data:**
   - Load the JSON data from `json_data` into a dictionary using `json.loads()`.
   - Create a new dictionary called `updated_data` with `"txid"` as the first property and its value set to the generated `txid`.
   - Use the `update()` method to merge the original JSON data dictionary into the `updated_data` dictionary, ensuring that `"txid"` remains the first property.

7. **Write the updated JSON data back to the file:**
   - Open the same JSON file in write mode using `open()` and the `"w"` flag.
   - Write the `updated_data` dictionary to the file using `json.dump()`.
   - Specify an indentation of 2 spaces using `indent=2` for better readability.

## Verifying the transactions

During the verification process I found out that the total number of P2WPKH were lots(around 3000-4000) of them.

And also the P2TR were lots. So verifying the P2TR is out of the scope of this project. The P2TR is considered valid by default.

## Verifying P2PKH Transactions

1. Parse the transaction JSON:

2. Load the transaction JSON data into a Python dictionary called tx.


3. Iterate over each input (vin) in the transaction:

4. For each input, retrieve the scriptPubKey and scriptSig from the transaction data.


5. Extract the public key hash from the scriptPubKey:

6. The public key hash is located in the scriptPubKey field, typically starting from the 7th character and ending 4 characters before the end.


7. Extract the signature and public key from the scriptSig:

8. The scriptSig contains the signature and public key.
The signature length is obtained by converting the 3rd and 4th characters of the scriptSig from hexadecimal to integer.

9. The signature starts after the length and continues for the specified number of bytes.
The public key starts immediately after the signature.


### Verify the public key hash:

1. Hash the extracted public key using SHA-256.

2. Apply the RIPEMD-160 hash function to the SHA-256 hash to obtain the public key hash.

3. Compare the newly computed public key hash with the one extracted from the scriptPubKey.
   
4. If the hashes don't match, print an error message indicating a public key hash mismatch and return False.


### Verify the signature:

1. Decode the extracted public key hash from hexadecimal to bytes.
   
2. Create a VerifyingKey object using the extracted public key and the SECP256k1 elliptic curve.
   
3. Verify the signature using the verify_digest method of the VerifyingKey object.
   
4. The verify_digest method takes the signature, the decoded public key hash, and the hash function (SHA-256) as arguments.
   
5. If the signature verification fails, print an error message indicating the failure and return False.


6. If all inputs pass the verification steps without any errors:

7. Return True to signify a valid transaction.



## Verifying P2WPKH Transactions

Verifying a P2WPKH transaction is a bit different than the traditional one. We need to create a message of the transaction and later verify the message with public key and Elliptic Curve.

1. Creating the preimage of the transaction: 
   - preimage = version + hash256(inputs(txid+vout)) + hash256(sequence) + inputs + scriptcode + amount + sequence + hash256(outputs) + locktime

   - Script Code is basically is a modified version of the ScriptPubKey from the output we're spending. To create the scriptcode, we need to find the ScriptPubKey on the output we want to spend, extract the public key hash, and place it in to the following P2PKH ScriptPubKey structure:
   
      **scriptcode = 1976a914{publickeyhash}88ac**

   - Now we need add the signature hash type to the end if preimage which is SIGHASH_ALL(0x01)
   - Finally we create message which is 
      
      **message = hash256(preimage)** 


2. Now verify the message and signature created for the transaction using ECDSA.

3. If it is successful then return true.


**NOTE: hash256(x) = sha256(sha256(x))**


## Creating Block






# Implementation Details

- Transaction Structure validation: [structural_check.py](./python_files/structural_check.py)

- Creating TXID and Updating the JSoN Structure: [create_txid.py](./python_files/create_txid.py)

- Verifying P2PKH transaction: [p2pkh_validation](./python_files/p2pkh_validation.py)

- Verifying P2WPKH Transaction: [p2wpkh_validation](./python_files/p2wpkh_validation.py)


# Result and Performance
Present the results of your solution, and analyze the efficiency of your solution.


# Conclusion
Discuss any insights gained from solving the problem, and outline potential areas for future improvement or research. Include a list of references or resources consulted during the problem-solving process.