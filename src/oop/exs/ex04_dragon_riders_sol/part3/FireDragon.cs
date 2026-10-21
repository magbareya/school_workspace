using System;

public class FireDragon : BasicDragon
{
    private double emberReserve;
    private double[] flightLog;
    private int logCount;

    public FireDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair)
        : this(realmNumber, caveNumber, dragonNumber, riderID, lair, 0)
    {
    }

    public FireDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair, double emberReserve)
        : base(realmNumber, caveNumber, dragonNumber, riderID, lair)
    {
        this.emberReserve = 0;
        this.SetEmberReserve(emberReserve);
        this.flightLog = new double[5];
        this.logCount = 0;
        this.dragonType = "Fire";
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

    public override bool IsInDanger()
    {
        return this.energy < 0;
    }

    public override string DangerLevel()
    {
        if (this.energy < 0)
        {
            if (this.energy <= -0.5 * this.emberReserve)
            {
                return "Critical";
            }
            return "Warning";
        }
        return "Safe";
    }

    public string RescueSuggestion()
    {
        if (this.energy < 0)
        {
            double needed = Math.Ceiling(-this.energy);
            return $"FireDragon {this.dragonNumber} requests energy transfer of {needed} from AlphaDragon";
        }
        return "No help needed";
    }

    public override string ToString()
    {
        return base.ToString() + $", EmberReserve:{this.emberReserve}, Lair:{this.lair}";
    }
}
