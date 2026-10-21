using System;

public class HibernatingDragon
{
    private int realmNumber;
    private int caveNumber;
    private int dragonNumber;
    private string riderID;
    private Coordinates lair;
    private double energy;
    private Date wakeDate;

    public HibernatingDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair, Date wakeDate)
    {
        this.realmNumber = realmNumber;
        this.caveNumber = caveNumber;
        this.dragonNumber = dragonNumber;
        this.riderID = riderID;
        this.SetLair(lair);
        this.energy = 0;
        this.SetWakeDate(wakeDate);
    }

    public int GetRealmNumber()
    {
        return this.realmNumber;
    }

    public int GetCaveNumber()
    {
        return this.caveNumber;
    }

    public int GetDragonNumber()
    {
        return this.dragonNumber;
    }

    public string GetRiderID()
    {
        return this.riderID;
    }

    public Coordinates GetLair()
    {
        if (this.lair == null)
        {
            return null;
        }
        return new Coordinates(this.lair);
    }

    public void SetLair(Coordinates lair)
    {
        if (lair != null)
        {
            this.lair = new Coordinates(lair);
        }
    }

    public double GetEnergy()
    {
        return this.energy;
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

    public bool Refuel(double amount)
    {
        if (amount > 0)
        {
            this.energy += amount;
            return true;
        }
        return false;
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
        return $"HibernatingDragon {this.dragonNumber}: Realm={this.realmNumber}, Cave={this.caveNumber}, " +
            $"Rider={this.riderID}, Lair={this.lair}, Energy={this.energy}, WakeDate={this.wakeDate}";
    }
}
