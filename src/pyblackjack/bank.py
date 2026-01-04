import copy

class Transaction:
    def __init__(self, name: str, amount: float | int, invoice_num: int) -> None:
        self.name = name
        self.value = float(amount)
        self.invoice_num = invoice_num

class Bank:
    """
    A finance handler, useable as the balance for both player and dealer, and for the current bet in each hand.
    
    Attributes:
        balance (float): The current bank balance.
    """
    def __init__(self, balance: float | int = 0.0) -> None:
        """
        Make the bank.
        
        :param balance: The starting balance of the bank.
        :type balance: float | int
        """
        self.__transaction_history: list[Transaction] = [Transaction("Initial Balance", float(balance), 0)]
        self.balance = self._refresh_balance()
        # Debug
        #print(f"DEBUG: Bank(), self.balance: {self.balance}")
    
    def add_transaction(self, name: str, amount: float | int) -> None:
        """
        Adds a transaction and adjusts the bank balance accordingly.
        
        :param name: The transaction name.
        :type name: str
        :param amount: The amount of money in the transaction. Negative numbers decrease balance, positive increase.
        :type amount: float | int
        """
        invoice_num = len(self.__transaction_history)
        # Debug
        #print(f"DEBUG: Bank, add_transaction(name={name}, amount={amount}")
        self.__transaction_history.append(Transaction(name=name, amount=amount, invoice_num=invoice_num))
        self.balance += float(amount)
        # Debug
        #print(f"DEBUG: bank balance: {self.balance}")

    def _refresh_balance(self) -> float:
        return float(sum(t.value for t in self.__transaction_history))
    
    def refresh(self) -> None:
        """
        Forces a refresh of the bank balance based on the entire transaction history.
        """
        self.balance = self._refresh_balance()
    
    def get_history(self, count: int = 1, get_all: bool = False) -> list[Transaction]:
        """
        Returns the bank's transaction history. Last-in-first-out.
        
        :param count: The number of entries from the history to return. Overridden by get_all if True.
        :type count: int
        :param get_all: A flag to return the entire history.
        :type get_all: bool
        :return: The requested history, be it count or all.
        :rtype: list[Transaction]
        """
        if get_all:
            return self.__transaction_history
        return self.__transaction_history[-count:]
    
    def build_new_transaction_record(self, all_transactions: list[list[Transaction]]) -> None:
        """
        Takes a list of multiple bank transaction records, merges them together, replaces the Bank's transaction record with the merged record, and updates the Bank.
        
        :param all_transactions: The list of multiple bank transaction records.
        :type all_transactions: list[list[Transaction]]
        """
        new_transaction_history: list[Transaction] = []

        first_initial = True
        invoice_num = 0
        for transact_list in all_transactions:
            for transaction in transact_list:
                new_transaction: Transaction = copy.deepcopy(transaction)
                if transaction.name == "Initial Balance" and first_initial:
                    first_initial = False
                elif transaction.name == "Initial Balance" and not first_initial:
                    new_transaction.name = "Merged Balance Initial"
                new_transaction.invoice_num = invoice_num
                invoice_num += 1
                new_transaction_history.append(new_transaction)
        self.__transaction_history = new_transaction_history
        self.refresh()
