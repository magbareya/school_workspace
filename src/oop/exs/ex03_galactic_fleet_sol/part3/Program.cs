using System;

public class Program
{
    public static void Main(string[] args)
    {
        FleetControl control = new FleetControl(6);

        ScoutShip sc1 = new ScoutShip(1, 10, 101, "Cap-Rami", 50);
        ScoutShip sc2 = new ScoutShip(1, 10, 102, "Cap-Sami", 30);
        HibernationShip h1 = new HibernationShip(1, 20, 201, "Cap-Huda", new Date(15, 6, 2028));
        MotherShip m1 = new MotherShip(1, 30, 301, "Cap-Kareem", "Orion", 200);

        sc1.Refuel(40);
        sc1.Consume(70.0); // fuel = -30, in danger
        h1.Refuel(100); // fuel = 100, not in danger
        m1.Refuel(300);

        // Exercise 6: Add + ToString (each ship describes itself polymorphically)
        control.Add(sc1);
        control.Add(sc2);
        control.Add(h1);
        control.Add(m1);
        Console.WriteLine(control.ToString());

        // Exercise 7: DangerShips via virtual/override IsInDanger
        Console.WriteLine("--- Danger Ships ---");
        BasicShip[] inDanger = control.DangerShips();
        for (int i = 0; i < inDanger.Length; i++)
        {
            Console.WriteLine(inDanger[i].ToString());
        }

        // Exercise 8: protected shipType and base.ToString chain (visible in output above)

        // Exercise 9: subclass-only operations used from subclass variables
        Console.WriteLine("--- Subclass-only operations ---");
        Console.WriteLine("sc1 LoanSuggestion: " + sc1.LoanSuggestion());
        Console.WriteLine("h1 ZeroFuel: " + h1.ZeroFuel());
        // Note: calling sc1.LoanSuggestion() through a BasicShip variable is a compile error:
        // BasicShip basic = sc1; basic.LoanSuggestion(); // does not compile

        // Exercise 10: PrintSuggestions using 'is' and downcasting
        Console.WriteLine("--- Suggestions (is) ---");
        control.PrintSuggestions();

        // Exercise 11: PrintSuggestions2 using 'as'
        Console.WriteLine("--- Suggestions (as) ---");
        control.PrintSuggestions2();

        // Exercise 12: RefuelAll
        Console.WriteLine("RefuelAll(+50) count: " + control.RefuelAll(50));
        Console.WriteLine("RefuelAll(-10) count: " + control.RefuelAll(-10));

        // Exercise 13: Equals + duplicate rejection in Add
        ScoutShip sc1Duplicate = new ScoutShip(1, 10, 101, "Cap-Other", 10);
        Console.WriteLine("sc1 equals sc1Duplicate: " + sc1.Equals(sc1Duplicate)); // True: same fleet/base/ship numbers
        Console.WriteLine("Add duplicate: " + control.Add(sc1Duplicate)); // False: rejected
        Console.WriteLine("Add null: " + control.Add(null)); // False
    }
}
