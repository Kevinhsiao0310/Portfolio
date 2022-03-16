#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "KM_class.h"
#define min(x, y) (x) > (y)? (y) : (x) 
#define max(x, y) (x) > (y)? (x) : (y) 


void init(TaskAssignment *task, int x, int y) {
    
    task->nx = x;
    task->ny = y;
    task->maxn = max(x,y);

    task->delta_l = INT_MAX;

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

    for (int u = 0; u < x; u++){
        for(int v = 0; v < y; v++){    
            printf("task->g[%d][%d]=%lf\n", u, v, task->g[u][v]);
        }
    } 

    for (int i = 0; i < task->maxn; i++) {
        task->cx[i] = -1; 
        task->cy[i] = -1; 
        task->xl[i] = INT_MIN;
        task->yl[i] = 0;
        task->s[i]  = 0;
        task->t[i]  = 0;
    }   

    for ( int i = 0; i < task->nx; i++ ) {
        for ( int j = 0; j < task->ny; j++ ) {
            if ( task->g[i][j] > task->xl[i] ) task->xl[i] = task->g[i][j];
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


//TODO bfs
void bfs(TaskAssignment *task, int startX) {
    //printf("startX:%d\n", startX);

    int find = 0;                //boolean find = false;
    int endY = -1; 
    int yPre[task->maxn]; 
    int queue[task->maxn];
    for (int i = 0; i < task->maxn; i++) {
        yPre[i]  = -1;
        queue[i] =  0;
    }

    int qs = 0, qe = 0;          // 队列开始结束索引
    queue[qe++] = startX;

    while (1) {               // 循环直到找到匹配
        //printf("a\n");
        while (qs < qe && find==0) {   // 队列不为空
            //printf("b\n");
            int x = queue[qs++];
            //printf("queue: qs = %d, qe = %d\n", qs, qe);
            task->s[x] = 1;
            for (int y = 0; y < task->ny; y++) {
                int tmp = task->xl[x] + task->yl[y] + task->g[x][y];
                //printf("y = %d\n", y);
                if (tmp == 0) {  // 相等子树中的边
                    if (task->t[y]) continue;
                    task->t[y] = 1;
                    yPre[y] = x;
                    if (task->cy[y] == -1) {
                        endY = y;
                        find = 1;
                        break;
                    } else {
                        queue[qe++] = task->cy[y];
                    }
                } else {      // 不在相等子树中的边，记录一下最小差值
                    task->delta_l = min(task->delta_l, tmp);
                }
                //printf("xl[%d] = %d, yl->[%d] = %d, g[x][y] = %lf, delta_l = %d\n", x, task->xl[x], y, task->yl[y], task->g[x][y], task->delta_l);
            }
        }
        if (find) break;

        qs = 0, qe = 0;
        for ( int i = 0; i < task->maxn; i++ ) {  // 根据a修改标号值
            if (task->s[i]) {
                //printf("label changed x, delta_l = %d\n", task->delta_l);
                task->xl[i] -= task->delta_l;
                queue[qe++] = i;        // 把所有在S中的点加回到队列中
            }
            if (task->t[i]) {
                //printf("label changed y, delta_l = %d\n", task->delta_l);
                task->yl[i] += task->delta_l;
            }
        }
        task->delta_l = INT_MAX; //Integer.MAX_VALUE;
    }

    int count = 0;
    while (endY != -1) {       // 找到可扩路最后的y点后，回溯并扩充
        int preX = yPre[endY], preY = task->cx[preX];
        //printf("c, preX=%d, preY=%d\n", preX, task->cx[preX]);
        task->cx[preX] = endY;
        task->cy[endY] = preX;
        endY = preY;
        count++;
    }
}

void solve(TaskAssignment *task) { // 入口，输入权重矩阵
    for ( int x = 0; x < task->nx; x++ ) {
        for (int i = 0; i < task->maxn; i++) task->s[i] = task->t[i] = 0;
        bfs(task, x);
    }
}

//TODO


int main() {

    TaskAssignment tt;

    init(&tt, 3,3); 
    solve(&tt);

    int cost = 0;
    for (int i = 0; i < tt.nx; i++) {
        printf("cx[%d] -> %d\n", i + 1, tt.cx[i] + 1);
        cost += tt.g[i][tt.cx[i]];
    }
    printf("cost = %d\n", cost);

    //free_task(&tt);    
    return 0;
} 
             
