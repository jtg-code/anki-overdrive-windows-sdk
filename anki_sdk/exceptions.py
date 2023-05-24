class NotFoundError(Exception):
    """
    Reason: Reason why the car could not be found
    """
    def __init__(self, reason: str = "Car not found"):
        self.reason = reason
        super().__init__(self.reason)
        
class ImportDisabled(Exception):
    """
    Reason: Reason why the import disabled is
    """
    def __init__(self, reason: str = "Import disabled"):
        self.reason = reason
        super().__init__(self.reason)
        
class NotConnected(Exception):
    """
    Reason: Reason why the car could not be found
    """
    def __init__(self, reason: str = "Car not connected"):
        self.reason = reason
        super().__init__(self.reason)