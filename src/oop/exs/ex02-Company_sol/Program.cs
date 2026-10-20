using System;

public class Program
{
    public static bool IsAccepted(object[] arr)
    {
        if (arr == null)
        {
            return false;
        }
        int forPoints = 0;
        int againstPoints = 0;

        for (int i = 0; i < arr.Length; i++)
        {
            if (arr[i] is Employee)
            {
                Employee emp = (Employee)arr[i];
                if (emp is UnionMember || emp is Supervisor)
                {
                    againstPoints += emp.GetScore();
                }
                else
                {
                    forPoints += emp.GetScore();
                }
            }
        }
        return forPoints > againstPoints;
    }

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
        s1.TransferBonusSeniority(t1);

        comp.AddEmployee(e1);
        comp.AddEmployee(t1);
        comp.AddEmployee(t2);
        comp.AddEmployee(u1);
        comp.AddEmployee(s1);

        Console.WriteLine("Details of 101: " + comp.GetEmployeeDetails("101"));
        Console.WriteLine("Most Veteran ID: " + comp.GetMostVeteranId());
        Console.WriteLine("Total Salary: " + comp.TotalSalary());

        Employee[] bonusList = comp.GetBonusEmployees();
        Console.WriteLine("Bonus Employees Count: " + bonusList.Length);

        Technician[] seniorTechs = comp.GetSeniorTechnicians(100);
        Console.WriteLine("Senior Techs Count: " + seniorTechs.Length);

        string[] report = comp.AuditReport();
        for (int i = 0; i < report.Length; i++)
        {
            Console.WriteLine(report[i]);
        }

        object[] allObjects = new object[] { e1, t1, t2, u1, s1 };
        Console.WriteLine("Proposal Accepted? " + IsAccepted(allObjects));
    }
}
