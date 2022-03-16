#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#include "KM_class.h"

int main() {

    TaskAssignment tt;
    int x = 2;
    int y = 2;

    init(&tt, x, y);

    tt.g[0][0] = 0;
    tt.g[0][1] = 1.0;
    tt.g[1][0] = 0.056500;
    tt.g[1][1] = 1.0; 

    for(int u = 0; u < x; u++){
        for(int v = 0; v < y; v++){    
            printf("task->g[%d][%d]=%lf\n", u, v, tt.g[u][v]);
        }
    } 

    maxMatch(&tt);

    double cost = 0;
    for (int i = 0; i < tt.nx; i++) {
        printf("cx[%d] -> %d\n", i + 1, tt.cx[i] + 1);
        cost += tt.g[i][tt.cx[i]];
    }
    printf("cost = %lf\n", cost);

    free_task(&tt);    
    return 0;
}              
