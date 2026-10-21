using System;

public class SortServices
{
    public static void SortAscending(IComparable[] arr)
    {
        if (arr == null)
        {
            return;
        }
        for (int i = 0; i < arr.Length - 1; i++)
        {
            for (int j = 0; j < arr.Length - 1 - i; j++)
            {
                if (arr[j] != null && arr[j + 1] != null && arr[j].CompareTo(arr[j + 1]) > 0)
                {
                    IComparable temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }

    public static void SortDescending(IComparable[] arr)
    {
        if (arr == null)
        {
            return;
        }
        for (int i = 0; i < arr.Length - 1; i++)
        {
            for (int j = 0; j < arr.Length - 1 - i; j++)
            {
                if (arr[j] != null && arr[j + 1] != null && arr[j].CompareTo(arr[j + 1]) < 0)
                {
                    IComparable temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
}
