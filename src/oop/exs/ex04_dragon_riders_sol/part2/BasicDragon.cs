using System;

public class BasicDragon
{
    protected int realmNumber;
    protected int caveNumber;
    protected int dragonNumber;
    protected string riderID;
    protected Coordinates lair;
    protected double energy;

    public BasicDragon(int realmNumber, int caveNumber, int dragonNumber, string riderID, Coordinates lair)
    {
        this.realmNumber = realmNumber;
        this.caveNumber = caveNumber;
        this.dragonNumber = dragonNumber;
        this.riderID = riderID;
        this.SetLair(lair);
        this.energy = 0;
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

    public bool Refuel(double amount)
    {
        if (amount > 0)
        {
            this.energy += amount;
            return true;
        }
        return false;
    }

    public override string ToString()
    {
        return $"Dragon {this.dragonNumber}: Realm={this.realmNumber}, Cave={this.caveNumber}, " +
            $"Rider={this.riderID}, Lair={this.lair}, Energy={this.energy}";
    }
}
