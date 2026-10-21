using System;

public class MotherShip : BasicShip
{
    private string fleetName;
    private double emergencyReserve;

    public MotherShip(int fleetNumber, int baseNumber, int shipNumber, string fleetName, string captainID)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.fleetName = fleetName;
        this.emergencyReserve = 0;
    }

    public MotherShip(int fleetNumber, int baseNumber, int shipNumber, string captainID, string fleetName, double emergencyReserve)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.fleetName = fleetName;
        this.emergencyReserve = 0;
        this.SetEmergencyReserve(emergencyReserve);
    }

    public string GetFleetName()
    {
        return this.fleetName;
    }

    public void SetFleetName(string fleetName)
    {
        this.fleetName = fleetName;
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

    public bool TransferFuel(double amount, ScoutShip target)
    {
        if (target != null && amount > 0)
        {
            if (this.Consume(amount))
            {
                target.Refuel(amount);
                return true;
            }
        }
        return false;
    }

    public override string ToString()
    {
        return base.ToString() + $", FleetName={this.fleetName}, EmergencyReserve={this.emergencyReserve}";
    }
}
