using System;

public class Program
{
    public static void Main(string[] args)
    {
        // Exercise 1: Coordinates with Clamp helper
        Coordinates p1 = new Coordinates(0, 0);
        Coordinates p2 = new Coordinates(3, 4);
        Coordinates pEdge = new Coordinates(0, 500);
        Coordinates pOut = new Coordinates(1500, -20); // Corrected to (1000, 0)
        Console.WriteLine("pOut after clamping: " + pOut.ToString());
        pEdge.SetX(2000); // Corrected to 1000
        Console.WriteLine("pEdge after SetX(2000): " + pEdge.ToString());
        Console.WriteLine("Distance (0,0)-(3,4): " + p1.DistanceTo(p2)); // 5
        Console.WriteLine("pEdge on map edge: " + pEdge.IsOnMapEdge());
        Coordinates cornerA = new Coordinates(10, 10);
        Coordinates cornerB = new Coordinates(100, 100);
        Console.WriteLine("(50,50) inside: " + new Coordinates(50, 50).IsInside(cornerA, cornerB));
        Console.WriteLine("(5,50) inside: " + new Coordinates(5, 50).IsInside(cornerA, cornerB));
        Console.WriteLine("(10,10) inside: " + new Coordinates(10, 10).IsInside(cornerA, cornerB));
        Console.WriteLine("(50,50) inside (reversed corners): " + new Coordinates(50, 50).IsInside(cornerB, cornerA));

        // Exercise 2: FireDragon without inheritance
        FireDragon f1 = new FireDragon(1, 10, 101, "Rider-Rami", new Coordinates(0, 0));
        FireDragon f2 = new FireDragon(1, 10, 102, "Rider-Sami", new Coordinates(100, 100), 50);
        Console.WriteLine("f1: " + f1.ToString());
        Console.WriteLine("f2: " + f2.ToString());
        f1.Refuel(100);
        Console.WriteLine("f1 consume 30: " + f1.Consume(30)); // True
        Console.WriteLine("f1 consume 80: " + f1.Consume(80)); // False
        Console.WriteLine("f1 consume -5: " + f1.Consume(-5)); // False
        Console.WriteLine("f2 consume 40: " + f2.Consume(40)); // True
        Console.WriteLine("f2 consume 20: " + f2.Consume(20)); // True
        f1.SetEmberReserve(30);
        Console.WriteLine("f1 FlyTo(0,30): " + f1.FlyTo(new Coordinates(0, 30))); // True (cost 30)
        Console.WriteLine("f1 FlyTo(null): " + f1.FlyTo(null)); // False

        // Exercise 3: flight log with shifting
        FireDragon f3 = new FireDragon(1, 10, 103, "Rider-Adel", new Coordinates(0, 0));
        f3.Refuel(1000);
        for (int i = 1; i <= 7; i++)
        {
            f3.Consume(10.0 * i);
            double[] log = f3.GetLog();
            Console.WriteLine("After flight " + i + ": " + string.Join(", ", log));
        }
        Console.WriteLine("LongestFlight: " + f3.LongestFlight()); // 70
        Console.WriteLine("CountFlightsOver(35): " + f3.CountFlightsOver(35)); // 4 (40,50,60,70)
        Console.WriteLine("HasFlown(40): " + f3.HasFlown(40)); // True
        Console.WriteLine("HasFlown(10): " + f3.HasFlown(10)); // False (shifted out)

        // Exercise 4: HibernatingDragon without inheritance
        HibernatingDragon h1 = new HibernatingDragon(1, 20, 201, "Rider-Huda", new Coordinates(50, 50), new Date(1, 3, 2026));
        HibernatingDragon h2 = new HibernatingDragon(1, 20, 202, "Rider-Nour", new Coordinates(60, 60), new Date(15, 5, 2027));
        HibernatingDragon h3 = new HibernatingDragon(1, 20, 203, "Rider-Ali", new Coordinates(70, 70), new Date(15, 5, 2027));
        h1.Refuel(80);
        h2.Refuel(80);
        Console.WriteLine("h1 before date, no alert: " + h1.WakeUp(new Date(1, 1, 2026), false)); // False
        Console.WriteLine("h1 after date: " + h1.WakeUp(new Date(2, 3, 2026), false)); // True
        Console.WriteLine("h2 alert with energy: " + h2.WakeUp(new Date(1, 1, 2026), true)); // True
        h3.Refuel(0); // no energy
        Console.WriteLine("h3 alert without energy: " + h3.WakeUp(new Date(1, 1, 2026), true)); // False
        Console.WriteLine("h1: " + h1.ToString());
        Console.WriteLine("h2: " + h2.ToString());
        Console.WriteLine("h3: " + h3.ToString());

        // Exercise 5: BasicDragon with the shared members only
        BasicDragon b1 = new BasicDragon(1, 30, 301, "Rider-Kareem", new Coordinates(500, 500));
        b1.Refuel(60);
        Console.WriteLine("b1: " + b1.ToString());
        b1.SetLair(new Coordinates(600, 600));
        Console.WriteLine("b1 lair after SetLair: " + b1.GetLair().ToString());
    }
}
