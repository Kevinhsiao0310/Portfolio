#include <iostream>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
using namespace std;
 
#define MAXN 10             
int nx,ny;                            
int g[MAXN][MAXN]; 
int gg[MAXN][MAXN];               
int cx[MAXN],cy[MAXN];       
int mk[MAXN];
 
int path(int u){
    for(int v=0;v<ny;v++){     
        if(g[u][v]!=0 && mk[v]==0){   
            mk[v]=1;             
            if(cy[v]==-1 || path(cy[v])){
                cx[u]=v;     
                cy[v]=u;   
                return 1;
            }
            mk[v] = 0;
        }
    }
    return 0;      
}
 
int maxMatch(){  
    int res=0;
    memset(cx,-1,sizeof(cx));    
    memset(cy,-1,sizeof(cy));
    memset(mk, 0,sizeof(mk)); 
    for(int i=0;i<nx;i++){
        if(cx[i]==-1){  
            //memset(mk, 0,sizeof(mk));           
            res+=path(i);
        }
    }
    return res;
}
 
int main() {

    /*
    printf("row?\n");
    scanf("%d", &nx);
    printf("col?\n");
    scanf("%d", &ny);

    // make array
    int value = 0;
    for(int i=0; i<nx; i++){
        for(int j=0; j<ny; j++){
            g[i][j] = value;
            printf("%d ", value);
            value++;
        }
        printf("\n");
    }
    */

    gg[0][0] = 43; gg[0][1] = 21; gg[0][2] = 1;
    gg[1][0] = 50; gg[1][1] = 95; gg[1][2] = 93;
    gg[2][0] =  0; gg[2][1] =  0; gg[2][2] = 0;

    g[0][0] = 42; g[0][1] = 20; g[0][2] = 0;
    g[1][0] = 0; g[1][1] = 45; g[1][2] = 43;
    g[2][0] = 0;  g[2][1] = 0;  g[2][2] = 0;
 
    nx = 3;
    ny = 3;
 
    int num= maxMatch();
    int cost = 0;
    cout<<"num="<<num<<endl;
    for(int num=0;num<nx;++num){
        cout<<"cx["<<num+1<<"]  -> "<<cx[num]+1<<endl;
        cost += gg[num][cx[num]];
    }
    cout << "cost = " << cost << endl; // prints !!!Hello World!!!
    return 0;
}
