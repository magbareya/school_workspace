# Classes and Objects

## step 1: Defining class and instantiation

```csharp
using System;
class Book
{
    public string Title;
    public string Author;
    public int Year;
    public double Price;
}
internal class Program
{
    public static void Main(string[] args)
    {
        Book b = new Book();
        b.Title = "Algebra";
        b.Author = "Teacher";
        b.Year = 2020;
        b.Price = 100.0;

        Book b2 = new Book();
        b2.Title = "Geometry";
        b2.Author = "Teacher";
        b2.Year = 2022;
        b2.Price = 150.0;
    }
}
```

## step 2: Parameterless methods and invoking them (the method gets the instance as hidden parameter)

```csharp
using System;
class Book
{
    public string Title;
    public string Author;
    public int Year;
    public double Price;

    public void Print()
    {
        Console.WriteLine($"{Author}: {Title} ({Year})");
    }
}
internal class Program
{
    public static void PrintBook(Book b)
    {
        Console.WriteLine($"{b.Author}: {b.Title} ({b.Year})");
    }
    public static void Main(string[] args)
    {
        Book b1 = new Book();
        b1.Title = "Algebra";
        b1.Author = "Teacher";
        b1.Year = 2020;
        b1.Price = 100.0;
        b1.Print();

        Book b2 = new Book();
        b2.Title = "Geometry";
        b2.Author = "Teacher";
        b2.Year = 2022;
        b2.Price = 150.0;
        PrintBook(b2);
    }
}
```

## step 3: methods with Parameters and invoking them

```csharp
using System;
class Book
{
    public string Title;
    public string Author;
    public int Year;
    public double Price;

    public void Print()
    {
        Console.WriteLine($"{Author}: {Title} ({Year})");
    }

    public bool WasPublishedBefore(int year)
    {
        return Year < year;
    }
}
internal class Program
{
    public static void Main(string[] args)
    {
        Book b1 = new Book();
        b1.Title = "Algebra";
        b1.Author = "Teacher";
        b1.Year = 2020;
        b1.Price = 100.0;
        b1.Print();
        if(b1.WasPublishedBefore(2021))
            Console.WriteLine("The book was published before 2021.");

        Book b2 = new Book();
        b2.Title = "Geometry";
        b2.Author = "Teacher";
        b2.Year = 2022;
        b2.Price = 150.0;
        b2.Print();
        if (b2.WasPublishedBefore(2021))
            Console.WriteLine("The book was published before 2021.");
        else
            Console.WriteLine("The book was published in 2021 or later.");
    }
}
```

### step 3.1: IsEqual method vs `==` operator

```csharp
using System;
class Book
{
    public string Title;
    public string Author;
    public int Year;
    public double Price;

    public void Print()
    {
        Console.WriteLine($"{Author}: {Title} ({Year})");
    }

    public bool WasPublishedBefore(int year)
    {
        return Year < year;
    }

    public bool IsEqualTo(Book other)
    {
        return Title == other.Title
            && Author == other.Author
            && Year == other.Year;
    }
}
internal class Program
{
    public static void Main(string[] args)
    {
        Book b1 = new Book();
        b1.Title = "Algebra";
        b1.Author = "Teacher";
        b1.Year = 2020;
        b1.Price = 100.0;

        Book b2 = new Book();
        b2.Title = "Algebra";
        b2.Author = "Teacher";
        b2.Year = 2020;
        b2.Price = 100.0;

        if (b1 == b2)
            Console.WriteLine("b1 == b2");
        else
            Console.WriteLine("b1 != b2");

        if(b1.IsEqualTo(b2))
            Console.WriteLine("b1 is equal to b2");
        else
            Console.WriteLine("b1 is not equal to b2");
    }
}
```

### step 3.2: Using `this` keyword

```csharp
using System;
class Book
{
    public string Title;
    public string Author;
    public int Year;
    public double Price;

    public void Print()
    {
        Console.WriteLine($"{Author}: {Title} ({Year})");
    }

    public bool WasPublishedBefore(int year)
    {
        return Year < year;
    }

    public bool IsEqualTo(Book other)
    {
        return this.Title == other.Title
            && this.Author == other.Author
            && this.Year == other.Year;
    }
}
internal class Program
{
    public static void Main(string[] args)
    {
        Book b1 = new Book();
        b1.Title = "Algebra";
        b1.Author = "Teacher";
        b1.Year = 2020;
        b1.Price = 100.0;

        Book b2 = new Book();
        b2.Title = "Algebra";
        b2.Author = "Teacher";
        b2.Year = 2020;
        b2.Price = 100.0;

        if (b1 == b2)
            Console.WriteLine("b1 == b2");
        else
            Console.WriteLine("b1 != b2");

        if(b1.IsEqualTo(b2))
            Console.WriteLine("b1 is equal to b2");
        else
            Console.WriteLine("b1 is not equal to b2");
    }
}
```

### step 3.3: `null` what is it? and checking null parameters

```csharp
using System;
class Book
{
    public string Title;
    public string Author;
    public int Year;
    public double Price;

    public void Print()
    {
        Console.WriteLine($"{Author}: {Title} ({Year})");
    }

    public bool WasPublishedBefore(int year)
    {
        return Year < year;
    }

    public bool IsEqualTo(Book other)
    {
        if(other == null)
            return false;

        return this.Title == other.Title
            && this.Author == other.Author
            && this.Year == other.Year;
    }
}
internal class Program
{
    public static void Main(string[] args)
    {
        Book b1 = new Book();
        b1.Title = "Algebra";
        b1.Author = "Teacher";
        b1.Year = 2020;
        b1.Price = 100.0;

        Book b2 = new Book();
        b2.Title = "Algebra";
        b2.Author = "Teacher";
        b2.Year = 2020;
        b2.Price = 100.0;

        Book b3 = null;

        if(b1.IsEqualTo(b3))
            Console.WriteLine("b1 is equal to b3");
        else
            Console.WriteLine("b1 is not equal to b3");
    }
}
```

## step 4: Constructor

```csharp
using System;
class Book
{
    public string Title;
    public string Author;
    public int Year;
    public double Price;

    public Book(string title, string author, int year, double price)
    {
        this.Title = title;
        this.Author = author;
        this.Year = year;
        this.Price = price;
    }

    public void Print()
    {
        Console.WriteLine($"{Author}: {Title} ({Year})");
    }

    public bool WasPublishedBefore(int year)
    {
        return Year < year;
    }

    public bool IsEqualTo(Book other)
    {
        if (other == null)
            return false;

        return this.Title == other.Title
            && this.Author == other.Author
            && this.Year == other.Year;
    }
}
internal class Program
{
    public static void Main(string[] args)
    {
        Book b1 = new Book("Algebra", "Teacher", 2020, 100.0);
        Book b2 = new Book("Geometry", "Teacher", 2022, 150.0);
        b1.Print();
    }
}
```

## step 5: Private Properies, getters and setter

### step 5.1: Properties getters

```csharp
using System;
class Book
{
    private string Title;
    private string Author;
    private int Year;
    private double Price;

    public Book(string title, string author, int year, double price)
    {
        this.Title = title;
        this.Author = author;
        this.Year = year;
        this.Price = price;
    }

    public string GetTitle()
    {
        return Title;
    }
    public string GetAuthor()
    {
        return Author;
    }

    public int GetYear()
    {
        return Year;
    }

    public double GetPrice()
    {
        return Price;
    }

    public void Print()
    {
        Console.WriteLine($"{Author}: {Title} ({Year})");
    }

    public bool WasPublishedBefore(int year)
    {
        return Year < year;
    }

    public bool IsEqualTo(Book other)
    {
        if (other == null)
            return false;

        return this.Title == other.Title
            && this.Author == other.Author
            && this.Year == other.Year;
    }
}
internal class Program
{
    public static void Main(string[] args)
    {
        Book b1 = new Book("Algebra", "Teacher", 2020, 100.0);
        Book b2 = new Book("Geometry", "Teacher", 2022, 150.0);
        b1.Print();
        Console.WriteLine(b2.GetTitle());
        Console.WriteLine(b2.GetAuthor());
        Console.WriteLine(b2.Author); // ERROR
    }
}
```

### step 5.2: Properies setters (maybe to some properties only)

```csharp
using System;
class Book
{
    private string Title;
    private string Author;
    private int Year;
    private double Price;

    public Book(string title, string author, int year, double price)
    {
        this.Title = title;
        this.Author = author;
        this.Year = year;
        this.Price = price;
    }

    public string GetTitle()
    {
        return Title;
    }
    public string GetAuthor()
    {
        return Author;
    }

    public int GetYear()
    {
        return Year;
    }

    public double GetPrice()
    {
        return Price;
    }

    public void SetPrice(double newPrice)
    {
        if(newPrice > 0)
            Price = newPrice;
    }

    public void Print()
    {
        Console.WriteLine($"{Author}: {Title} ({Year})");
    }

    public bool WasPublishedBefore(int year)
    {
        return Year < year;
    }

    public bool IsEqualTo(Book other)
    {
        if (other == null)
            return false;

        return this.Title == other.Title
            && this.Author == other.Author
            && this.Year == other.Year;
    }
}
internal class Program
{
    public static void Main(string[] args)
    {
        Book b1 = new Book("Algebra", "Teacher", 2020, 100.0);
        Book b2 = new Book("Geometry", "Teacher", 2022, 150.0);
        Console.WriteLine(b2.GetPrice()); // 150.0
        b2.SetPrice(120.0);
        Console.WriteLine(b2.GetPrice()); // 120.0
        b2.SetPrice(-100); // will do nothing
        Console.WriteLine(b2.GetPrice()); // 120.0
    }
}
```

## step 6: more methods

```csharp
using System;
class Book
{
    private string Title;
    private string Author;
    private int Year;
    private double Price;

    public Book(string title, string author, int year, double price)
    {
        this.Title = title;
        this.Author = author;
        this.Year = year;
        this.Price = price;
    }

    public string GetTitle()
    {
        return Title;
    }
    public string GetAuthor()
    {
        return Author;
    }

    public int GetYear()
    {
        return Year;
    }

    public double GetPrice()
    {
        return Price;
    }

    public void SetPrice(double newPrice)
    {
        if(newPrice > 0)
            Price = newPrice;
    }

    public void Print()
    {
        Console.WriteLine($"{Author}: {Title} ({Year})");
    }

    public bool WasPublishedBefore(int year)
    {
        return Year < year;
    }

    public bool IsEqualTo(Book other)
    {
        if (other == null)
            return false;

        return this.Title == other.Title
            && this.Author == other.Author
            && this.Year == other.Year;
    }

    public void ApplyDiscount(int ratio)
    {
        this.Price = this.Price * (100 - ratio) / 100;
    }
}
internal class Program
{
    public static void Main(string[] args)
    {
        Book b1 = new Book("Algebra", "Teacher", 2020, 100.0);
        Console.WriteLine(b1.GetPrice()); // 100.0
        b1.ApplyDiscount(20);
        Console.WriteLine(b1.GetPrice()); // 80.0
    }
}
```
