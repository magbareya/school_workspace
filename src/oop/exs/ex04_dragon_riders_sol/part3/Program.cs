using System;

public class Program
{
    public static void Main(string[] args)
    {
        // Exercise 8: DragonRegistry with Add/Find/Remove/Count
        DragonRegistry north = new DragonRegistry(6);
        FireDragon f1 = new FireDragon(1, 10, 101, "Rider-Rami", new Coordinates(0, 0), 100);
        FireDragon f2 = new FireDragon(1, 10, 102, "Rider-Sami", new Coordinates(100, 100), 80);
        HibernatingDragon h1 = new HibernatingDragon(1, 20, 201, "Rider-Huda", new Coordinates(50, 50), new Date(1, 3, 2026));
        AlphaDragon a1 = new AlphaDragon(1, 30, 301, "Rider-Kareem", new Coordinates(500, 500), "BlazeClan", 4, 200);
        HibernatingDragon h2 = new HibernatingDragon(1, 20, 202, "Rider-Nour", new Coordinates(60, 60), new Date(15, 5, 2027));

        north.Add(f1);
        north.Add(f2);
        north.Add(h1);
        north.Add(a1);
        north.Add(h2);
        Console.WriteLine("Count: " + north.Count());
        Console.WriteLine("Find 201: " + north.Find(201).ToString());
        Console.WriteLine("Remove 102: " + north.Remove(102)); // Shifts the following dragons left
        Console.WriteLine("Registry after remove:\n" + north.ToString());

        // Exercise 9: virtual/override IsInDanger and DangerLevel
        f1.Refuel(30);
        f1.Consume(100.0); // energy = -70 (Critical for FireDragon)
        f2.Refuel(50);
        f2.Consume(60.0); // energy = -10 (Warning for FireDragon)
        a1.AddMember(f1);
        Console.WriteLine("f1 DangerLevel: " + f1.DangerLevel()); // Critical
        Console.WriteLine("f2 DangerLevel: " + f2.DangerLevel()); // Warning
        Console.WriteLine("h1 DangerLevel: " + h1.DangerLevel()); // Critical (no energy)
        Console.WriteLine("a1 DangerLevel: " + a1.DangerLevel()); // Warning (a pack member is Critical)
        BasicDragon[] inDanger = north.DangerDragons();
        Console.WriteLine("Dragons in danger: " + inDanger.Length);

        // Exercise 10: protected dragonType + base.ToString chain (visible in the ToString output above)

        // Exercise 11: subclass-only operations
        Console.WriteLine("h1 IsEmpty: " + h1.IsEmpty());
        Console.WriteLine("f2 RescueSuggestion: " + f2.RescueSuggestion());

        // Exercise 12: PrintSuggestions using 'is'
        Console.WriteLine("--- Suggestions (is) ---");
        north.PrintSuggestions();

        // Exercise 13: PrintSuggestions2 using 'as'
        Console.WriteLine("--- Suggestions (as) ---");
        north.PrintSuggestions2();

        // Exercise 14: FeedAll and TotalEnergy
        Console.WriteLine("TotalEnergy before: " + north.TotalEnergy());
        Console.WriteLine("Fed with +25: " + north.FeedAll(25));
        Console.WriteLine("Fed with -10: " + north.FeedAll(-10));
        Console.WriteLine("TotalEnergy after: " + north.TotalEnergy());

        // Exercise 15: Equals + duplicate rejection in Add
        FireDragon f1Duplicate = new FireDragon(1, 10, 101, "Rider-Other", new Coordinates(10, 10), 20);
        Console.WriteLine("f1 equals f1Duplicate: " + f1.Equals(f1Duplicate)); // True: same realm/cave/dragon numbers
        Console.WriteLine("Add duplicate: " + north.Add(f1Duplicate)); // False: rejected

        // Exercise 16: Merge two registries without duplicates
        DragonRegistry south = new DragonRegistry(6);
        south.Add(f1); // Shared dragon
        south.Add(h1); // Shared dragon
        FireDragon f3 = new FireDragon(1, 10, 103, "Rider-Adel", new Coordinates(200, 200), 60);
        south.Add(f3);
        DragonRegistry valley = north.Merge(south);
        Console.WriteLine("Merged count: " + valley.Count()); // 4 + 1 (f3 only, f1/h1 deduplicated)
        Console.WriteLine(valley.ToString());
    }
}
