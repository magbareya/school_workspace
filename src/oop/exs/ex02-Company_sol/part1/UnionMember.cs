using System;

public class UnionMember
{
    private string id;
    private string name;
    private int seniority;
    private int unionYears;

    public UnionMember(string id, string name, int seniority, int unionYears)
    {
        this.id = id;
        this.name = name;
        this.seniority = seniority;
        this.SetUnionYears(unionYears);
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

    public int GetUnionYears()
    {
        return this.unionYears;
    }

    public void SetName(string name)
    {
        this.name = name;
    }

    public void SetUnionYears(int unionYears)
    {
        if (unionYears >= 0 && unionYears <= this.seniority)
        {
            this.unionYears = unionYears;
        }
    }

    public void AddSeniorityYear()
    {
        this.seniority++;
    }

    public override string ToString()
    {
        return $"ID: {this.id}, Name: {this.name}, Seniority: {this.seniority}, UnionYears: {this.unionYears}";
    }
}
