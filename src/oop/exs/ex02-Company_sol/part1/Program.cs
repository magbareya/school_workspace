using System;

public class Program
{
    public static void Main(string[] args)
    {
        // Exercise 1: Technician without inheritance
        Technician t1 = new Technician("101", "Rami", 7, 110);
        Technician t2 = new Technician("102", "Sami", 40); // Second constructor: seniority = 0
        t1.AddSeniorityYear();
        t1.SetComputers(-5); // Invalid: must be ignored
        t2.SetComputers(25);
        Console.WriteLine("Technician 1: " + t1.ToString());
        Console.WriteLine("Technician 2: " + t2.ToString());

        // Exercise 2: UnionMember without inheritance
        UnionMember u1 = new UnionMember("201", "Huda", 8, 5);
        u1.AddSeniorityYear();
        u1.SetUnionYears(10); // Invalid: greater than seniority, must be ignored
        Console.WriteLine("UnionMember 1: " + u1.ToString());

        // Exercise 3: Employee with the shared members only
        Employee e1 = new Employee("301", "Nour", 6);
        Employee e2 = new Employee("302", "Lina"); // Second constructor: seniority = 0
        e2.AddSeniorityYear();
        e1.SetName("Nour-A");
        Console.WriteLine("Employee 1: " + e1.ToString());
        Console.WriteLine("Employee 2: " + e2.ToString());
    }
}
