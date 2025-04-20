#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int input;
    int total;
    do
    {
    input = get_int("How much you have in cents? ");
    }
    while (input <=0);

   int q=(input/25);
   int d=(input-(q*25))/10;
   int n=(input-((q*25)+(d*10)))/5;
   int c=input-((q*25)+(d*10)+(n*5));
    total=q+d+n+c;
      printf("%i Total\n", total);


}
