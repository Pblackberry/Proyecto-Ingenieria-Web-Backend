from Models.Horarios.TemporadaModel import Temporada
from Models.Core.AssistanceModel import AssistanceReport
from Models.Core.EmployeeModel import EmployeeData
from Models.Core.ReportModel import Salary
def CalcMonthlyPaycheck(season: Temporada, assistance: AssistanceReport, employee_data: EmployeeData) -> Salary:
    area_multiplier = ObtainAreaMuliplier(employee_data, season)
    cargo_multiplier = ObtainCargoMultiplier(employee_data, season)
    paycheck = Salary()
    paycheck.Normal_hours = assistance.Normal_hours*employee_data.Sueldo_hora
    paycheck.Extra_hours = assistance.Extra_hours*(employee_data.Sueldo_hora+2)
    paycheck.Payment =  paycheck.Normal_hours + paycheck.Extra_hours
    paycheck.Payment_with_mult =    paycheck.Payment*area_multiplier*cargo_multiplier
    return  paycheck

def ObtainAreaMuliplier(employee_data: EmployeeData, season: Temporada):
    match employee_data.Area:
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

def ObtainCargoMultiplier(employee_data: EmployeeData, season: Temporada):
    match employee_data.Cargo:
        case "Staff":
            return season.mult_staff
        case "Supervisor":
            return season.mult_supervisor
        case "Manager":
            return season.mult_manager
        case "Area Supervisor":
            return season.mult_as