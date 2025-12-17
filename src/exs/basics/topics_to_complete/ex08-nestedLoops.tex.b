\documentclass[14pt]{extarticle}
\input{../../../scripts/tex_preamble.tex}

\title{ورقة تمرن 8 للصف العاشر 10 - حلقات متداخلة}

\begin{document}

\maketitle
\thispagestyle{fancy}

\section{الحلقات المتداخلة}
\begin{enumerate}
    \item استخدم \textenglish{for} داخل  \textenglish{for} لطباعة الجدول التالي:
    \begin{align*}
      &1\ 2\ 3\ 4\ 5 \\
      &1\ 2\ 3\ 4\ 5 \\
      &1\ 2\ 3\ 4\ 5
    \end{align*}
    \item اطبع مصفوفة نجوم $4 \times 6$ (4 أسطر، كل سطر 6 نجوم).
    % \item  \textenglish{for} داخل  \textenglish{while}: اقرأ 5 أعداد، وإذا كان أحدها سالبًا أعد طلبه حتى يدخل عددًا صحيحًا.
    \item استخدم \textenglish{for} داخل  \textenglish{for} لطباعة جميع الأزواج $(i,j)$ حيث $i=1..3$ و $j=1..4$.
    \item استخدم \textenglish{while} داخل  \textenglish{for}: اطلب عددًا موجبًا، وإذا كان صفرًا أو سالبًا أعد طلبه، وبعدها اطبع جدول ضربه حتى ×10.
    \item استخدم \textenglish{for} داخل  \textenglish{for} لطباعة مثلث النجوم:
    \begin{english}
    \begin{align*}
    * \\
    ** \\
    *** \\
    ****
    \end{align*}
\end{english}
    \item استخدم \textenglish{for داخل while}: اقرأ عدد الأسطر، وإذا كان سلبيًا اطلبه مرة أخرى، ثم أطبع من 1 حتى طول السطر في كل سطر.
    \item استخدم \textenglish{for داخل for} لطباعة جميع الأزواج $(i,j)$ حيث $j>i$ و $i,j$ من 1 إلى 5.
    \item استخدم \textenglish{while داخل for}: اطبع الأعداد من 1 إلى 5، لكن قبل كل عدد اطلب من المستخدم إدخال ``y'' للتأكيد.
    \item استخدم \textenglish{for داخل while}: اقرأ أعدادًا حتى يدخل المستخدم عددًا سالبًا، ولكل عدد موجب اطبع كلمة ``Hello'' بعدد ذلك العدد.

    \item اكتب عملية تتلقى عددًا $n$ وتطبع مثلثًا من الأرقام كما في الشكل (للمدخل 4):
\begin{english}
\begin{verbatim}
1
1 2
1 2 3
1 2 3 4
\end{verbatim}
\end{english}
\ifwithsols
\begin{boxSolution}
\begin{english}
\begin{minted}{csharp}
public static void PrintNumTriangle(int n)
{
    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= i; j++)
        {
            Console.Write(j + " ");
        }
        Console.WriteLine();
    }
}
\end{minted}
\end{english}
\end{boxSolution}
\fi
\end{enumerate}

\vspace{1cm}
\begin{flushleft}
أرجو لكم وقتًا ممتعًا.

الأستاذ محمود اغبارية.
\end{flushleft}

\end{document}



