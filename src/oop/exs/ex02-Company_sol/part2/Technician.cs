using System;

public class Technician : Employee
{
    private int computers;

    public Technician(string id, string name, int seniority, int computers)
        : base(id, name, seniority)
    {
        this.SetComputers(computers);
    }

    public Technician(string id, string name, int computers)
        : base(id, name)
    {
        this.SetComputers(computers);
    }

    public int GetComputers()
    {
        return this.computers;
    }

    public void SetComputers(int computers)
    {
        if (computers >= 0)
        {
            this.computers = computers;
        }
    }

    public override string ToString()
    {
        return base.ToString() + $", Computers: {this.computers}";
    }
}
