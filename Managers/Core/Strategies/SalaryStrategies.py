from Interfaces.ISalaryStrategy import ISalaryStrategy
from Models.Horarios.TemporadaModel import Temporada
from Models.Core.AssistanceModel import AssistanceReport
from Models.Core.EmployeeModel import EmployeeData
from Models.Core.ReportModel import Salary

class StandardSalaryStrategy(ISalaryStrategy):
    def CalcMonthlyPaycheck(self, season: Temporada, assistance: AssistanceReport, employee_data: EmployeeData) -> Salary:
        area_multiplier = self._get_area_mult(employee_data.Area, season)
        cargo_multiplier = self._get_cargo_mult(employee_data.Cargo, season)
        
        paycheck = Salary()
        paycheck.Normal_hours = assistance.Normal_hours*employee_data.Sueldo_hora
        paycheck.Extra_hours = assistance.Extra_hours*(employee_data.Sueldo_hora+2)

        paycheck.Payment =  paycheck.Normal_hours + paycheck.Extra_hours
        paycheck.Payment_with_mult =    paycheck.Payment*area_multiplier*cargo_multiplier

        return  paycheck

    def _get_area_mult(self, area, season):
        match area:
            case "Foods":
                return season.mult_foods
            case "House keeping":
                return season.mult_hk
            case "Rides":
                return season.mult_rides
            case "Maintainance":
                return season.mult_maintainance
            case "Lifeguard":
                return season.mult_lifeguard
            case "Games":
                return season.mult_games

    def _get_cargo_mult(self, cargo, season):
        match cargo:
            case "Staff":
                return season.mult_staff
            case "Supervisor":
                return season.mult_supervisor
            case "Manager":
                return season.mult_manager
            case "Area Supervisor":
                return season.mult_as

class ManagerSalaryStrategy(ISalaryStrategy):
    def CalcMonthlyPaycheck(self, season: Temporada, assistance: AssistanceReport, employee_data: EmployeeData) -> Salary:
        paycheck = Salary()

        paycheck.Normal_hours = assistance.Total_hours * employee_data.Sueldo_hora 
        paycheck.Extra_hours = 0 
        
        paycheck.Payment = paycheck.Normal_hours
  
        paycheck.Payment_with_mult = (paycheck.Payment * season.mult_manager) + 500 
        
        return paycheck