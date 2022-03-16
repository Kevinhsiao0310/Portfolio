#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>
#define MINN(x, y) (x) > (y)? (y) : (x) 
#define MAXX(x, y) (x) > (y)? (x) : (y) 


typedef struct{
    int nx; 
    int ny;
    int maxn; 
    int *cx;
    int *cy;
    int *xl;
    int *yl;
    int *s;
    int *t;
    int delta_l;
    double **g;
} TaskAssignment;


void initTask(TaskAssignment *task, int x, int y); 
void labelchange(TaskAssignment *task); 
int  dfs(TaskAssignment *task, int u); 
void maxMatch(TaskAssignment *task);  
void freeTask(TaskAssignment *task); 
