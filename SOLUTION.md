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





# Implementation Details

- Transaction Structure validation: [structural_check.py](./python_files/structural_check.py)

- Creating TXID and Updating the JSoN Structure: [create_txid.py](./python_files/create_txid.py)


# Result and Performance
Present the results of your solution, and analyze the efficiency of your solution.


# Conclusion
Discuss any insights gained from solving the problem, and outline potential areas for future improvement or research. Include a list of references or resources consulted during the problem-solving process.