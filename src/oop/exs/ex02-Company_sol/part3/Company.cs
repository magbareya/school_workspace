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
}
