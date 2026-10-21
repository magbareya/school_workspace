using System;

public class FleetControl
{
    private BasicShip[] ships;

    public FleetControl(int maxShips)
    {
        this.ships = new BasicShip[maxShips];
    }

    public BasicShip[] GetShips()
    {
        return this.ships;
    }

    public void SetShips(BasicShip[] ships)
    {
        this.ships = ships;
    }

    public bool Add(BasicShip ship)
    {
        if (ship == null)
        {
            return false;
        }
        for (int i = 0; i < this.ships.Length; i++)
        {
            if (this.ships[i] != null && this.ships[i].Equals(ship))
            {
                return false;
            }
        }
        for (int i = 0; i < this.ships.Length; i++)
        {
            if (this.ships[i] == null)
            {
                this.ships[i] = ship;
                return true;
            }
        }
        return false;
    }

    public BasicShip[] DangerShips()
    {
        int count = 0;
        for (int i = 0; i < this.ships.Length; i++)
        {
            if (this.ships[i] != null && this.ships[i].IsInDanger())
            {
                count++;
            }
        }
        BasicShip[] result = new BasicShip[count];
        int index = 0;
        for (int i = 0; i < this.ships.Length; i++)
        {
            if (this.ships[i] != null && this.ships[i].IsInDanger())
            {
                result[index] = this.ships[i];
                index++;
            }
        }
        return result;
    }

    public void PrintSuggestions()
    {
        for (int i = 0; i < this.ships.Length; i++)
        {
            BasicShip s = this.ships[i];
            if (s != null)
            {
                if (s is HibernationShip)
                {
                    HibernationShip h = (HibernationShip)s;
                    if (h.ZeroFuel())
                    {
                        Console.WriteLine($"Warning: HibernationShip {h.GetShipNumber()} has zero fuel!");
                    }
                }
                else if (s is ScoutShip)
                {
                    ScoutShip sc = (ScoutShip)s;
                    Console.WriteLine(sc.LoanSuggestion());
                }
                else if (s is MotherShip)
                {
                    MotherShip m = (MotherShip)s;
                    Console.WriteLine(m.LoanSuggestion());
                }
            }
        }
    }

    // Comparison of approaches:
    // 1. 'is' checks runtime compatibility and returns bool; 'as' attempts conversion and returns null if incompatible;
    //    direct cast '(HibernationShip)ship' throws InvalidCastException if incompatible.
    // 2. If 'ship' is null: 'is' returns false, 'as' returns null, and direct cast returns null.
    public void PrintSuggestions2()
    {
        for (int i = 0; i < this.ships.Length; i++)
        {
            BasicShip s = this.ships[i];
            HibernationShip h = s as HibernationShip;
            if (h != null)
            {
                if (h.ZeroFuel())
                {
                    Console.WriteLine($"Warning: HibernationShip {h.GetShipNumber()} has zero fuel!");
                }
            }
            ScoutShip sc = s as ScoutShip;
            if (sc != null)
            {
                Console.WriteLine(sc.LoanSuggestion());
            }
            MotherShip m = s as MotherShip;
            if (m != null)
            {
                Console.WriteLine(m.LoanSuggestion());
            }
        }
    }

    public int RefuelAll(double amount)
    {
        int count = 0;
        for (int i = 0; i < this.ships.Length; i++)
        {
            if (this.ships[i] != null && this.ships[i].Refuel(amount))
            {
                count++;
            }
        }
        return count;
    }

    public override string ToString()
    {
        string result = "=== FleetControl Ships ===\n";
        for (int i = 0; i < this.ships.Length; i++)
        {
            if (this.ships[i] != null)
            {
                result += this.ships[i].ToString() + "\n";
            }
        }
        return result;
    }
}
