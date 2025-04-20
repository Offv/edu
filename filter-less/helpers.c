#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sum =((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) );
            float k = round(sum / 3.0);
            //int s =(int)k;
//if ((k-s)>0.5)
//s++;
            image[i][j].rgbtRed = round(k);
            image[i][j].rgbtBlue = round(k);
            image[i][j].rgbtGreen = round(k);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            float sepiaRed = (.393 * image[i][j].rgbtRed) + (.769 * image[i][j].rgbtGreen) +
                             (.189 * image[i][j].rgbtBlue);
            float sepiaGreen = (.349 * image[i][j].rgbtRed) + (.686 * image[i][j].rgbtGreen) +
                               (.168 * image[i][j].rgbtBlue);
            float sepiaBlue = (.272 * image[i][j].rgbtRed) + (.534 * image[i][j].rgbtGreen) +
                              (.131 * image[i][j].rgbtBlue);

            if (sepiaRed > 255)
                sepiaRed = 255;
            if (sepiaGreen > 255)
                sepiaGreen = 255;
            if (sepiaBlue > 255)
                sepiaBlue = 255;
            image[i][j].rgbtRed = (round(sepiaRed));
            image[i][j].rgbtGreen = (round(sepiaGreen));
            image[i][j].rgbtBlue = (round(sepiaBlue));
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int bufr[height][width];
    int bufg[height][width];
    int bufb[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width; k++)
        {
            bufr[i][k] = image[i][k].rgbtRed;
            bufb[i][k] = image[i][k].rgbtBlue;
            bufg[i][k] = image[i][k].rgbtGreen;
        }
    }
    for (int i = 0; i < height; i++){
        for (int j =0; j< width;  j++)
        {

            image[i][j].rgbtRed = bufr[i][width-j-1];
            image[i][j].rgbtBlue = bufb[i][width-j-1];
            image[i][j].rgbtGreen = bufg[i][width-j-1];
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int red = 0;
    int green = 0;
    int blue = 0;
    int counter = 0;

    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];  //create a copy of the image
        }
    }
    for (int i = 0; i < height; i++)
    {

        for (int j = 0; j < width; j++)
        {
            if (i - 1 >= 0)
            {
                red += copy[i - 1][j].rgbtRed;
                green += copy[i - 1][j].rgbtGreen;
                blue += copy[i - 1][j].rgbtBlue;
                counter++;
            }
            if (i + 1 < height)
            {
                red += copy[i + 1][j].rgbtRed;
                green += copy[i + 1][j].rgbtGreen;
                blue += copy[i + 1][j].rgbtBlue;
                counter++;
            }
            if (j - 1 >= 0)
            {
                red += copy[i][j - 1].rgbtRed;
                green += copy[i][j - 1].rgbtGreen;
                blue += copy[i][j - 1].rgbtBlue;
                counter++;
            }
            if (j + 1 < width)
            {
                red += copy[i][j + 1].rgbtRed;
                green += copy[i][j + 1].rgbtGreen;
                blue += copy[i][j + 1].rgbtBlue;
                counter++;
            }
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                red += copy[i - 1][j - 1].rgbtRed;
                green += copy[i - 1][j - 1].rgbtGreen;
                blue += copy[i - 1][j - 1].rgbtBlue;
                counter++;
            }
            if (i + 1 < height && j + 1 < width)
            {
                red += copy[i + 1][j + 1].rgbtRed;
                green += copy[i + 1][j + 1].rgbtGreen;
                blue += copy[i + 1][j + 1].rgbtBlue;
                counter++;
            }
            if (i + 1 < height && j - 1 >= 0)
            {
                red += copy[i + 1][j - 1].rgbtRed;
                green += copy[i + 1][j - 1].rgbtGreen;
                blue += copy[i + 1][j - 1].rgbtBlue;
                counter++;
            }
            if (i - 1 >= 0 && j + 1 < width)
            {
                red += copy[i - 1][j + 1].rgbtRed;
                green += copy[i - 1][j + 1].rgbtGreen;
                blue += copy[i - 1][j + 1].rgbtBlue;
                counter++;
            }
            red += copy[i][j].rgbtRed;
            green += copy[i][j].rgbtGreen;
            blue += copy[i][j].rgbtBlue;
            counter++;

            image[i][j].rgbtRed = round(red / (counter * 1.0));
            image[i][j].rgbtGreen = round(green / (counter * 1.0));
            image[i][j].rgbtBlue = round(blue / (counter * 1.0));

            red = 0;
            green = 0;
            blue = 0;
            counter = 0;
        }
    }
    return;
}

