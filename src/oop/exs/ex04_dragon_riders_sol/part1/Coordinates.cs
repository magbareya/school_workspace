using System;

public class Coordinates
{
    private int x;
    private int y;

    public Coordinates(int x, int y)
    {
        this.x = this.Clamp(x);
        this.y = this.Clamp(y);
    }

    public Coordinates(Coordinates other)
    {
        if (other != null)
        {
            this.x = other.x;
            this.y = other.y;
        }
    }

    private int Clamp(int val)
    {
        if (val < 0)
        {
            return 0;
        }
        if (val > 1000)
        {
            return 1000;
        }
        return val;
    }

    public int GetX()
    {
        return this.x;
    }

    public int GetY()
    {
        return this.y;
    }

    public void SetX(int x)
    {
        this.x = this.Clamp(x);
    }

    public void SetY(int y)
    {
        this.y = this.Clamp(y);
    }

    public double DistanceTo(Coordinates other)
    {
        if (other == null)
        {
            return 0;
        }
        double dx = this.x - other.x;
        double dy = this.y - other.y;
        return Math.Sqrt((dx * dx) + (dy * dy));
    }

    public bool IsOnMapEdge()
    {
        return this.x == 0 || this.x == 1000 || this.y == 0 || this.y == 1000;
    }

    public bool IsInside(Coordinates c1, Coordinates c2)
    {
        if (c1 == null || c2 == null)
        {
            return false;
        }
        int minX = Math.Min(c1.x, c2.x);
        int maxX = Math.Max(c1.x, c2.x);
        int minY = Math.Min(c1.y, c2.y);
        int maxY = Math.Max(c1.y, c2.y);

        return this.x >= minX && this.x <= maxX &&
               this.y >= minY && this.y <= maxY;
    }

    public override string ToString()
    {
        return $"({this.x},{this.y})";
    }
}
