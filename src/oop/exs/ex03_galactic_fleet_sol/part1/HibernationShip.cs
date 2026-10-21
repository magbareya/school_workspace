using System;

public class HibernationShip
{
    private int fleetNumber;
    private int baseNumber;
    private int shipNumber;
    private string captainID;
    private double fuel;
    private Date arrivalDate;

    public HibernationShip(int fleetNumber, int baseNumber, int shipNumber, string captainID, Date arrivalDate)
    {
        this.fleetNumber = fleetNumber;
        this.baseNumber = baseNumber;
        this.shipNumber = shipNumber;
        this.captainID = captainID;
        this.fuel = 0;
        this.SetArrivalDate(arrivalDate);
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

    public Date GetArrivalDate()
    {
        if (this.arrivalDate == null)
        {
            return null;
        }
        return new Date(this.arrivalDate);
    }

    public void SetArrivalDate(Date arrivalDate)
    {
        if (arrivalDate != null)
        {
            this.arrivalDate = new Date(arrivalDate);
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

    public bool WithdrawAllFuel(Date withdrawalDate)
    {
        if (withdrawalDate != null && this.arrivalDate != null)
        {
            if (withdrawalDate.CompareTo(this.arrivalDate) >= 0 && this.fuel > 0)
            {
                this.fuel = 0;
                return true;
            }
        }
        return false;
    }

    public override string ToString()
    {
        return $"HibernationShip {this.shipNumber}: Fleet={this.fleetNumber}, Base={this.baseNumber}, " +
            $"Captain={this.captainID}, Fuel={this.fuel}, ArrivalDate={this.arrivalDate}";
    }
}
