using System;

public class HibernatingDragon : BasicDragon, IComparable
{
    private Date wakeDate;

    public HibernatingDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair, Date wakeDate)
        : base(realmNumber, caveNumber, dragonNumber, riderID, lair)
    {
        this.SetWakeDate(wakeDate);
        this.dragonType = "Hibernating";
    }

    public Date GetWakeDate()
    {
        if (this.wakeDate == null)
        {
            return null;
        }
        return new Date(this.wakeDate);
    }

    public void SetWakeDate(Date wakeDate)
    {
        if (wakeDate != null)
        {
            this.wakeDate = new Date(wakeDate);
        }
    }

    public bool IsEmpty()
    {
        return this.energy <= 0;
    }

    public bool WakeUp(Date today, bool volcanoAlert)
    {
        if (today == null || this.wakeDate == null)
        {
            return false;
        }
        if (today.CompareTo(this.wakeDate) >= 0 || (volcanoAlert && this.energy > 0))
        {
            this.energy = 0;
            return true;
        }
        return false;
    }

    public override bool UseEnergy(object o)
    {
        if (o is Date)
        {
            return this.WakeUp((Date)o, false);
        }
        return false;
    }

    public override bool IsInDanger()
    {
        return this.IsEmpty();
    }

    public override string DangerLevel()
    {
        if (this.energy <= 0)
        {
            return "Critical";
        }
        return "Safe";
    }

    public int CompareTo(object obj)
    {
        if (obj == null || !(obj is HibernatingDragon))
        {
            return 1;
        }
        HibernatingDragon other = (HibernatingDragon)obj;
        return this.wakeDate.CompareTo(other.wakeDate);
    }

    public override string ToString()
    {
        return base.ToString() + $", WakeDate:{this.wakeDate}, Lair:{this.lair}";
    }
}
