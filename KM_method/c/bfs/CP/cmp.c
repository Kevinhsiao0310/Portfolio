#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>
#include "PMX_KM.h"

int main() 
{
    int nx = 15;
    int ny = 13;  // size of costtable

    for (int seed = 0; seed < 10; seed++) {

        TaskAssignment tt; 
        TaskAssignment ttt;
  
        allocate_CostTable(&tt, nx, ny, 0);                                                                                                                                                             
        allocate_CostTable(&ttt, nx, ny, 0); 

        printf("seed = %d\n", seed);
        for (int x = 0; x < nx; x++) {
            for (int y = 0; y < ny; y++) {
                int r = rand() % 10000000 + 1;
                tt.g[x][y] = r;
                ttt.g[x][y] = r;      
            }
        }

        set_Table(&tt); 
        set_Table(&ttt); 

        maxMatch_bfs(&tt, 1);
        km_cost(&tt, 1);

        int cost = 0;
        for (int i = 0; i < tt.nx; i++) {
            cost += tt.g[i][tt.cx[i]];
        }

        maxMatch_dfs(&ttt, 1);
        km_cost(&ttt, 1);

        int costt = 0;
        for (int i = 0; i < ttt.nx; i++) {
            costt += ttt.g[i][ttt.cx[i]];
        }
        printf("cost = %d\n", cost);
        if (cost != costt) printf("Not solved, cost_bfs = %d, cost_dfs = %d\n", cost, costt);
    }
    return 0;
} 
