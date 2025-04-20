#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int points []= {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int compute_score(string word);
int digit;
string word1, word2;
int main (void)
{

         do
 {
  word1 =get_string ("Player 1: \n");

        digit = 0;
        for (int i = 0; i < strlen(word1); i++)
        {
            if (!(((word1[i] >= 'a' && word1[i] <= 'z') || (word1[i] >= 'A' && word1[i] <= 'Z')  )))
            {
                if (word1[i] != '!' && word1[i] != '?')
                {digit = 1;
                break;}
            }
        }

        if (digit==1)
        {
            printf("Words only, please! \n");
        }
 }
       while (digit);

   do
 {
  word2 =get_string ("Player 2: \n");


        digit = 0;
        for (int i = 0; i < strlen(word2); i++)
        {
            if (!(((word2[i] >= 'a' && word2[i] <= 'z') || (word2[i] >= 'A' && word2[i] <= 'Z')  )))
            {
                if (word2[i] != '!' && word2[i] != '?')
                {digit = 1;
                break;}
            }
        }

        if (digit==1)
        {
            printf("Words only, please! \n");
        }
 }
       while (digit);

// Compute the score of each word
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

}
int compute_score(string word)
{
    // Keep track of score
    int score = 0;
    // Compute score for each character
    for (int j = 0, len = strlen(word); j < len; j++)
    {
        if (isupper(word[j]))
        {
            score += points[word[j] - 'A'];
        }
        else if (islower(word[j]))
        {
            score += points[word[j] - 'a'];
        }
    }

    return score;
}
