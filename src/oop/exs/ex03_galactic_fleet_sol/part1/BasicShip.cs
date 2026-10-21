using System;

public class BasicShip
{
    private int fleetNumber;
    private int baseNumber;
    private int shipNumber;
    private string captainID;
    private double fuel;

    public BasicShip(int fleetNumber, int baseNumber, int shipNumber, string captainID)
    {
        this.fleetNumber = fleetNumber;
        this.baseNumber = baseNumber;
        this.shipNumber = shipNumber;
        this.captainID = captainID;
        this.fuel = 0;
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

    public override string ToString()
    {
        return $"BasicShip {this.shipNumber}: Fleet={this.fleetNumber}, Base={this.baseNumber}, " +
            $"Captain={this.captainID}, Fuel={this.fuel}";
    }
}
