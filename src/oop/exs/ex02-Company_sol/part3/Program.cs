using System;

public class Program
{
    public static void Main(string[] args)
    {
        // Exercise 6: Company registry with upcasting (Employee[])
        Company comp = new Company();
        Console.WriteLine("Initial employee count: " + comp.GetCurrent());

        // Exercise 7: AddEmployee — upcasting all four types into Employee[]
        Employee e1 = new Employee("301", "Nour", 6);
        Technician t1 = new Technician("101", "Rami", 7, 110);
        Technician t2 = new Technician("102", "Sami", 7, 40);
        UnionMember u1 = new UnionMember("201", "Huda", 8, 5);
        Supervisor s1 = new Supervisor("401", "Kareem", 10);
        s1.AddEmployeeToTeam(e1);
        s1.AddEmployeeToTeam(t1);
        comp.AddEmployee(e1);
        comp.AddEmployee(t1);
        comp.AddEmployee(t2);
        comp.AddEmployee(u1);
        comp.AddEmployee(s1);
        Console.WriteLine("Employee count after adds: " + comp.GetCurrent());

        // Exercise 8: GetEmployeeDetails — found and not found
        Console.WriteLine("Details of 101: " + comp.GetEmployeeDetails("101"));
        Console.WriteLine("Details of 999: '" + comp.GetEmployeeDetails("999") + "'");

        // Exercise 9: CountSameSeniority — t1 has 7 years, t2 also has 7
        Console.WriteLine("Employees with same seniority as 101: " + comp.CountSameSeniority("101"));

        // Exercise 10: GetEmployeesByMinSeniority
        Employee[] veterans = comp.GetEmployeesByMinSeniority(7);
        if (veterans != null)
        {
            for (int i = 0; i < veterans.Length; i++)
            {
                Console.WriteLine("Veteran: " + veterans[i].ToString());
            }
        }
        Employee[] none = comp.GetEmployeesByMinSeniority(50);
        Console.WriteLine("No employee with 50+ years? " + (none == null));

        // Exercise 11: GetMostVeteranId
        Console.WriteLine("Most veteran ID: " + comp.GetMostVeteranId());
    }
}
