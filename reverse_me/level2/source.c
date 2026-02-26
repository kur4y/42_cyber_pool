#include <stdio.h>
#include <string.h>
#include <stdlib.h>


void no(void)
{
    printf("Nope.\n");
    exit(1);
}

void ok(void)
{
    printf("Good job.\n");
    return;
}

int main(int ac, char **av)
{
    char    input[100];
    char    constructed_pwd[9];
    char    chunk[4];
    int     input_idx = 2;
    int     pwd_idx = 1;
    int     val;

    (void) ac;
    (void) av;
    
    printf("Please enter key: ");
    
    if (scanf("%s", input) != 1)
        no();
    
    if (input[0] != '0' || input[1] != '0')
        no();
    
    memset(constructed_pwd, 0, 9);
    constructed_pwd[0] = 'd';

    while (pwd_idx < 8)
    {
        chunk[0] = input[input_idx];
        chunk[1] = input[input_idx + 1];
        chunk[2] = input[input_idx + 2];
        chunk[3] = '\0';

        val = atoi(chunk);
        constructed_pwd[pwd_idx] = (char)val;

        input_idx += 3;
        pwd_idx += 1;
    }
    constructed_pwd[pwd_idx] = '\0';

    if (strcmp(constructed_pwd, "delabere") == 0)
        ok();
    else
        no();
    
    return (0);
}
