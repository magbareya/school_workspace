using System;

public class HibernatingDragon : BasicDragon
{
    private Date wakeDate;

    public HibernatingDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair, Date wakeDate)
        : base(realmNumber, caveNumber, dragonNumber, riderID, lair)
    {
        this.SetWakeDate(wakeDate);
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

    public override string ToString()
    {
        return base.ToString() + $", WakeDate={this.wakeDate}";
    }
}
