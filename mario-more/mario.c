#include <stdio.h>
#include <cs50.h>


int main(void)

{
int n;
int cond;
int x=0;
 do
   {
   n=get_int("number of blocks? ");
   if (0<n)
   {
    cond=1;
    if (n<=8)
    {
   cond=1;
   }
   else cond=0;}
    else cond=0;}

 while (cond==0);

for (int i=n; i>0; i--)
 {
    for (int j=1; j<=n; j++)
    {
    if (j<i)
     printf(" ");
     else
     {
        printf("#");
        x++;
     }
    }
    printf("  ");
    for (int y=x; y>0; y--)
    {
     printf("#");
    }
   printf("\n");
   x=0;

 }
}

