#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void no(void)
{
    printf("Nope.\n");
    exit(1);
}

void ok(void)
{
    printf("Good job.\n");
}

int main(void)
{
    char    input[100];
    char    buffer[100];
    char    chunk[4];
    int     idx_input = 2;
    int     idx_buf = 0;
    int     val;

    printf("Please enter key: ");
    if (scanf("%s", input) != 1)
        no();
    
    if (input[0] != '4' || input[1] != '2')
        no();
    
    memset(buffer, 0, 100);
    buffer[0] = '*';
    idx_buf = 1;

    while (idx_input < (int)strlen(input))
    {
        chunk[0] = input[idx_input];
        chunk[1] = input[idx_input + 1];
        chunk[2] = input[idx_input + 2];
        chunk[3] = '\0';

        val = atoi(chunk);
        buffer[idx_buf] = (char)val;

        idx_input += 3;
        idx_buf += 1;
    }

    if (strcmp(buffer, "********") == 0)
        ok();
    else
        no();
    
    return(0);
}
