using System;

public class UnionMember : Employee
{
    private int unionYears;

    public UnionMember(string id, string name, int seniority, int unionYears)
        : base(id, name, seniority)
    {
        this.SetUnionYears(unionYears);
    }

    public int GetUnionYears()
    {
        return this.unionYears;
    }

    public void SetUnionYears(int unionYears)
    {
        if (unionYears >= 0 && unionYears <= this.seniority)
        {
            this.unionYears = unionYears;
        }
    }

    public override string ToString()
    {
        return base.ToString() + $", UnionYears: {this.unionYears}";
    }
}
