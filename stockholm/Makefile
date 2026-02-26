# colors
GREEN   = \033[1;32m
RED     = \033[1;31m
CYAN    = \033[96m
RESET   = \033[0m

# variables
NAME 	= 	stockholm
SCRIPT 	=	stockholm.py

all		:	$(NAME)

$(NAME)	:
			@echo "$(CYAN)Creating Stockholm program...$(RESET)"
			cp $(SCRIPT) $(NAME)
			chmod +x $(NAME)
			@echo "$(GREEN)Stockholm program has been created!$(RESET)"

clean	:
			
			@echo "$(RED)Erasing Stockholm program...$(RESET)"
			rm -f $(NAME)
			@echo "$(GREEN)Done!$(RESET)"

fclean	:	clean

re		:	fclean all

.PHONY	:	all clean fclean re
