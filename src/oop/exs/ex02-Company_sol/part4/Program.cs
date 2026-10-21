using System;

public class Program
{
    public static void Main(string[] args)
    {
        Company comp = new Company();

        Employee e1 = new Employee("301", "Nour", 6);
        Technician t1 = new Technician("101", "Rami", 7, 110);
        Technician t2 = new Technician("102", "Sami", 2, 40);
        UnionMember u1 = new UnionMember("201", "Huda", 8, 5);
        Supervisor s1 = new Supervisor("401", "Kareem", 10);
        s1.AddEmployeeToTeam(e1);
        s1.AddEmployeeToTeam(t1);
        s1.AddEmployeeToTeam(u1);

        comp.AddEmployee(e1);
        comp.AddEmployee(t1);
        comp.AddEmployee(t2);
        comp.AddEmployee(u1);
        comp.AddEmployee(s1);

        // Exercise 12: GetSalary and GetScore via virtual/override
        Console.WriteLine("Employee 301 -> Salary: " + e1.GetSalary() + ", Score: " + e1.GetScore());
        Console.WriteLine("Technician 101 -> Salary: " + t1.GetSalary() + ", Score: " + t1.GetScore());
        Console.WriteLine("Technician 102 -> Salary: " + t2.GetSalary() + ", Score: " + t2.GetScore());
        Console.WriteLine("UnionMember 201 -> Salary: " + u1.GetSalary() + ", Score: " + u1.GetScore());
        Console.WriteLine("Supervisor 401 -> Salary: " + s1.GetSalary() + ", Score: " + s1.GetScore());
        Console.WriteLine("Total company salary: " + comp.TotalSalary());

        // Polymorphism through the base class
        Employee[] all = new Employee[] { e1, t1, t2, u1, s1 };
        for (int i = 0; i < all.Length; i++)
        {
            Console.WriteLine(all[i].GetId() + " earns " + all[i].GetSalary());
        }

        // Exercise 13: YearlyBonus and GetBonusEmployees
        Console.WriteLine("Bonus? 301: " + e1.YearlyBonus() + ", 101: " + t1.YearlyBonus() +
            ", 102: " + t2.YearlyBonus() + ", 201: " + u1.YearlyBonus() + ", 401: " + s1.YearlyBonus());
        Employee[] bonusList = comp.GetBonusEmployees();
        for (int i = 0; i < bonusList.Length; i++)
        {
            Console.WriteLine("Bonus employee: " + bonusList[i].ToString());
        }
    }
}
