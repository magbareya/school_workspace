using System;

public class MotherShip : BasicShip, IComparable
{
    private string fleetName;
    private double emergencyReserve;

    public MotherShip(int fleetNumber, int baseNumber, int shipNumber, string fleetName, string captainID)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.fleetName = fleetName;
        this.emergencyReserve = 0;
        this.shipType = "Mother";
    }

    public MotherShip(int fleetNumber, int baseNumber, int shipNumber, string captainID, string fleetName, double emergencyReserve)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.fleetName = fleetName;
        this.emergencyReserve = 0;
        this.SetEmergencyReserve(emergencyReserve);
        this.shipType = "Mother";
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

    public double GetPowerPotential()
    {
        return this.fuel + this.emergencyReserve;
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

    public override bool Consume(object o)
    {
        if (o is double)
        {
            return this.Consume((double)o);
        }
        if (o is int)
        {
            return this.Consume((double)(int)o);
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

    public override bool IsInDanger()
    {
        return this.emergencyReserve > 0 && this.fuel <= -0.9 * this.emergencyReserve;
    }

    public string LoanSuggestion()
    {
        if (this.fuel < -0.5 * this.emergencyReserve)
        {
            return $"MotherShip {this.shipNumber} ({this.fleetName}) requires emergency resupply of {-this.fuel} units";
        }
        return "No loan needed";
    }

    public int CompareTo(object obj)
    {
        if (obj == null || !(obj is MotherShip))
        {
            return 1;
        }
        MotherShip other = (MotherShip)obj;
        double diff = this.GetPowerPotential() - other.GetPowerPotential();
        if (diff > 0)
        {
            return 1;
        }
        if (diff < 0)
        {
            return -1;
        }
        return 0;
    }

    public override string ToString()
    {
        return base.ToString() + $", FleetName:{this.fleetName}, EmergencyReserve:{this.emergencyReserve}";
    }
}
