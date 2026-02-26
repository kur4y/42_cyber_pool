# colors
GREEN   =	\033[1;32m
RED     =	\033[1;31m
CYAN    =	\033[96m
RESET   =	\033[0m

# commands
UP		=	docker compose -f docker-compose.yml up --build -d
DOWN	=	docker compose -f docker-compose.yml down -v --remove-orphans

all		:	up

up		:
			@echo "$(CYAN)Launching Inquisitor laboratory...$(RESET)"
			$(UP)
			@echo "$(GREEN)Environment ready!$(RESET)"

down	:
			@echo "$(RED)Erasing laboratory...$(RESET)"
			$(DOWN)
			rm -rf ftp_credentials.log
			@echo "$(GREEN)Done!$(RESET)"

fclean	: 	down
			@echo "$(RED)Hard reset...$(RESET)"
			docker network prune -f
			docker builder prune -f
			docker system prune -af
			@echo "$(GREEN)Done!$(RESET)"

re		:	fclean up

.PHONY	:	all up down re fclean
