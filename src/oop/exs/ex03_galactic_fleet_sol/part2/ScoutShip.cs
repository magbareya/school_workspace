using System;

public class ScoutShip : BasicShip
{
    private double emergencyReserve;

    public ScoutShip(int fleetNumber, int baseNumber, int shipNumber, string captainID)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.emergencyReserve = 0;
    }

    public ScoutShip(int fleetNumber, int baseNumber, int shipNumber, string captainID, double emergencyReserve)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.emergencyReserve = 0;
        this.SetEmergencyReserve(emergencyReserve);
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

    public override string ToString()
    {
        return base.ToString() + $", EmergencyReserve={this.emergencyReserve}";
    }
}
