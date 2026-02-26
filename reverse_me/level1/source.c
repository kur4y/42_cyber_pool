#include <stdio.h>
#include <string.h>


int main(int ac, char **av)
{
    if (ac == 2)
    {
        if (!(strcmp(av[1], "__stack_check")))
        {
            printf("Good job!\n");
            return (0);
        }
        else
        {
            printf("Nope.\n");
            return (1);
        }
    }
    printf("Usage: %s password.\n", av[0]);
    return (1);
}
