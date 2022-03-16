#include <bits/stdc++.h>
#pragma comment(linker, “/STACK:1024000000,1024000000”)
#define INF 0x3f3f3f3f
#define LL long long
using namespace std;

const int AX = 3e2+6;
int w[AX][AX];
int lx[AX] , ly[AX];
int linker[AX];
int slack[AX];
int n ;
bool visy[AX];
int pre[AX];

void bfs( int k ){
    int x , y = 0 , yy = 0 , delta;
    memset( pre , 0 , sizeof(pre) );
    for( int i = 1 ; i <= n ; i++ ) slack[i] = INF;
    linker[y] = k;
    while(1){
        x = linker[y]; delta = INF; visy[y] = true;
        for( int i = 1 ; i <= n ;i++ ){
            if( !visy[i] ){
                if( slack[i] > lx[x] + ly[i] + w[x][i] ){
                    slack[i] = lx[x] + ly[i] + w[x][i];
                    pre[i] = y; 
                }
                if( slack[i] < delta ) delta = slack[i] , yy = i ;
            }
            printf("xl[%d] = %d, yl[%d] = %d, g[%d][%d] = %d, delta_l = %d\n", x, lx[x], i, ly[i], x, i, w[x][i], delta);
        }
        for( int i = 0 ; i <= n ; i++ ){
            if( visy[i] ) {
                lx[linker[i]] -= delta , ly[i] += delta;
                printf("label changed! delta = %d, i = %d\n", delta, i);
            }
            else slack[i] -= delta;
        }
        y = yy ;
        if( linker[y] == -1 ) break;
    }
    while( y ) linker[y] = linker[pre[y]] , y = pre[y];
}

void KM(){
    memset( lx ,  1e-8 , sizeof(lx) );
    memset( ly ,     0 , sizeof(ly) );
    memset( linker , -1, sizeof(linker) );

    for(int i = 1; i <= n; i++) {
        for(int j = 1; j <= n; j++) {
            if (w[i][j] > lx[i]) lx[i] = w[i][j]; 
        }
    }

    for( int i = 1 ; i <= n ; i++ ){
        memset( visy , false , sizeof(visy) );
        bfs(i);
    }
}

int main(){
    n = 3;

    w[1][1] = 37; w[1][2] = 12; w[1][3] = 26; 
    w[2][1] = 9;  w[2][2] = 75; w[2][3] = 5;
    w[3][1] = 79; w[3][2] = 64; w[3][3] = 16; 




    w[1][1] = 345353; w[1][2] = 760957;  w[1][3] = 881167;
    w[2][1] = 443712; w[2][2] =  617841; w[2][3] = 105595;
    w[3][1] = 533660; w[3][2] =  927705; w[3][3] = 299741;




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
/*
int main(){
    int x ;
    while( ~scanf("%d",&n) ){
        for( int i = 1 ; i <= n ; i++ ){
            for( int j = 1 ; j <= n ; j++ ){
                
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
