using System;

public class DragonRegistry
{
    private BasicDragon[] dragons;
    private int count;

    public DragonRegistry(int maxDragons)
    {
        this.dragons = new BasicDragon[maxDragons];
        this.count = 0;
    }

    public int Count()
    {
        return this.count;
    }

    private int FindIndex(int dragonNum)
    {
        for (int i = 0; i < this.count; i++)
        {
            if (this.dragons[i].GetDragonNumber() == dragonNum)
            {
                return i;
            }
        }
        return -1;
    }

    public bool Add(BasicDragon d)
    {
        if (d == null || this.count >= this.dragons.Length)
        {
            return false;
        }
        for (int i = 0; i < this.count; i++)
        {
            if (this.dragons[i].Equals(d))
            {
                return false;
            }
        }
        this.dragons[this.count] = d;
        this.count++;
        return true;
    }

    public BasicDragon Find(int dragonNum)
    {
        int idx = this.FindIndex(dragonNum);
        if (idx != -1)
        {
            return this.dragons[idx];
        }
        return null;
    }

    public bool Remove(int dragonNum)
    {
        int idx = this.FindIndex(dragonNum);
        if (idx == -1)
        {
            return false;
        }
        for (int i = idx; i < this.count - 1; i++)
        {
            this.dragons[i] = this.dragons[i + 1];
        }
        this.dragons[this.count - 1] = null;
        this.count--;
        return true;
    }

    public BasicDragon[] DangerDragons()
    {
        int dangerCount = 0;
        for (int i = 0; i < this.count; i++)
        {
            if (this.dragons[i].IsInDanger())
            {
                dangerCount++;
            }
        }
        BasicDragon[] result = new BasicDragon[dangerCount];
        int index = 0;
        for (int i = 0; i < this.count; i++)
        {
            if (this.dragons[i].IsInDanger())
            {
                result[index] = this.dragons[i];
                index++;
            }
        }
        return result;
    }

    public void PrintSuggestions()
    {
        for (int i = 0; i < this.count; i++)
        {
            BasicDragon d = this.dragons[i];
            if (d is HibernatingDragon)
            {
                HibernatingDragon h = (HibernatingDragon)d;
                if (h.IsEmpty())
                {
                    Console.WriteLine($"Warning: HibernatingDragon {h.GetDragonNumber()} has zero energy!");
                }
            }
            else if (d is FireDragon)
            {
                FireDragon f = (FireDragon)d;
                if (f.IsInDanger())
                {
                    Console.WriteLine(f.RescueSuggestion());
                }
            }
            else if (d is AlphaDragon)
            {
                AlphaDragon a = (AlphaDragon)d;
                if (a.IsInDanger() || a.HasCriticalMember())
                {
                    Console.WriteLine(a.RescueSuggestion());
                }
            }
        }
    }

    // Comparison of approaches:
    // 1. 'is' checks runtime compatibility and returns bool; 'as' attempts conversion and returns null if incompatible;
    //    direct cast '(FireDragon)d' throws InvalidCastException if incompatible.
    // 2. If 'd' is null: 'is' returns false, 'as' returns null, and direct cast returns null.
    public void PrintSuggestions2()
    {
        for (int i = 0; i < this.count; i++)
        {
            BasicDragon d = this.dragons[i];
            HibernatingDragon h = d as HibernatingDragon;
            if (h != null && h.IsEmpty())
            {
                Console.WriteLine($"Warning: HibernatingDragon {h.GetDragonNumber()} has zero energy!");
            }
            FireDragon f = d as FireDragon;
            if (f != null && f.IsInDanger())
            {
                Console.WriteLine(f.RescueSuggestion());
            }
            AlphaDragon a = d as AlphaDragon;
            if (a != null && (a.IsInDanger() || a.HasCriticalMember()))
            {
                Console.WriteLine(a.RescueSuggestion());
            }
        }
    }

    public int FeedAll(double amount)
    {
        int fed = 0;
        for (int i = 0; i < this.count; i++)
        {
            if (this.dragons[i].Refuel(amount))
            {
                fed++;
            }
        }
        return fed;
    }

    public double TotalEnergy()
    {
        double sum = 0;
        for (int i = 0; i < this.count; i++)
        {
            sum += this.dragons[i].GetEnergy();
        }
        return sum;
    }

    public DragonRegistry Merge(DragonRegistry other)
    {
        int otherLen = (other != null) ? other.dragons.Length : 0;
        DragonRegistry merged = new DragonRegistry(this.dragons.Length + otherLen);
        for (int i = 0; i < this.count; i++)
        {
            merged.Add(this.dragons[i]);
        }
        if (other != null)
        {
            for (int i = 0; i < other.count; i++)
            {
                merged.Add(other.dragons[i]);
            }
        }
        return merged;
    }

    public override string ToString()
    {
        string result = $"=== DragonRegistry ({this.count} dragons) ===\n";
        for (int i = 0; i < this.count; i++)
        {
            result += this.dragons[i].ToString() + "\n";
        }
        return result;
    }
}
