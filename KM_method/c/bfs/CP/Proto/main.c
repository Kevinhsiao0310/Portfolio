#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>
#include "PMX_KM.h"

int main() {

    int seed = 0;
    printf("seed = %d\n", seed);
    TaskAssignment tt;
    TaskAssignment ttt;

    initTask(&tt, 3,3); 
    //print_CostTable(&tt, 1);
    maxMatch_bfs(&tt);

    int cost = 0;
    for (int i = 0; i < tt.nx; i++) {
        //printf("cx[%d] -> %d\n", i + 1, tt.cx[i] + 1);
        cost += tt.g[i][tt.cx[i]];
    }
    //printf("cost = %d\n", cost);


    initTask(&ttt, 3,3);
    //print_CostTable(&ttt, 1);
    maxMatch_dfs(&ttt);

    int costt = 0;
    for (int i = 0; i < ttt.nx; i++) {
        //printf("cx[%d] -> %d\n", i + 1, ttt.cx[i] + 1);
        costt += ttt.g[i][ttt.cx[i]];
    }
    //printf("cost = %d\n", cost);
    if (cost != costt) printf("Not solved, cost_bfs = %d, cost_dfs = %d\n", cost, costt);

    return 0;
} 
