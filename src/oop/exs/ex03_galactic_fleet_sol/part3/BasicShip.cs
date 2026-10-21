using System;

public class BasicShip
{
    protected int fleetNumber;
    protected int baseNumber;
    protected int shipNumber;
    protected string captainID;
    protected double fuel;
    protected string shipType;

    public BasicShip(int fleetNumber, int baseNumber, int shipNumber, string captainID)
    {
        this.fleetNumber = fleetNumber;
        this.baseNumber = baseNumber;
        this.shipNumber = shipNumber;
        this.captainID = captainID;
        this.fuel = 0;
        this.shipType = "Basic";
    }

    public int GetFleetNumber()
    {
        return this.fleetNumber;
    }

    public int GetBaseNumber()
    {
        return this.baseNumber;
    }

    public int GetShipNumber()
    {
        return this.shipNumber;
    }

    public string GetCaptainID()
    {
        return this.captainID;
    }

    public double GetFuel()
    {
        return this.fuel;
    }

    public bool Refuel(double amount)
    {
        if (amount > 0)
        {
            this.fuel += amount;
            return true;
        }
        return false;
    }

    public virtual bool IsInDanger()
    {
        return false;
    }

    public override bool Equals(object obj)
    {
        if (obj == null || !(obj is BasicShip))
        {
            return false;
        }
        BasicShip other = (BasicShip)obj;
        return this.fleetNumber == other.fleetNumber &&
               this.baseNumber == other.baseNumber &&
               this.shipNumber == other.shipNumber;
    }

    public override string ToString()
    {
        return $"Type:{this.shipType}, Num:{this.shipNumber}, Captain:{this.captainID}, Fuel:{this.fuel}";
    }
}
