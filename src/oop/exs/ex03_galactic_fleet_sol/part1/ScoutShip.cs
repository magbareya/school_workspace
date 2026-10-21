using System;

public class ScoutShip
{
    private int fleetNumber;
    private int baseNumber;
    private int shipNumber;
    private string captainID;
    private double fuel;
    private double emergencyReserve;

    public ScoutShip(int fleetNumber, int baseNumber, int shipNumber, string captainID)
    {
        this.fleetNumber = fleetNumber;
        this.baseNumber = baseNumber;
        this.shipNumber = shipNumber;
        this.captainID = captainID;
        this.fuel = 0;
        this.emergencyReserve = 0;
    }

    public ScoutShip(int fleetNumber, int baseNumber, int shipNumber, string captainID, double emergencyReserve)
    {
        this.fleetNumber = fleetNumber;
        this.baseNumber = baseNumber;
        this.shipNumber = shipNumber;
        this.captainID = captainID;
        this.fuel = 0;
        this.SetEmergencyReserve(emergencyReserve);
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

    public bool Refuel(double amount)
    {
        if (amount > 0)
        {
            this.fuel += amount;
            return true;
        }
        return false;
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
        return $"ScoutShip {this.shipNumber}: Fleet={this.fleetNumber}, Base={this.baseNumber}, " +
            $"Captain={this.captainID}, Fuel={this.fuel}, EmergencyReserve={this.emergencyReserve}";
    }
}
