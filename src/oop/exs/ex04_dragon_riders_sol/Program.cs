using System;

public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("=== Step 1: Creating North and South Registries ===");
        DragonRegistry north = new DragonRegistry(6);
        DragonRegistry south = new DragonRegistry(6);

        FireDragon f1 = new FireDragon(1, 10, 101, "Rider-Rami", new Coordinates(0, 0), 100);
        FireDragon f2 = new FireDragon(1, 10, 102, "Rider-Sami", new Coordinates(100, 100), 80);
        FireDragon f3 = new FireDragon(1, 10, 103, "Rider-Adel", new Coordinates(200, 200), 60);

        HibernatingDragon h1 = new HibernatingDragon(1, 20, 201, "Rider-Huda", new Coordinates(50, 50), new Date(1, 3, 2026));
        HibernatingDragon h2 = new HibernatingDragon(1, 20, 202, "Rider-Nour", new Coordinates(60, 60), new Date(15, 5, 2027));

        AlphaDragon a1 = new AlphaDragon(1, 30, 301, "Rider-Kareem", new Coordinates(500, 500), "BlazeClan", 4, 200);
        AlphaDragon a2 = new AlphaDragon(1, 30, 302, "Rider-Tariq", new Coordinates(600, 600), "StormClan", 4, 150);

        a1.AddMember(f1);
        a1.AddMember(f2);
        a2.AddMember(f3);

        north.Add(f1);
        north.Add(f2);
        north.Add(h1);
        north.Add(a1);

        south.Add(f2); // Shared dragon
        south.Add(f3);
        south.Add(h1); // Shared dragon
        south.Add(h2);
        south.Add(a2);

        Console.WriteLine("=== Step 2: Merging into Valley Registry ===");
        DragonRegistry valley = north.Merge(south);
        Console.WriteLine(valley.ToString());

        Console.WriteLine("=== Step 3: Feeding All Dragons (+30) ===");
        valley.FeedAll(30);
        a1.Refuel(150);
        a2.Refuel(80);
        Console.WriteLine("Total Energy: " + valley.TotalEnergy());

        Console.WriteLine("=== Step 4: Sending FireDragons on Flights ===");
        f1.FlyTo(new Coordinates(60, 80));    // Distance = 100 -> energy = 30 - 100 = -70 (Critical)
        f2.FlyTo(new Coordinates(130, 140));  // Distance = 50  -> energy = 30 - 50 = -20  (Warning)
        f3.FlyTo(new Coordinates(203, 204));  // Distance = 5   -> energy = 30 - 5 = 25    (Safe)

        Console.WriteLine("=== Step 5: Danger Levels & Suggestions ===");
        BasicDragon[] inDanger = valley.DangerDragons();
        Console.WriteLine("Dragons in danger count: " + inDanger.Length);
        valley.PrintSuggestions();

        Console.WriteLine("=== Step 6: Rescuing FireDragons in Danger ===");
        a1.TransferEnergy(80, f1);
        a1.TransferEnergy(30, f2);
        Console.WriteLine("f1 DangerLevel after rescue: " + f1.DangerLevel());
        Console.WriteLine("f2 DangerLevel after rescue: " + f2.DangerLevel());

        Console.WriteLine("=== Step 7: Volcano Alert! Waking Hibernating Dragons ===");
        Date today = new Date(20, 10, 2026);
        bool woke1 = h1.WakeUp(today, true);
        bool woke2 = h2.WakeUp(today, true);
        Console.WriteLine($"h1 woke up? {woke1}, h2 woke up? {woke2}");

        Console.WriteLine("=== Step 8: Sorted AlphaDragons and HibernatingDragons ===");
        AlphaDragon[] alphas = valley.GetAlphasByPower();
        for (int i = 0; i < alphas.Length; i++)
        {
            Console.WriteLine(alphas[i].ToString());
        }

        Console.WriteLine("=== Step 9: Removing Awakened Dragons ===");
        if (woke1)
        {
            valley.Remove(h1.GetDragonNumber());
        }
        if (woke2)
        {
            valley.Remove(h2.GetDragonNumber());
        }
        Console.WriteLine(valley.ToString());
    }
}
