#include <iostream>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
using namespace std;
#define min(x, y) (x) > (y)? (y) : (x) 
#define max(x, y) (x) > (y)? (x) : (y)

 
#define MAXN 10             
int NX, NY; 
double **G, **GG;
int *CX, *CY, *XL, *YL, *S, *T;   
double delta_l = 0; //change of lable 

void labelchange() {
    for ( int i = 0; i < MAXN; i++ ) { 
        if (S[i]) XL[i] -= delta_l;
        if (T[i]) YL[i] += delta_l;
    }   
}

int dfs(int u) {
    S[u] = 1;
    for(int v = 0; v < NY; v++) {
        if(T[v]) continue; 
        double tmp = XL[u] + YL[v] + G[u][v];     // + G[u][v] -> min cost / - G[u][v] -> max_cost 
        if(tmp == 0) {
            T[v] = 1;
            if(CY[v] == -1 || dfs(CY[v]) == 1){
                CX[u] = v;     
                CY[v] = u;   
                return 1;
            }
        } else {
            delta_l = min(tmp, delta_l); 
        }
    }
    return 0;      
}
 
void maxMatch() {  
    int res = 0;
    for (int i = 0; i < NX; i++) {
        for (int j = 0; j < MAXN; j++) S[j] = T[j] = 0;
        delta_l = INT_MAX;
        while(dfs(i) == 0) {
            labelchange();
            for (int j = 0; j < MAXN; j++) S[j] = T[j] = 0; 
            delta_l = INT_MAX;
        }
    }
}

// check
void init() {
    NX = 3; NY = 3; 

    CX = (int*) malloc(MAXN * sizeof(int)); 
    CY = (int*) malloc(MAXN * sizeof(int));
    XL = (int*) malloc(MAXN * sizeof(int));
    YL = (int*) malloc(MAXN * sizeof(int));
    S  = (int*) calloc(MAXN,  sizeof(int));
    T  = (int*) calloc(MAXN,  sizeof(int));

    G =  (double**) calloc(MAXN, sizeof(double*));
    for (int i = 0; i < MAXN; i++) G[i] = (double*) calloc(MAXN, sizeof(double));
    GG = (double**) calloc(MAXN, sizeof(double*));
    for (int i = 0; i < MAXN; i++) GG[i] = (double*) calloc(MAXN, sizeof(double));

    for (int i = 0; i < MAXN; i++) {
        XL[i] = INT_MIN;
    }

    for(int i = 0; i < MAXN; i++) {
        CX[i] = -1; 
        CY[i] = -1; 
    }   

    GG[0][0] = 43; GG[0][1] = 21; GG[0][2] = 1;
    GG[1][0] = 50; GG[1][1] = 95; GG[1][2] = 93; 
    GG[2][0] =  0; GG[2][1] =  0; GG[2][2] = 0;

    G[0][0] = 37; G[0][1] = 12; G[0][2] = 72;
    G[1][0] = 9; G[1][1] = 75; G[1][2] = 5; 
    G[2][0] = 79; G[2][1] = 64; G[2][2] = 16;

    for ( int i = 0; i < NX; i++ ) {
        for ( int j = 0; j < NY; j++ ) {
            if ( G[i][j] > XL[i] ) XL[i] = G[i][j];
        }
    }
}

void free() {
    memset(CX, 0, sizeof(CX));
    memset(CY, 0, sizeof(CY));
    memset(G,  0, sizeof(G));
    memset(GG, 0, sizeof(GG));
    memset(S,  0, sizeof(S));
    memset(T,  0, sizeof(T));
    memset(XL, 0, sizeof(XL));
    memset(YL, 0, sizeof(YL));

    free(G); free(GG); free(CX); free(CY); free(S); free(T); free(XL); free(YL);
}
 
int main() {

    init(); 
    maxMatch();

    int cost = 0;
    for(int num = 0; num < NX; ++num){
        cout << "CX[" << num+1 << "] -> "<< CX[num] + 1 << endl;
        cost += G[num][CX[num]];
    }
    cout << "cost = " << cost << endl; // prints !!!Hello World!!!

    free();    
    return 0;
}
