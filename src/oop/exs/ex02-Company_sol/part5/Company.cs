using System;

public class Company
{
    public const int MAX = 100;
    private Employee[] employees;
    private int current;

    public Company()
    {
        this.employees = new Employee[MAX];
        this.current = 0;
    }

    public int GetCurrent()
    {
        return this.current;
    }

    public bool AddEmployee(Employee e)
    {
        if (e != null && this.current < MAX)
        {
            this.employees[this.current] = e;
            this.current++;
            return true;
        }
        return false;
    }

    public string GetEmployeeDetails(string id)
    {
        for (int i = 0; i < this.current; i++)
        {
            if (this.employees[i].GetId() == id)
            {
                return this.employees[i].ToString();
            }
        }
        return "";
    }

    public int CountSameSeniority(string id)
    {
        int target = -1;
        for (int i = 0; i < this.current; i++)
        {
            if (this.employees[i].GetId() == id)
            {
                target = this.employees[i].GetSeniority();
            }
        }
        if (target == -1)
        {
            return 0;
        }
        int count = 0;
        for (int i = 0; i < this.current; i++)
        {
            if (this.employees[i].GetSeniority() == target)
            {
                count++;
            }
        }
        return count;
    }

    public Employee[] GetEmployeesByMinSeniority(int minYears)
    {
        int count = 0;
        for (int i = 0; i < this.current; i++)
        {
            if (this.employees[i].GetSeniority() >= minYears)
            {
                count++;
            }
        }
        if (count == 0)
        {
            return null;
        }
        Employee[] result = new Employee[count];
        int index = 0;
        for (int i = 0; i < this.current; i++)
        {
            if (this.employees[i].GetSeniority() >= minYears)
            {
                result[index] = this.employees[i];
                index++;
            }
        }
        return result;
    }

    public string GetMostVeteranId()
    {
        if (this.current == 0)
        {
            return "";
        }
        Employee veteran = this.employees[0];
        for (int i = 1; i < this.current; i++)
        {
            if (this.employees[i].GetSeniority() > veteran.GetSeniority())
            {
                veteran = this.employees[i];
            }
        }
        return veteran.GetId();
    }

    public double TotalSalary()
    {
        double sum = 0;
        for (int i = 0; i < this.current; i++)
        {
            sum += this.employees[i].GetSalary();
        }
        return sum;
    }

    public Employee[] GetBonusEmployees()
    {
        int count = 0;
        for (int i = 0; i < this.current; i++)
        {
            if (this.employees[i].YearlyBonus())
            {
                count++;
            }
        }
        Employee[] bonusArr = new Employee[count];
        int index = 0;
        for (int i = 0; i < this.current; i++)
        {
            if (this.employees[i].YearlyBonus())
            {
                bonusArr[index] = this.employees[i];
                index++;
            }
        }
        return bonusArr;
    }

    public Technician[] GetSeniorTechnicians(int minComputers)
    {
        int count = 0;
        for (int i = 0; i < this.current; i++)
        {
            if (this.employees[i] is Technician)
            {
                Technician tech = (Technician)this.employees[i];
                if (tech.GetComputers() >= minComputers)
                {
                    count++;
                }
            }
        }

        Technician[] result = new Technician[count];
        int index = 0;
        for (int i = 0; i < this.current; i++)
        {
            if (this.employees[i] is Technician)
            {
                Technician tech = (Technician)this.employees[i];
                if (tech.GetComputers() >= minComputers)
                {
                    result[index] = tech;
                    index++;
                }
            }
        }
        return result;
    }

    public string[] AuditReport()
    {
        int count = 0;
        for (int i = 0; i < this.current; i++)
        {
            Employee emp = this.employees[i];
            if ((emp is Technician || emp is UnionMember) &&
                emp.GetSeniority() > 3 && emp.GetScore() > 15)
            {
                count++;
            }
        }
        string[] report = new string[count];
        int index = 0;
        for (int i = 0; i < this.current; i++)
        {
            Employee emp = this.employees[i];
            if ((emp is Technician || emp is UnionMember) &&
                emp.GetSeniority() > 3 && emp.GetScore() > 15)
            {
                if (emp is Technician)
                {
                    Technician t = (Technician)emp;
                    report[index] = $"Type:Technician, ID:{t.GetId()}, Name:{t.GetName()}, " +
                        $"Score:{t.GetScore()}, Computers:{t.GetComputers()}";
                }
                else
                {
                    UnionMember u = (UnionMember)emp;
                    report[index] = $"Type:Union, ID:{u.GetId()}, Name:{u.GetName()}, " +
                        $"Score:{u.GetScore()}, UnionYears:{u.GetUnionYears()}";
                }
                index++;
            }
        }
        return report;
    }
}
