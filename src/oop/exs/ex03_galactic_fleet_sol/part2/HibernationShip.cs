using System;

public class HibernationShip : BasicShip
{
    private Date arrivalDate;

    public HibernationShip(int fleetNumber, int baseNumber, int shipNumber, string captainID, Date arrivalDate)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.SetArrivalDate(arrivalDate);
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
        return base.ToString() + $", ArrivalDate={this.arrivalDate}";
    }
}
