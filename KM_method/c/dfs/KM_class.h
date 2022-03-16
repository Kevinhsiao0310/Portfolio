#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#define min(x, y) (x) > (y)? (y) : (x) 
#define max(x, y) (x) > (y)? (x) : (y)

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
    double delta_l;
    double **g;
} TaskAssignment;


void init(TaskAssignment *task, int x, int y); 
void labelchange(TaskAssignment *task); 
int  dfs(TaskAssignment *task, int u); 
void maxMatch(TaskAssignment *task);  
void free_task(TaskAssignment *task); 
