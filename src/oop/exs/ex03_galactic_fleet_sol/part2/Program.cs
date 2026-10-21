using System;

public class Program
{
    public static void Main(string[] args)
    {
        // Exercise 4: Inheritance applied on BasicShip, ScoutShip and HibernationShip
        ScoutShip sc1 = new ScoutShip(1, 10, 101, "Cap-Rami", 50);
        HibernationShip h1 = new HibernationShip(1, 20, 201, "Cap-Huda", new Date(15, 6, 2028));

        sc1.Refuel(40);
        Console.WriteLine("sc1 consumes 70: " + sc1.Consume(70)); // Uses emergency reserve
        Console.WriteLine("Inherited GetFuel on sc1: " + sc1.GetFuel());
        h1.Refuel(100);
        Console.WriteLine("h1 withdraw at arrival: " + h1.WithdrawAllFuel(new Date(15, 6, 2028)));
        Console.WriteLine("sc1: " + sc1.ToString());
        Console.WriteLine("h1: " + h1.ToString());

        // Exercise 5: MotherShip with TransferFuel
        MotherShip m1 = new MotherShip(1, 30, 301, "Cap-Kareem", "Orion", 200);
        m1.Refuel(300);
        ScoutShip sc2 = new ScoutShip(1, 10, 102, "Cap-Sami");

        Console.WriteLine("Transfer 80 to sc2: " + m1.TransferFuel(80, sc2)); // Success
        Console.WriteLine("Transfer -5 to sc2: " + m1.TransferFuel(-5, sc2)); // Fails: non-positive amount
        Console.WriteLine("Transfer 5000 to sc2: " + m1.TransferFuel(5000, sc2)); // Fails: exceeds allowed consumption
        Console.WriteLine("Transfer 10 to null: " + m1.TransferFuel(10, null)); // Fails: null target
        Console.WriteLine("m1: " + m1.ToString());
        Console.WriteLine("sc2: " + sc2.ToString());
    }
}
