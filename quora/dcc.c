/*
 * Author : mourad mourafiq (07/01/2012)
 *
 * This is an attempr to solve the datacenter cooling problem
 */
#include <stdio.h>
#include <stdlib.h>

//constants
#define VISITED_ROOM '4'
#define GO_ROOM '0'
#define NOGO_ROOM '1'
#define ENTRY_ROOM '2'
#define EXIT_ROOM '3'

//global variables
char **rooms;
int *to_check;
int nbr_rooms;
int H;
int W;
int nbr_rooms_visited=0;
int nbr_ways=0;

int way_exists(int l, int c){
	int i, j;
	int result = 0;
	int nbr_to_check = (nbr_rooms - nbr_rooms_visited)*2;
	int count_added = 0;
	if (c > 0){
		if (rooms[l][c-1] == GO_ROOM){
			rooms[l][c-1] = VISITED_ROOM;
			//nbr_to_check--;
			to_check[count_added++] = l;
			to_check[count_added++] = c-1;
		}
		else if (rooms[l][c-1] == EXIT_ROOM){
			result = 1;
		}
	}
	if (l > 0){
		if (rooms[l-1][c] == GO_ROOM){
			rooms[l-1][c] = VISITED_ROOM;
			//nbr_to_check--;
			to_check[count_added++] = l-1;
			to_check[count_added++] = c;
		}
		else if (rooms[l-1][c] == EXIT_ROOM){
			result = 1;
		}
	}
	if (c+1 < W){
		if (rooms[l][c+1] == GO_ROOM){
			rooms[l][c+1] = VISITED_ROOM;
			//nbr_to_check--;
			to_check[count_added++] = l;
			to_check[count_added++] = c+1;
		}
		else if (rooms[l][c+1] == EXIT_ROOM){
			result = 1;
		}
	}
	if (l+1 < H){
		if (rooms[l+1][c] == GO_ROOM){
			rooms[l+1][c] = VISITED_ROOM;
			//nbr_to_check--;
			to_check[count_added++] = l+1;
			to_check[count_added++] = c;
		}
		else if (rooms[l+1][c] == EXIT_ROOM){
			result = 1;
		}
	}
	if (result == 1){
		for (i=0; i<count_added; i+=2){
			rooms[to_check[i]][to_check[i+1]] = GO_ROOM;
		}
		return result;
	}
	if (count_added == 0){
		return 0;
	}
	int cpt = 0;
	int exit_found = 0;
    while(1){
        int cl = to_check[cpt++];
        int cc = to_check[cpt++];
        if (cc > 0){
            if (rooms[cl][cc-1] == GO_ROOM){
                rooms[cl][cc-1] = VISITED_ROOM;
                //nbr_to_check--;
                to_check[count_added++] = cl;
                to_check[count_added++] = cc-1;
            }
            else if (rooms[cl][cc-1] == EXIT_ROOM)
                	exit_found = 1;
        }
        if (cl > 0){
            if (rooms[cl-1][cc] == GO_ROOM){
                rooms[cl-1][cc] = VISITED_ROOM;
                //nbr_to_check--;
				to_check[count_added++] = cl-1;
		        to_check[count_added++] = cc;
            }
            else if (rooms[cl-1][cc] == EXIT_ROOM)
                	exit_found = 1;
        }
        if (cc+1 < W){
            if (rooms[cl][cc+1] == GO_ROOM){
                rooms[cl][cc+1] = VISITED_ROOM;
                //nbr_to_check--;
                to_check[count_added++] = cl;
                to_check[count_added++] = cc+1;
            }
            else if (rooms[cl][cc+1] == EXIT_ROOM)
                	exit_found = 1;
        }
        if (cl+1 < H){
            if (rooms[cl+1][cc] == GO_ROOM){
                rooms[cl+1][cc] = VISITED_ROOM;
                //nbr_to_check--;
                to_check[count_added++] = cl+1;
                to_check[count_added++] = cc;
            }
            else if (rooms[cl+1][cc] == EXIT_ROOM)
                	exit_found = 1;
        }
        if ((nbr_to_check == count_added) && (exit_found == 1)){
        	result = 1;
        	break;
        }
        if (cpt >= count_added){
        	result = 0;
        	break;
        }
    }
    for (i=0; i<count_added; i+=2){
		rooms[to_check[i]][to_check[i+1]] = GO_ROOM;
	}
	return result;
}

long find_ways(int l, int c){
	if (way_exists(l, c) == 0){
		return 0;
	}
	if (c > 0){
		if (rooms[l][c-1] == GO_ROOM){
			rooms[l][c-1] = VISITED_ROOM;
			nbr_rooms_visited++;
			find_ways(l, c-1);
			rooms[l][c-1] = GO_ROOM;
			nbr_rooms_visited--;
		}
		else if ((rooms[l][c-1] == EXIT_ROOM) && (nbr_rooms_visited == nbr_rooms)){
				nbr_ways++;
				return 1;
		}
	}
	if (l > 0){
		if (rooms[l-1][c] == GO_ROOM){
			rooms[l-1][c] = VISITED_ROOM;
			nbr_rooms_visited++;
			find_ways(l-1, c);
			rooms[l-1][c] = GO_ROOM;
			nbr_rooms_visited--;
		}
		else if ((rooms[l-1][c] == EXIT_ROOM) && (nbr_rooms_visited == nbr_rooms)){
				nbr_ways++;
				return 1;
		}
	}
	if (c+1 < W){
		if (rooms[l][c+1] == GO_ROOM){
			rooms[l][c+1] = VISITED_ROOM;
			nbr_rooms_visited++;
			find_ways(l, c+1);
			rooms[l][c+1] = GO_ROOM;
			nbr_rooms_visited--;
		}
		else if ((rooms[l][c+1] == EXIT_ROOM) && (nbr_rooms_visited == nbr_rooms)){
				nbr_ways++;
				return 1;
		}
	}
	if (l+1 < H){
		if (rooms[l+1][c] == GO_ROOM){
			rooms[l+1][c] = VISITED_ROOM;
			nbr_rooms_visited++;
			find_ways(l+1, c);
			rooms[l+1][c] = GO_ROOM;
			nbr_rooms_visited--;
		}
		else if ((rooms[l+1][c] == EXIT_ROOM) && (nbr_rooms_visited == nbr_rooms)){
				nbr_ways++;
				return 1;
		}
	}
	return 0;
}

int main(int argc, char* argv[]){
	int i, j, start_l, start_c;
	scanf("%d %d\n", &W, &H);
	nbr_rooms = W * H - 2;
	char line[sizeof(char)*(W+2)*2];
	rooms = (char **) malloc(H * sizeof(char *));
	for (i=0; i<H; i++){
		rooms[i] = (char *) malloc(W*sizeof(char));
		fgets(line, sizeof(char)*(W+2)*2, stdin);
		for (j=0; j<W; j++){
			rooms[i][j] = line[2*j];
			//Now checks whether we can identify the start and goal state
			if (rooms[i][j] == ENTRY_ROOM){
				start_l = i;
				start_c = j;
			}else if(rooms[i][j] == NOGO_ROOM){
				nbr_rooms -= 1;
			}
		}
	}
	to_check = (int *) malloc(nbr_rooms*2*sizeof(int));
	find_ways(start_l, start_c);
	printf("%d\n", nbr_ways);
	for (i= 0; i<H; i++){
			free(rooms[i]);
		}
	free(rooms);
	free(to_check);
	return 0;
}
