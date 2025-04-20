#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

char ciphertext[26];
int main(int argc, string argv[])
{

    if (strlen(argv[1]) > 26 || strlen(argv[1]) < 26)
    {
        argc = 1;
        printf("Key must contain 26 characters \n");
        return argc;
    }
    for (int i = 0; argv[i] != NULL; i++)
    {
        for (int j = 0; j < strlen(argv[i]); j++)
        {

            if (!((argv[1][j] >= 'a' && argv[1][j] <= 'z') ||
                  (argv[1][j] >= 'A' && argv[1][j] <= 'Z')))
            {
                argc = 1;
                printf("key\n");
                return argc;
            }
            for (int n = j + 1; n < strlen(argv[i]); n++)
            {
                if (argv[1][j] == argv[1][n])
                {
                    argc = 1;
                    printf("Repeating symbols\n");

                    return argc;
                }
            }
            if islower (argv[1][j])
            {
                argv[1][j] = (char) (argv[1][j] - 32);
            }
        }
    }

    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        if isalpha (plaintext[i])
        {
            if islower (plaintext[i])
            {
                ciphertext[i] = (char) (argv[1][((int) plaintext[i] - (97))]) + 32;
            }
            else
            {
                ciphertext[i] = (char) (argv[1][((int) plaintext[i] - (65))]);
            }
        }
        else
        {
            ciphertext[i] = (char) plaintext[i];
        }
        printf("%c", ciphertext[i]);

    }
    argc=0;
printf("\n");
    return argc;
}
