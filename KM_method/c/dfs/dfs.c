#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "KM_class.h"

void init(TaskAssignment *task, int x, int y) {
    
    task->nx = x;
    task->ny = y;
    task->maxn = max(x,y);
    task->delta_l = 0.;

    task->cx = (int*) malloc(task->maxn * sizeof(int)); 
    task->cy = (int*) malloc(task->maxn * sizeof(int));
    task->xl = (int*) malloc(task->maxn * sizeof(int));
    task->yl = (int*) malloc(task->maxn * sizeof(int));
    task->s  = (int*) calloc(task->maxn,  sizeof(int));
    task->t  = (int*) calloc(task->maxn,  sizeof(int));

    task->g =  (double**) calloc(task->maxn, sizeof(double*));
    for (int i = 0; i < task->maxn; i++) task->g[i] = (double*) calloc(task->maxn, sizeof(double));

    task->g[0][0] = 37; task->g[0][1] = 12; task->g[0][2] = 26;
    task->g[1][0] = 9;  task->g[1][1] = 75; task->g[1][2] = 5; 
    task->g[2][0] = 79; task->g[2][1] = 64; task->g[2][2] = 16;

    for(int u = 0; u < x; u++){
        for(int v = 0; v < y; v++){    
            printf("task->g[%d][%d]=%lf\n", u, v, task->g[u][v]);
        }
    } 

    for(int i = 0; i < task->maxn; i++) {
        task->cx[i] = -1; 
        task->cy[i] = -1; 
        task->xl[i] = INT_MIN;
        task->yl[i] = 0;
    }   

    for ( int i = 0; i < task->nx; i++ ) {
        for ( int j = 0; j < task->ny; j++ ) {
            if ( task->g[i][j] > task->xl[i] ) task->xl[i] = task->g[i][j];
        }
    }
}

void labelchange(TaskAssignment *task) {
    for ( int i = 0; i < task->maxn; i++ ) { 
        if (task->s[i]) task->xl[i] -= task->delta_l;
        if (task->t[i]) task->yl[i] += task->delta_l;
    }  
    printf("label changed, delta_l = %lf\n", task->delta_l); 
}

int dfs(TaskAssignment *task, int u) {
    task->s[u] = 1;
    for(int v = 0; v < task->ny; v++) {
        if(task->t[v]) continue; 
        int tmp = (int) task->xl[u] + task->yl[v] - task->g[u][v];      // + task->g[u][v] -> min cost / - task->g[u][v] -> max_cost
        printf("xl[%d] = %d, yl->[%d] = %d, g[x][y] = %lf\n", u, task->xl[u], v, task->yl[v], task->g[u][v]);
//        double temp = (double) tmp;
        //printf("tmp = %d\n", tmp);
        if(tmp == 0) {
            task->t[v] = 1;
            if(task->cy[v] == -1 || dfs(task, task->cy[v]) == 1){
                task->cx[u] = v;     
                task->cy[v] = u;   
                return 1;
            }
        } else {
            task->delta_l = min(tmp, task->delta_l);
            printf("u = %d, v = %d, delta_l = %lf, tmp = %d\n", u, v, task->delta_l, tmp);
        }
    }
    return 0;      
}

void maxMatch(TaskAssignment *task) {  
    int res = 0;
    for (int i = 0; i < task->nx; i++) {
        for (int j = 0; j < task->maxn; j++) task->s[j] = task->t[j] = 0;
        task->delta_l = INT_MAX;
        while(dfs(task, i) == 0) {
            labelchange(task);
            for (int j = 0; j < task->maxn; j++) task->s[j] = task->t[j] = 0; 
            task->delta_l = INT_MAX;
        }
    }
}

void free_task(TaskAssignment *task) {
    memset(task->cx, 0, sizeof(task->cx));
    memset(task->cy, 0, sizeof(task->cy));
    memset(task->g,  0, sizeof(task->g));
    memset(task->s,  0, sizeof(task->s));
    memset(task->t,  0, sizeof(task->t));
    memset(task->xl, 0, sizeof(task->xl));
    memset(task->yl, 0, sizeof(task->yl));

    free(task->g); free(task->cx); free(task->cy); free(task->s); free(task->t); free(task->xl); free(task->yl);
}

int main() {

    TaskAssignment tt;

    init(&tt, 3,3); 
    maxMatch(&tt);

    int cost = 0;
    for (int i = 0; i < tt.nx; i++) {
        printf("cx[%d] -> %d\n", i + 1, tt.cx[i] + 1);
        cost += tt.g[i][tt.cx[i]];
    }
    printf("cost = %d\n", cost);

    free_task(&tt);    
    return 0;
} 
             
