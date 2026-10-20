using System;

public class Date : IComparable
{
    private int day;
    private int month;
    private int year;

    public Date(int day, int month, int year)
    {
        this.day = day;
        this.month = month;
        this.year = year;
    }

    public Date(Date other)
    {
        if (other != null)
        {
            this.day = other.day;
            this.month = other.month;
            this.year = other.year;
        }
    }

    public int GetDay()
    {
        return this.day;
    }

    public int GetMonth()
    {
        return this.month;
    }

    public int GetYear()
    {
        return this.year;
    }

    public void SetDay(int day)
    {
        this.day = day;
    }

    public void SetMonth(int month)
    {
        this.month = month;
    }

    public void SetYear(int year)
    {
        this.year = year;
    }

    public int CompareTo(object obj)
    {
        if (obj == null || !(obj is Date))
        {
            return 1;
        }
        Date other = (Date)obj;
        if (this.year != other.year)
        {
            return this.year - other.year;
        }
        if (this.month != other.month)
        {
            return this.month - other.month;
        }
        return this.day - other.day;
    }

    public override string ToString()
    {
        return $"{this.day}.{this.month}.{this.year}";
    }
}
