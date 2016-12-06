using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace ConsoleApplication1
{
    public class Program
    {
        public static void Main(string[] args)
        {
            /* char[] alpha = new char[] { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0','1','2','3','4','5','6','7','8','9' };
             Dictionary<char, Int32> Alpha = new Dictionary<char, Int32>();

             for (int i = 0; i < alpha.Length; i++)
             {
                 Alpha.Add(alpha[i], 0);
             }

             String fileName = "C:\\Users\\Sebastian\\Documents\\Uni\\WebScience\\Hotel\\workspace\\a6\\simple-20160801-1-article-per-line";

             StreamReader sr = new StreamReader(fileName);
             String line = sr.ReadToEnd();

                 String[] words = line.Split(' ');
                 for(int i = 0; i < words.Length; i++)
                 {
                     for(int j = 0; j < words[i].Length; j++)
                     {
                         if(Alpha.ContainsKey(words[i][j]))
                         {
                             Alpha[words[i][j]] += 1;
                         }
                     }
                 }

             foreach(KeyValuePair<char, int> entry in Alpha)
             {
                 Console.WriteLine(entry.Key + ":" + entry.Value.ToString());
             }*/

            readLines();
            Console.ReadLine();
        }


        public static void readLines()
        {
            char[] alpha = new char[] { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
            Dictionary<char, Int32> Alpha = new Dictionary<char, Int32>();

            for (int i = 0; i < alpha.Length; i++)
            {
                Alpha.Add(alpha[i], 0);
            }

            String fileName = "C:\\Users\\Sebastian\\Documents\\Uni\\WebScience\\Hotel\\workspace\\a6\\simple-20160801-1-article-per-line";
            StreamReader sr = new StreamReader(fileName);
            String line;
            double lines = 0;
            double articleLines = 0;
            while((line = sr.ReadLine()) != null)
            {
                lines += 1;
                String word = line.Split(' ')[0].ToLower();
                if (word.Equals("the") || word.Equals("a") ||word.Equals("an"))
                {
                    articleLines += 1;
                }
            }

            double ratio = articleLines / lines;

            Console.WriteLine("total lines:" + lines.ToString());
            Console.WriteLine("lines with an article: " + articleLines.ToString());
            Console.WriteLine("ratio total/with article: " + ratio);

        }
    }


}
