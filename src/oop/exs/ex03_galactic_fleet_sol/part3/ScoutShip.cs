using System;

public class ScoutShip : BasicShip
{
    private double emergencyReserve;

    public ScoutShip(int fleetNumber, int baseNumber, int shipNumber, string captainID)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.emergencyReserve = 0;
        this.shipType = "Scout";
    }

    public ScoutShip(int fleetNumber, int baseNumber, int shipNumber, string captainID, double emergencyReserve)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.emergencyReserve = 0;
        this.SetEmergencyReserve(emergencyReserve);
        this.shipType = "Scout";
    }

    public double GetEmergencyReserve()
    {
        return this.emergencyReserve;
    }

    public void SetEmergencyReserve(double emergencyReserve)
    {
        if (emergencyReserve >= 0)
        {
            this.emergencyReserve = emergencyReserve;
        }
    }

    public bool Consume(double amount)
    {
        if (amount > 0)
        {
            if (this.fuel - amount >= -this.emergencyReserve)
            {
                this.fuel -= amount;
                return true;
            }
        }
        return false;
    }

    public override bool IsInDanger()
    {
        return this.fuel < 0;
    }

    public string LoanSuggestion()
    {
        if (this.fuel < 0)
        {
            return $"Ship {this.shipNumber} needs a fuel loan of {-this.fuel} units from a MotherShip";
        }
        return "No loan needed";
    }

    public override string ToString()
    {
        return base.ToString() + $", EmergencyReserve:{this.emergencyReserve}";
    }
}
