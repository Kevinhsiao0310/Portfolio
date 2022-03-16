#include <bits/stdc++.h>
#pragma comment(linker, “/STACK:1024000000,1024000000”)
#define INF 0x3f3f3f3f
#define LL long long
using namespace std;
const int AX = 3e2+6;
bool visx[AX];
bool visy[AX];
int w[AX][AX];
int lx[AX] , ly[AX];  //可行性顶标
int linker[AX];  //记录匹配的边
int slack[AX];   //记录每个j相连的i的最小的lx[i]+ly[j]-w[i][j]
int n ;
bool dfs( int x ){
    visx[x] = true;
    for( int y = 1 ; y <= n ; y ++ ){
        if( !visy[y] && lx[x] + ly[y] == w[x][y] ){
            visy[y] = true;
            if( linker[y] == -1 || dfs( linker[y] ) ){
                linker[y] = x ;
                return true;
            }
        }else if( slack[y] > lx[x] + ly[y] - w[x][y] ){//x,y不在相等子图且y不在增广路
            slack[y] = lx[x] + ly[y] - w[x][y];
        }
    }
    return false;
}

void KM(){
    memset( linker , -1 , sizeof(linker) );
    memset( ly , 0 , sizeof(ly) );
    for( int i = 1 ; i <= n ; i++ ){
        lx[i] = -INF;
        for( int j = 1 ; j <= n ; j++ ){
            if( lx[i] < w[i][j] ) lx[i] = w[i][j];
        }
    }
    for( int x = 1 ; x <= n ; x++ ){
        for( int i = 1 ; i <= n ; i++ ) slack[i] = INF;//每次匹配x都要更新slack
        while(1){
            memset( visx , false , sizeof(visx) );
            memset( visy , false , sizeof(visy) );
            if( dfs(x) ){
                break;
            }else{ // 匹配失败后x一定在增广路，寻找不在增广路的j
                int delta = INF;
                for( int j = 1 ; j <= n ; j++ ){
                    if( !visy[j] && delta > slack[j] ){
                        delta = slack[j];
                    }
                }

                for( int i = 1 ; i <= n ; i++ ){
                    if( visx[i] ) lx[i] -= delta;
                }
                for( int i = 1 ; i <= n ; i++ ){
                    if( visy[i] ) ly[i] += delta;
                    else slack[i] -= delta;
                    //修改顶标后，要把所有的slack值都减去delta
                     //slack[j] = min(lx[i] + ly[j] -w[i][j])
                     //在增广路的lx[i]减少，所以不在增广路的slack[j]减小
                }
            }
        }
    }
}

/*
int main(){
    int x ;
    while( ~scanf("%d",&n) ){
        for( int i = 1 ; i <= n ; i++ ){
            for( int j = 1 ; j <= n ; j++ ){
                printf("inset: (%d,%d)\n", i, j);
                scanf("%d",&x);
                w[i][j] = x ;
            }
        }
        KM();
        int res = 0 ;
        for( int i = 1 ; i <= n ; i++ ){
            if( linker[i] != -1 ){
                res += w[linker[i]][i] ;
            }
        }
        printf("%d\n",res);
    }
    return 0 ;
}
*/

int main(){
    n = 3;

    w[1][1] = 37; w[1][2] = 12; w[1][3] = 26; 
    w[2][1] = 9;  w[2][2] = 75; w[2][3] = 5;
    w[3][1] = 79; w[3][2] = 64; w[3][3] = 16; 

    KM();
    int res = 0 ; 
    for( int i = 1 ; i <= n ; i++ ){
        if( linker[i] != -1 ){
            res += w[linker[i]][i] ;
        }
    }   
    printf("%d\n",res);
    return 0 ; 
}

