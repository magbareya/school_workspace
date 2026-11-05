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
}
