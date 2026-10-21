using System;

public class FireDragon
{
    private int realmNumber;
    private int caveNumber;
    private int dragonNumber;
    private string riderID;
    private Coordinates lair;
    private double energy;
    private double emberReserve;
    private double[] flightLog;
    private int logCount;

    public FireDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair)
        : this(realmNumber, caveNumber, dragonNumber, riderID, lair, 0)
    {
    }

    public FireDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair, double emberReserve)
    {
        this.realmNumber = realmNumber;
        this.caveNumber = caveNumber;
        this.dragonNumber = dragonNumber;
        this.riderID = riderID;
        this.SetLair(lair);
        this.energy = 0;
        this.emberReserve = 0;
        this.SetEmberReserve(emberReserve);
        this.flightLog = new double[5];
        this.logCount = 0;
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

    public bool Refuel(double amount)
    {
        if (amount > 0)
        {
            this.energy += amount;
            return true;
        }
        return false;
    }

    private void AddToLog(double amount)
    {
        if (this.logCount < this.flightLog.Length)
        {
            this.flightLog[this.logCount] = amount;
            this.logCount++;
        }
        else
        {
            for (int i = 0; i < this.flightLog.Length - 1; i++)
            {
                this.flightLog[i] = this.flightLog[i + 1];
            }
            this.flightLog[this.flightLog.Length - 1] = amount;
        }
    }

    private bool TrySpend(double amount)
    {
        if (amount > 0)
        {
            if (this.energy - amount >= -this.emberReserve)
            {
                this.energy -= amount;
                this.AddToLog(amount);
                return true;
            }
        }
        return false;
    }

    public bool Consume(double amount)
    {
        return this.TrySpend(amount);
    }

    public bool FlyTo(Coordinates target)
    {
        if (target == null || this.lair == null)
        {
            return false;
        }
        double cost = this.lair.DistanceTo(target);
        return this.TrySpend(cost);
    }

    public double[] GetLog()
    {
        double[] copy = new double[this.logCount];
        for (int i = 0; i < this.logCount; i++)
        {
            copy[i] = this.flightLog[i];
        }
        return copy;
    }

    public double LongestFlight()
    {
        if (this.logCount == 0)
        {
            return 0;
        }
        double max = this.flightLog[0];
        for (int i = 1; i < this.logCount; i++)
        {
            if (this.flightLog[i] > max)
            {
                max = this.flightLog[i];
            }
        }
        return max;
    }

    public int CountFlightsOver(double threshold)
    {
        int count = 0;
        for (int i = 0; i < this.logCount; i++)
        {
            if (this.flightLog[i] > threshold)
            {
                count++;
            }
        }
        return count;
    }

    public bool HasFlown(double amount)
    {
        for (int i = 0; i < this.logCount; i++)
        {
            if (this.flightLog[i] == amount)
            {
                return true;
            }
        }
        return false;
    }

    public override string ToString()
    {
        return $"FireDragon {this.dragonNumber}: Realm={this.realmNumber}, Cave={this.caveNumber}, " +
            $"Rider={this.riderID}, Lair={this.lair}, Energy={this.energy}, EmberReserve={this.emberReserve}";
    }
}
