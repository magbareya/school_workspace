using System;

public class HibernationShip : BasicShip, IComparable
{
    private Date arrivalDate;

    public HibernationShip(int fleetNumber, int baseNumber, int shipNumber, string captainID, Date arrivalDate)
        : base(fleetNumber, baseNumber, shipNumber, captainID)
    {
        this.SetArrivalDate(arrivalDate);
        this.shipType = "Hibernation";
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

    public bool ZeroFuel()
    {
        return this.fuel <= 0;
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

    public override bool Consume(object o)
    {
        if (o is Date)
        {
            return this.WithdrawAllFuel((Date)o);
        }
        return false;
    }

    public override bool IsInDanger()
    {
        return this.ZeroFuel();
    }

    public int CompareTo(object obj)
    {
        if (obj == null || !(obj is HibernationShip))
        {
            return 1;
        }
        HibernationShip other = (HibernationShip)obj;
        return this.arrivalDate.CompareTo(other.arrivalDate);
    }

    public override string ToString()
    {
        return base.ToString() + $", ArrivalDate:{this.arrivalDate}";
    }
}
