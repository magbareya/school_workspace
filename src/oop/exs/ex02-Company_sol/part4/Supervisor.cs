using System;

public class Supervisor : Employee
{
    private Employee[] team;
    private int teamCount;

    public Supervisor(string id, string name, int seniority)
        : base(id, name, seniority)
    {
        this.team = new Employee[15];
        this.teamCount = 0;
    }

    public Supervisor(string id, string name, int seniority, Employee[] team)
        : base(id, name, seniority)
    {
        this.team = new Employee[15];
        this.teamCount = 0;
        if (team != null)
        {
            for (int i = 0; i < team.Length && this.teamCount < 15; i++)
            {
                if (team[i] != null)
                {
                    this.team[this.teamCount] = team[i];
                    this.teamCount++;
                }
            }
        }
    }

    public Employee[] GetTeam()
    {
        return this.team;
    }

    public int GetTeamCount()
    {
        return this.teamCount;
    }

    public bool AddEmployeeToTeam(Employee emp)
    {
        if (emp != null && this.teamCount < 15)
        {
            this.team[this.teamCount] = emp;
            this.teamCount++;
            return true;
        }
        return false;
    }

    public bool TransferBonusSeniority(Employee emp)
    {
        if (emp == null)
        {
            return false;
        }
        for (int i = 0; i < this.teamCount; i++)
        {
            if (this.team[i].GetId() == emp.GetId())
            {
                this.team[i].AddSeniorityYear();
                return true;
            }
        }
        return false;
    }

    public override double GetSalary()
    {
        // Stage 4 formula: base salary + 100 for each actual team member
        return base.GetSalary() + (100 * this.teamCount);
    }

    public override int GetScore()
    {
        int totalScore = base.GetScore();
        for (int i = 0; i < this.teamCount; i++)
        {
            totalScore += this.team[i].GetScore();
        }
        return totalScore;
    }

    public override bool YearlyBonus()
    {
        return false;
    }

    public override string ToString()
    {
        return base.ToString() + $", TeamCount: {this.teamCount}";
    }
}
