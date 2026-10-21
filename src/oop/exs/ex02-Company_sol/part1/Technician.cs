using System;

public class Technician
{
    private string id;
    private string name;
    private int seniority;
    private int computers;

    public Technician(string id, string name, int seniority, int computers)
    {
        this.id = id;
        this.name = name;
        this.seniority = seniority;
        this.SetComputers(computers);
    }

    public Technician(string id, string name, int computers)
    {
        this.id = id;
        this.name = name;
        this.seniority = 0;
        this.SetComputers(computers);
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

    public int GetComputers()
    {
        return this.computers;
    }

    public void SetName(string name)
    {
        this.name = name;
    }

    public void SetComputers(int computers)
    {
        if (computers >= 0)
        {
            this.computers = computers;
        }
    }

    public void AddSeniorityYear()
    {
        this.seniority++;
    }

    public override string ToString()
    {
        return $"ID: {this.id}, Name: {this.name}, Seniority: {this.seniority}, Computers: {this.computers}";
    }
}
