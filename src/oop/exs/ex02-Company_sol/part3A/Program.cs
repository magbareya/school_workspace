using System;

public class Program
{
    public static void Main(string[] args)
    {
        // Exercise 1: Upcasting (saving derived objects in Employee references) and virtual/override
        Employee e1 = new Employee("301", "Nour", 6);
        Employee t1 = new Technician("101", "Rami", 7, 110);
        Employee t2 = new Technician("102", "Sami", 2, 40);
        Employee u1 = new UnionMember("201", "Huda", 8, 5);

        Supervisor sup = new Supervisor("401", "Kareem", 10);
        sup.AddEmployeeToTeam(e1);
        sup.AddEmployeeToTeam(t1);
        sup.AddEmployeeToTeam(u1);
        Employee s1 = sup;

        Console.WriteLine(e1.ToString() + " -> Salary: " + e1.GetSalary() + ", Score: " + e1.GetScore());
        Console.WriteLine(t1.ToString() + " -> Salary: " + t1.GetSalary() + ", Score: " + t1.GetScore());
        Console.WriteLine(t2.ToString() + " -> Salary: " + t2.GetSalary() + ", Score: " + t2.GetScore());
        Console.WriteLine(u1.ToString() + " -> Salary: " + u1.GetSalary() + ", Score: " + u1.GetScore());
        Console.WriteLine(s1.ToString() + " -> Salary: " + s1.GetSalary() + ", Score: " + s1.GetScore());

        // Exercise 2: YearlyBonus via base-class references
        Console.WriteLine("Bonus? 301: " + e1.YearlyBonus() + ", 101: " + t1.YearlyBonus() +
            ", 102: " + t2.YearlyBonus() + ", 201: " + u1.YearlyBonus() + ", 401: " + s1.YearlyBonus());

        // Exercise 3: Company and AddEmployee
        Company comp = new Company();
        Console.WriteLine("Initial employees count: " + comp.GetCurrent());
        comp.AddEmployee(e1);
        comp.AddEmployee(t1);
        comp.AddEmployee(t2);
        comp.AddEmployee(u1);
        comp.AddEmployee(s1);
        Console.WriteLine("Employees count after adding: " + comp.GetCurrent());

        // Exercise 4: GetEmployeeDetails, TotalSalary, and GetBonusEmployees
        Console.WriteLine("Details of 101: " + comp.GetEmployeeDetails("101"));
        Console.WriteLine("Details of 999: " + comp.GetEmployeeDetails("999"));
        Console.WriteLine("Total company salary: " + comp.TotalSalary());

        Employee[] bonusList = comp.GetBonusEmployees();
        for (int i = 0; i < bonusList.Length; i++)
        {
            Console.WriteLine("Bonus employee: " + bonusList[i].ToString());
        }
    }
}
