public class KM_DFS {

    private int[][] table = null;     // 权重矩阵（方阵）
    private int[] xl = null;          // X标号值
    private int[] yl = null;          // Y标号值
    private int[] xMatch = null;      // X点对应的匹配点
    private int[] yMatch = null;      // Y点对应的匹配点
    private int n = 0;                // 矩阵维度
    private int a = 0;                // 标号修改量

    public int solve(int[][] table) { // 入口，输入权重矩阵
        this.table = table;
        init();
        for ( int x = 0; x < n; x++ ) {  // 为每一个x寻找匹配
            boolean[] S = new boolean[n], T = new boolean[n]; // S集合，T集合
            a = Integer.MAX_VALUE;
            while ( !dfs(S, T, x) ) {   // 找到可扩路结束，否则修改标号值
                LModified(S, T);
                Arrays.fill(S, false);
                Arrays.fill(T, false);
                a = Integer.MAX_VALUE;
            }
        }
        int value = 0;
        for ( int x = 0; x < n; x++ ) {
            value += table[x][xMatch[x]];
        }
        return value;
    }

    private boolean dfs(boolean[] S, boolean[] T, int x) {  // 深度优先搜索
        S[x] = true;
        for ( int y = 0; y < n; y++ ) {
            if ( T[y] ) {
                continue;
            }
            int tmp = xl[x] + yl[y] - table[x][y];
            if ( tmp == 0 ) {  // 在相等子树中
                T[y] = true;
                if ( yMatch[y] == -1 || dfs(S, T, yMatch[y]) ) {     // 1. y顶点没有匹配，那么进行匹配
                    xMatch[x] = y;                                   // 2. dfs寻找可扩路成功，那么这条x，y就会因为可扩路的扩展而交换到匹配中
                    yMatch[y] = x;
                    return true;
                }
            } else {    // 不在相等子树中
                a = Math.min(tmp, a);
            }
        }
        return false;
    }

    private void init() {
        this.n = table.length;
        this.xl = new int[n];
        this.yl = new int[n];
        Arrays.fill(xl, Integer.MIN_VALUE);
        for ( int x = 0; x < n; x++ ) {
            for ( int y = 0; y < n; y++ ) {
                if ( table[x][y] > xl[x] ) {
                    xl[x] = table[x][y];
                }
            }
        }
        this.xMatch = new int[n];
        this.yMatch = new int[n];
        Arrays.fill(xMatch, -1);
        Arrays.fill(yMatch, -1);
    }

    private void LModified(boolean[] S, boolean[] T) { // 修改标号值
        for ( int i = 0; i < n; i++ ) {
            if ( S[i] ) {
                xl[i] -= a;
            }
            if ( T[i] ) {
                yl[i] += a;
            }
        }
    }
    
}
