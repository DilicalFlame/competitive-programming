// Codeforces: https://codeforces.com/problemset/problem/4/A

#include <iostream>
#include <string>

using namespace std;

int main()
{
    int n;
    string ans;

    cin >> n;
    ans = (n == 2) ? "NO" : (n % 2 == 0) ? "YES"
                                         : "NO";
    cout << ans << endl;

    return 0;
}
