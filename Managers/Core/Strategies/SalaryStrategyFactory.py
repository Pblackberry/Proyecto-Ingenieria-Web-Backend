from Models.Core.EmployeeModel import EmployeeData
from Interfaces.ISalaryStrategy import ISalaryStrategy
from Managers.Core.Strategies.SalaryStrategies import StandardSalaryStrategy, ManagerSalaryStrategy

class SalaryStrategyFactory:
    @staticmethod
    def get_strategy(employee_data: EmployeeData) -> ISalaryStrategy:
        if employee_data.Cargo == "Manager":
            return ManagerSalaryStrategy()
        else:
            return StandardSalaryStrategy()