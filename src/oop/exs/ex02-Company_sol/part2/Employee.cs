using System;

public class Employee
{
    protected string id;
    protected string name;
    protected int seniority;

    public Employee(string id, string name, int seniority)
    {
        this.id = id;
        this.name = name;
        this.seniority = seniority;
    }

    public Employee(string id, string name)
    {
        this.id = id;
        this.name = name;
        this.seniority = 0;
    }

    public string GetId()
    {
        return this.id;
    }

    public string GetName()
    {
        return this.name;
    }

    public int GetSeniority()
    {
        return this.seniority;
    }

    public void SetName(string name)
    {
        this.name = name;
    }

    public void AddSeniorityYear()
    {
        this.seniority++;
    }

    public override string ToString()
    {
        return $"ID: {this.id}, Name: {this.name}, Seniority: {this.seniority}";
    }
}
