class Bank:
    def __init__(self, balance: float | int = 0.0) -> None:
        self.__balance: float = float(balance)
    
    def check_balance(self) -> float:
        return self.__balance
    
    def receive_payout(self, amount: float | int) -> float:
        if amount < 0:
            raise ValueError("Can't receive a negative payout.")
        self.__balance += amount
        return self.__balance
    
    def charge_account(self, amount: float | int) -> float:
        if amount < 0:
            raise ValueError("Can't be charged a negative amount.")
        self.__balance -= amount
        return self.__balance