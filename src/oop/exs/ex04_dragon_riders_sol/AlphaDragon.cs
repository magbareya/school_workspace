using System;

public class AlphaDragon : BasicDragon, IComparable
{
    private string clanName;
    private double emberReserve;
    private FireDragon[] pack;
    private int packCount;

    public AlphaDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair, string clanName, int maxPackSize)
        : this(realmNumber, caveNumber, dragonNumber, riderID, lair, clanName, maxPackSize, 0)
    {
    }

    public AlphaDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair, string clanName, int maxPackSize, double emberReserve)
        : base(realmNumber, caveNumber, dragonNumber, riderID, lair)
    {
        this.clanName = clanName;
        this.emberReserve = 0;
        this.SetEmberReserve(emberReserve);
        this.pack = new FireDragon[maxPackSize];
        this.packCount = 0;
        this.dragonType = "Alpha";
    }

    public string GetClanName()
    {
        return this.clanName;
    }

    public void SetClanName(string clanName)
    {
        this.clanName = clanName;
    }

    public double GetEmberReserve()
    {
        return this.emberReserve;
    }

    public void SetEmberReserve(double emberReserve)
    {
        if (emberReserve >= 0)
        {
            this.emberReserve = emberReserve;
        }
    }

    public int GetPackCount()
    {
        return this.packCount;
    }

    public double GetPowerPotential()
    {
        return this.energy + this.emberReserve;
    }

    public bool Consume(double amount)
    {
        if (amount > 0)
        {
            if (this.energy - amount >= -this.emberReserve)
            {
                this.energy -= amount;
                return true;
            }
        }
        return false;
    }

    public override bool UseEnergy(object o)
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

    private int FindMemberIndex(int dragonNum)
    {
        for (int i = 0; i < this.packCount; i++)
        {
            if (this.pack[i].GetDragonNumber() == dragonNum)
            {
                return i;
            }
        }
        return -1;
    }

    public bool AddMember(FireDragon d)
    {
        if (d != null && this.packCount < this.pack.Length && this.FindMemberIndex(d.GetDragonNumber()) == -1)
        {
            this.pack[this.packCount] = d;
            this.packCount++;
            return true;
        }
        return false;
    }

    public FireDragon FindMember(int dragonNum)
    {
        int idx = this.FindMemberIndex(dragonNum);
        if (idx != -1)
        {
            return this.pack[idx];
        }
        return null;
    }

    public bool RemoveMember(int dragonNum)
    {
        int idx = this.FindMemberIndex(dragonNum);
        if (idx == -1)
        {
            return false;
        }
        for (int i = idx; i < this.packCount - 1; i++)
        {
            this.pack[i] = this.pack[i + 1];
        }
        this.pack[this.packCount - 1] = null;
        this.packCount--;
        return true;
    }

    public bool TransferEnergy(double amount, FireDragon target)
    {
        if (target != null)
        {
            FireDragon found = this.FindMember(target.GetDragonNumber());
            if (found == target && amount > 0)
            {
                if (this.Consume(amount))
                {
                    target.Refuel(amount);
                    return true;
                }
            }
        }
        return false;
    }

    public override bool IsInDanger()
    {
        return this.emberReserve > 0 && this.energy <= -0.9 * this.emberReserve;
    }

    public override string DangerLevel()
    {
        if (this.IsInDanger())
        {
            return "Critical";
        }
        if (this.energy < 0)
        {
            return "Warning";
        }
        for (int i = 0; i < this.packCount; i++)
        {
            if (this.pack[i].DangerLevel() == "Critical")
            {
                return "Warning";
            }
        }
        return "Safe";
    }

    public bool HasCriticalMember()
    {
        for (int i = 0; i < this.packCount; i++)
        {
            if (this.pack[i].DangerLevel() == "Critical")
            {
                return true;
            }
        }
        return false;
    }

    public string RescueSuggestion()
    {
        return $"AlphaDragon {this.dragonNumber} (Clan {this.clanName}) needs emergency support for its pack!";
    }

    public int CompareTo(object obj)
    {
        if (obj == null || !(obj is AlphaDragon))
        {
            return 1;
        }
        AlphaDragon other = (AlphaDragon)obj;
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
        return base.ToString() + $", Clan:{this.clanName}, Members:{this.packCount}, EmberReserve:{this.emberReserve}";
    }
}
