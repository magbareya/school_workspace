using System;

public class UnionMember : Employee
{
    private int unionYears;

    public UnionMember(string id, string name, int seniority, int unionYears)
        : base(id, name, seniority)
    {
        this.unionYears = unionYears;
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

    public override int GetScore()
    {
        return (2 * base.GetScore()) + (2 * this.unionYears);
    }

    public override bool YearlyBonus()
    {
        return false;
    }

    public override string ToString()
    {
        return base.ToString() + $", UnionYears: {this.unionYears}";
    }
}
