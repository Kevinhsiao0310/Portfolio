#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>
#include <sys/time.h>
#define minn(x, y) (x) > (y)? (y) : (x) 
#define maxx(x, y) (x) > (y)? (x) : (y) 
#define MAX_T 300

typedef struct {
    int nx; 
    int ny;
    int maxn; 
    int delta_l;
    int cost;
    int cx[MAX_T];
    int cy[MAX_T];
    int xl[MAX_T];
    int yl[MAX_T];
    int s[MAX_T];
    int t[MAX_T];
    int Yslack[MAX_T];
    int queue[MAX_T];
    int Ypre[MAX_T];
    int g[MAX_T][MAX_T];
} TaskAssignment;

void initTask(TaskAssignment *task, int x, int y) // x means num of AI, y means num of trackinglist
{
    task->nx = x;
    task->ny = y;
    task->maxn = maxx(x, y);
    task->delta_l = 0;
    task->cost = 0;

    // reset to defalut
    for (int u = 0; u < MAX_T; u++) {
        task->cx[u] = -1;
        task->cy[u] = -1;
        task->xl[u] = INT_MIN;
        task->yl[u] = 0;
        task->s[u]  = 0;
        task->t[u]  = 0; 
        for (int v = 0; v < MAX_T; v++) task->g[u][v] = 1e8;
    } 
} 

void print_CostTable(TaskAssignment* table) 
{
    printf("\n  ====COST====\n"); 
    for (int u = 0; u < table->maxn; u++) {
        printf("[");
        for(int v = 0; v < table->maxn; v++) { 
            printf("%d\t", table->g[u][v]);
        }   
        printf("]\n");
    }   
    printf("\n");
}

void set_Table(TaskAssignment *task)
{
    //print_CostTable(task);
    // preparing cost table
    for (int i = 0; i < task->maxn; i++ ) {
        for (int j = 0; j < task->maxn; j++ ) {
            if ( task->g[i][j] > task->xl[i] ) task->xl[i] = task->g[i][j];
        }
    }
}

//// dfs ////
int dfs(TaskAssignment *task, int u) 
{
    task->s[u] = 1;
    for(int v = 0; v < task->maxn; v++) {
        if(task->t[v]) continue; 
        int tmp = (int) task->xl[u] + task->yl[v] + task->g[u][v];      // + task->g[u][v] -> min cost / - task->g[u][v] -> max_cost
        if(tmp == 0) {
            task->t[v] = 1;
            if(task->cy[v] == -1 || dfs(task, task->cy[v]) == 1){
                task->cx[u] = v;     
                task->cy[v] = u;   
                return 1;
            }
        } else {
            task->delta_l = minn(tmp, task->delta_l);
        }
    }
    return 0;      
}

void maxMatch_dfs(TaskAssignment *task, int _PRINT_LOG) 
{ 
    struct timeval mstart, mend;
    gettimeofday(&mstart, NULL); 

    for (int i = 0; i < task->maxn; i++) {
        for (int j = 0; j < task->maxn; j++) task->s[j] = task->t[j] = 0;
        task->delta_l = INT_MAX;
        while(dfs(task, i) == 0) {
            for (int j = 0; j < task->maxn; j++ ) { 
                if (task->s[j]) task->xl[j] -= task->delta_l;
                if (task->t[j]) task->yl[j] += task->delta_l;
            }   

            for (int j = 0; j < task->maxn; j++) task->s[j] = task->t[j] = 0; 
            task->delta_l = INT_MAX;
        }
    }
    
    gettimeofday(&mend, NULL);
    if (_PRINT_LOG) printf("maxMatch_dfs cost %ld us\n", 1000000 * (mend.tv_sec - mstart.tv_sec) + mend.tv_usec - mstart.tv_usec);
}

//// bfs ////
void bfs(TaskAssignment *task, int xstart) 
{
    int find = 0;
    int endY = -1;
    int qs = 0;
    int qe = 0;

    task->queue[qe++] = xstart;
    while (find == 0) {
        while((qs < qe) && (find == 0)) {
            int x = task->queue[qs++];
            task->s[x] = 1;
            for (int y = 0; y < task->maxn; y++) {
                if (task->t[y] == 1) {
                    continue;
                }
                int tmp = task->xl[x] + task->yl[y] + task->g[x][y];
                if (tmp == 0) {
                    task->t[y] = 1;
                    task->Ypre[y] = x;
                    if (task->cy[y] == -1) {
                        endY = y;
                        find = 1;
                        break;
                    } else {
                        task->queue[qe++] = task->cy[y];
                    }   
                } else if (task->Yslack[y] > tmp) {
                    task->Yslack[y] = tmp;
                    task->Ypre[y] = x; 
                }
            }
        }
        if (find) break;

        task->delta_l = INT_MAX;
        for (int y = 0; y < task->maxn; y++) {
            if (task->t[y] == 0) task->delta_l = minn(task->delta_l, task->Yslack[y]);
        }
        for (int i = 0; i < task->maxn; i++) {
            if (task->s[i]) task->xl[i] -= task->delta_l;
            if (task->t[i]) task->yl[i] += task->delta_l;
        }

        qs = 0;
        qe = 0;

        for (int y = 0; y < task->maxn; y++) {
            if ((task->t[y] == 0) && (task->Yslack[y] == task->delta_l)) {
                task->t[y] = 1;
                if (task->cy[y] == -1) {
                    endY = y;
                    find = 1;
                    break;
                } else {
                    task->queue[qe++] = task->cy[y];
                }
            }
            task->Yslack[y] -= task->delta_l;    
        }
    }

    while (endY != -1) {
        int preX = task->Ypre[endY];
        int preY = task->cx[preX];
        task->cx[preX] = endY;
        task->cy[endY] = preX;
        endY = preY;
    }
}

void maxMatch_bfs(TaskAssignment *task, int _PRINT_LOG) 
{
    struct timeval mstart, mend;
    gettimeofday(&mstart, NULL);

    for (int i = 0; i < task->maxn; i++) {
        for (int j = 0; j < MAX_T; j++) {
             task->s[j]      = 0;
             task->t[j]      = 0;
             task->Ypre[j]   = -1;
             task->queue[j]  = 0;
             task->Yslack[j] = INT_MAX;
        }
        bfs(task, i);
    }
    gettimeofday(&mend, NULL);
    if (_PRINT_LOG) printf("maxMatch_bfs cost %ld us\n", 1000000 * (mend.tv_sec - mstart.tv_sec) + mend.tv_usec - mstart.tv_usec);
}

void allocate_CostTable(TaskAssignment* table, int ai_num, int track_num, int _PRINT_LOG) 
{
    if (_PRINT_LOG) printf("init Cost: AInum:%d, Tracknum:%d\n", ai_num, track_num);
   
    ai_num = minn(ai_num, MAX_T);
    track_num = minn(track_num, MAX_T); 

    struct timeval mstart, mend;
    gettimeofday(&mstart, NULL);

    initTask(table, ai_num, track_num);
    gettimeofday(&mend, NULL);

    if (_PRINT_LOG) printf("initTask cost %ld us\n", 1000000 * (mend.tv_sec - mstart.tv_sec) + mend.tv_usec - mstart.tv_usec);      
}

void km_cost(TaskAssignment* table, int _PRINT_LOG) 
{
    struct timeval ustart, uend;
    gettimeofday(&ustart, NULL);

    double cost = 0;  
    for (int z = 0; z < table->nx; z++) {
        if (_PRINT_LOG) printf("cx[%d] -> %d\n", z + 1, table->cx[z] + 1);  
        cost += table->g[z][table->cx[z]];
    }        
    gettimeofday(&uend, NULL);

    if (_PRINT_LOG) {
        printf("min_cost:%lg\n\n", cost);
        printf("update cost %ld us\n", 1000000 * (uend.tv_sec - ustart.tv_sec) + uend.tv_usec - ustart.tv_usec);
    }

    table->cost = cost;
}

