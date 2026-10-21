using System;

public class Program
{
    public static void Main(string[] args)
    {
        // Exercise 1: ScoutShip without inheritance
        ScoutShip sc1 = new ScoutShip(1, 10, 101, "Cap-Rami"); // First constructor
        ScoutShip sc2 = new ScoutShip(1, 10, 102, "Cap-Sami", 50); // Second constructor
        sc1.Refuel(40);
        Console.WriteLine("sc1 consumes 30: " + sc1.Consume(30)); // Success
        Console.WriteLine("sc1 consumes 30 again: " + sc1.Consume(30)); // Fails: would drop under -0
        sc2.Refuel(20);
        Console.WriteLine("sc2 consumes 60: " + sc2.Consume(60)); // Success: uses emergency reserve (fuel = -40)
        Console.WriteLine("sc1: " + sc1.ToString());
        Console.WriteLine("sc2: " + sc2.ToString());

        // Exercise 2: HibernationShip without inheritance
        HibernationShip h1 = new HibernationShip(1, 20, 201, "Cap-Huda", new Date(15, 6, 2028));
        h1.Refuel(100);
        Date early = new Date(1, 1, 2027);
        Date onTime = new Date(15, 6, 2028);
        Console.WriteLine("Withdraw before arrival: " + h1.WithdrawAllFuel(early)); // False
        Console.WriteLine("Withdraw on arrival date: " + h1.WithdrawAllFuel(onTime)); // True
        Console.WriteLine("h1: " + h1.ToString());

        // Exercise 3: BasicShip with the shared members only
        BasicShip b1 = new BasicShip(1, 30, 301, "Cap-Kareem");
        b1.Refuel(80);
        Console.WriteLine("b1: " + b1.ToString());
    }
}
