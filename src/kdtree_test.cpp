#include "kdtree.h"

#include <iostream>
#include <string>

using std::cout, std::endl;

int main() {
  KDTree<int, 2, std::string> t({
    {{0, 3}, "a"},
    {{1, 1}, "b"},
    {{1, 4}, "c"},
    {{2, 3}, "d"},
    {{3, 1}, "e"},
    {{3, 2}, "f"},
    {{4, 0}, "g"},
    {{4, 3}, "h"},
    {{4, 4}, "i"},
    {{5, 2}, "j"},
    {{5, 3}, "k"},
    {{6, 2}, "l"}
  });

  for (auto[p, d] : t.search({1, 1}, {3, 3}))
    cout << d << "(" << p[0] << "," << p[1] << ") ";
  std::cout << endl;

  t.insert({{2,2}, "m"});
  
  for (auto[p, d] : t.search({1, 1}, {3, 3}))
    cout << d << "(" << p[0] << "," << p[1] << ") ";
  std::cout << endl;
}
