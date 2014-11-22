#include <iostream>
#include <sstream>
#include <vector>
#include <fstream>
#include <math.h>

void primeSum(unsigned long long *ret, int start, int n)
{
    int k, flag;
    *ret = 0;
    for (int i = start; i <= start + n; ++i)
    {
        flag = 1;
        if (i == 0 || i == 1) {
            flag = 0;
        } else {
            k = sqrt(i);
            for (int j = 2; j <= k; ++j)
                if (i % j == 0) {
                    flag = 0;
                    break;
                }
        }
        if (flag)
            *ret += i;
    }
}

int main(int argc, char** argv)
{
    if (argc != 2) 
    {
        std::cerr << "Usage: t2s N\n";
        return -1;
    }
    
    int n;
    if (!(std::stringstream(argv[1]) >> n))
    {
        std::cerr << argv[1] << " cannot be converted to an integer.\n";
        return -1;
    }
    
    unsigned long long sum;
    primeSum(&sum, 0, n);
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
