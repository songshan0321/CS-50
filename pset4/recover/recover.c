#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    int picNumber = 0;
    char filename[8];
    unsigned char buffer[512];

    FILE *img = NULL;
    while(fread(buffer, 512, 1, file))
    {
        // if start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 &&
            buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close the file, if it is opened
            if (img != NULL)
                fclose(img);

            //create new JPEG
            sprintf(filename,"%03i.jpg", picNumber);
            img = fopen(filename, "w");

            picNumber ++;
        }

        if (img != NULL)
            fwrite(buffer, 512, 1, img);

    }
    if (img != NULL)
        fclose(img);
    fclose(file);
    return 0;
}