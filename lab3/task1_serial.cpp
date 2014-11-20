#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <vector>

int main(int argc, char** argv)
{
    if ((argc > 1 && (argv[1] == "-h" || argv[1] == "--help")) || argc != 3)
    {
        std::cerr << "Usage: t1s [-h|--help] N filename\n";
        return -1;
    }

    std::ifstream fin(argv[2]);
    if (fin.fail())
    {
        perror(argv[2]);
        return -1;
    }
    int n;
    if (!(std::stringstream(argv[1]) >> n))
    {
        std::cerr << argv[1] << " cannot be converted to an integer.\n";
        return -1;
    }

    float val;
    std::vector<float> data, output;
    while (fin >> val)
        data.push_back(val);
    
    output.resize(data.size() - n + 1, 0.0f);
    for (unsigned i = 0; i < data.size() - n + 1; ++i)
        for (int j = 0; j < n; ++j)
            output[i] += data[i + j];

    int m = 0;
    for (unsigned i = 1; i < output.size(); ++i)
        if (output[i] > output[m])
            m = i;

    std::cout << "Index: " << std::setw(10) << m << std::endl;
    std::cout << "Sum:   " << std::setw(10) << output[m] << std::endl;
}
