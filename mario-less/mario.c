#include <stdio.h>
#include <cs50.h>
int main(void)

{
int n;
 do
   {
   n=get_int("number of blocks? ");
   }
 while (n<1);
for (int i=0; i<n; i++)
 {
    for (int y=0; y<=i; y++)
    {
     printf("#");
    }
   printf("\n");
 }
}
