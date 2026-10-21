using System;

public class Program
{
    public static void Main(string[] args)
    {
        // Exercise 4: Inheritance applied on Employee, Technician and UnionMember
        Employee e1 = new Employee("301", "Nour", 6);
        Technician t1 = new Technician("101", "Rami", 7, 110);
        Technician t2 = new Technician("102", "Sami", 40); // Second constructor via base(id, name)
        UnionMember u1 = new UnionMember("201", "Huda", 8, 5);

        // Inherited operations on derived objects
        t1.AddSeniorityYear();
        Console.WriteLine("Technician name (inherited GetName): " + t1.GetName());
        u1.SetUnionYears(3);
        Console.WriteLine("Technician 1: " + t1.ToString());
        Console.WriteLine("Technician 2: " + t2.ToString());
        Console.WriteLine("UnionMember 1: " + u1.ToString());
        Console.WriteLine("Employee 1: " + e1.ToString());

        // Exercise 5: Supervisor with a team of up to 15 employees
        Supervisor s1 = new Supervisor("401", "Kareem", 10);
        s1.AddEmployeeToTeam(e1);
        s1.AddEmployeeToTeam(t1);
        s1.AddEmployeeToTeam(u1);
        Console.WriteLine("Supervisor after adds: " + s1.ToString());

        Employee[] readyTeam = new Employee[] { e1, t2, null, u1 };
        Supervisor s2 = new Supervisor("402", "Adel", 12, readyTeam);
        Console.WriteLine("Supervisor 2 (second constructor): " + s2.ToString());

        // Bonus seniority for a team member
        bool granted = s1.TransferBonusSeniority(t1);
        bool rejected = s1.TransferBonusSeniority(t2); // Not in s1's team
        Console.WriteLine($"Bonus granted to t1? {granted}, to t2? {rejected}");
        Console.WriteLine("Technician 1 after bonus: " + t1.ToString());
    }
}
