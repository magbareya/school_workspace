using System;

public class Program
{
    public static void Main(string[] args)
    {
        FleetControl control = new FleetControl(8);

        ScoutShip sc1 = new ScoutShip(1, 10, 101, "Cap-Rami", 50);
        ScoutShip sc2 = new ScoutShip(1, 10, 102, "Cap-Sami", 30);

        HibernationShip h1 = new HibernationShip(1, 20, 201, "Cap-Huda", new Date(15, 6, 2028));
        HibernationShip h2 = new HibernationShip(1, 20, 202, "Cap-Nour", new Date(1, 1, 2027));

        MotherShip m1 = new MotherShip(1, 30, 301, "Cap-Kareem", "Orion", 200);
        MotherShip m2 = new MotherShip(1, 30, 302, "Cap-Adel", "Vega", 100);

        sc1.Refuel(40);
        sc1.Consume(70.0); // Now fuel = -30 (in danger)

        h1.Refuel(100);
        // h2 remains at 0 fuel (in danger)

        m1.Refuel(300);
        m2.Consume(95.0); // Uses 95% of emergency reserve (in danger)

        control.Add(sc1);
        control.Add(sc2);
        control.Add(h1);
        control.Add(h2);
        control.Add(m1);
        control.Add(m2);

        Console.WriteLine(control.ToString());

        Console.WriteLine("--- Danger Ships ---");
        BasicShip[] inDanger = control.DangerShips();
        for (int i = 0; i < inDanger.Length; i++)
        {
            Console.WriteLine(inDanger[i].ToString());
        }

        Console.WriteLine("--- Suggestions ---");
        control.PrintSuggestions();

        Console.WriteLine("--- MotherShips Ordered By Power ---");
        MotherShip[] mothers = control.GetMotherShipsByPower();
        for (int i = 0; i < mothers.Length; i++)
        {
            Console.WriteLine(mothers[i].ToString());
        }

        Console.WriteLine("--- HibernationShips Ordered By Arrival Date ---");
        HibernationShip[] hibs = control.GetHibernationByArrivalDate();
        for (int i = 0; i < hibs.Length; i++)
        {
            Console.WriteLine(hibs[i].ToString());
        }
    }
}
