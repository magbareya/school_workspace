using System;

public class Program
{
    public static void Main(string[] args)
    {
        // Exercise 6: Inheritance applied on BasicDragon, FireDragon and HibernatingDragon
        FireDragon f1 = new FireDragon(1, 10, 101, "Rider-Rami", new Coordinates(0, 0), 100);
        HibernatingDragon h1 = new HibernatingDragon(1, 20, 201, "Rider-Huda", new Coordinates(50, 50), new Date(1, 3, 2026));

        f1.Refuel(100);
        Console.WriteLine("f1 consume 30: " + f1.Consume(30)); // True
        Console.WriteLine("Inherited GetEnergy on f1: " + f1.GetEnergy()); // 70
        f1.FlyTo(new Coordinates(0, 50)); // cost 50, recorded in the flight log
        Console.WriteLine("f1 HasFlown(50): " + f1.HasFlown(50)); // True
        h1.Refuel(80);
        Console.WriteLine("h1 wakes after date: " + h1.WakeUp(new Date(2, 3, 2026), false)); // True
        Console.WriteLine("f1: " + f1.ToString());
        Console.WriteLine("h1: " + h1.ToString());

        // Exercise 7: AlphaDragon with a FireDragon[] pack
        AlphaDragon a1 = new AlphaDragon(1, 30, 301, "Rider-Kareem", new Coordinates(500, 500), "BlazeClan", 3, 200);
        FireDragon f2 = new FireDragon(1, 10, 102, "Rider-Sami", new Coordinates(100, 100), 80);
        FireDragon f3 = new FireDragon(1, 10, 103, "Rider-Adel", new Coordinates(200, 200), 60);
        FireDragon f4 = new FireDragon(1, 10, 104, "Rider-Tariq", new Coordinates(300, 300), 40);

        a1.Refuel(150);
        Console.WriteLine("Add f1: " + a1.AddMember(f1)); // True
        Console.WriteLine("Add f2: " + a1.AddMember(f2)); // True
        Console.WriteLine("Add f3: " + a1.AddMember(f3)); // True
        Console.WriteLine("Add f4 (full pack): " + a1.AddMember(f4)); // False: pack size 3
        Console.WriteLine("Add f1 again (duplicate): " + a1.AddMember(f1)); // False: already a member
        Console.WriteLine("Add null: " + a1.AddMember(null)); // False

        Console.WriteLine("Find 102: " + a1.FindMember(102).ToString());
        Console.WriteLine("Find 999: " + (a1.FindMember(999) == null ? "null" : "found"));

        a1.Refuel(200);
        Console.WriteLine("Transfer 30 to f2: " + a1.TransferEnergy(30, f2)); // True: member
        Console.WriteLine("Transfer 30 to f4: " + a1.TransferEnergy(30, f4)); // False: not a member
        Console.WriteLine("Transfer -5 to f2: " + a1.TransferEnergy(-5, f2)); // False: non-positive

        Console.WriteLine("Remove 102: " + a1.RemoveMember(102)); // True, members shift left
        Console.WriteLine("Pack count after remove: " + a1.GetPackCount()); // 2
        Console.WriteLine("a1: " + a1.ToString());
    }
}
