from .python_files import structural_check

# Run the structural check on the transactions in the mempool
structural_check.check_structure_transactions("./mempool")
