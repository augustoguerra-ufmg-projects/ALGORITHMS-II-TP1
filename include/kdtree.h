#ifndef KDTREE_H
#define KDTREE_H

#include <algorithm>
#include <vector>
#include <array>
#include <utility>

using std::vector;
using std::array;
using std::pair;
using std::nth_element;

/**
 * T      : tipo das coordenadas
 * K      : número de dimensões
 * Data   : tipo dos dados associados aos pontos
 *
 * TODO: suportar remoção, usar smart pointers
 */
template<typename T, size_t K, typename Data>
class KDTree { 
public:
  using Point = array<T, K>;
  using Pair = pair<Point, Data>;

  struct Node {
    Node(Point p) : point(p) {};
    Node(Point p, Data d) : point(p), data(d) {};
    Node(Pair p) : point(p.first), data(p.second) {};

    Point point;
    Data data;
    Node *left = nullptr, *right = nullptr; 
  };

  KDTree() {};
  KDTree(const vector<Pair>& pairs) { build(pairs); }

  void insert(const Pair& p) {
    if (root == nullptr) {
      root = new Node(p);
      return;
    }
    insert(p, root, 0);
  }

  vector<Pair> search(const Point& lower, const Point& upper) {
    vector<pair<Point, Data>> res;
    search(lower, upper, root, 0, res);
    return res;
  }

private:
  Node* root = nullptr;
  
  void build(const vector<Pair>& points) {
    vector<Pair> copy = points;
    root = build(copy.begin(), copy.end(), 0);
  }

  // Usamos iterators para chamar nth_element (mediana em tempo linear)
  Node* build(typename vector<Pair>::iterator begin, typename vector<Pair>::iterator end, size_t depth) {
    if (begin >= end) return nullptr;

    size_t d = depth%K;
    typename vector<Pair>::iterator mid = begin + (end-begin)/2;
    nth_element(begin, mid, end, [d](const Pair& a, const Pair& b) {
      return a.first[d] < b.first[d];
    });

    Node* n = new Node(*mid);
    n->left = build(begin, mid, depth+1);
    n->right = build(mid+1, end, depth+1);
    return n;
  }
  
  Node* insert(const Pair& pair, Node* node, const size_t depth) {
    if (node == nullptr)
      return new Node(pair);
    
    size_t d = depth % K;
    if (pair.first[d] < node->point[d]) node->left = insert(pair, node->left, depth+1);
    else node->right = insert(pair, node->right, depth+1);

    return node;
  }

  void search(const Point& lower, const Point& upper, Node* node, const size_t depth, vector<pair<Point, Data>>& res) {
    if (node == nullptr) return;

    bool ok = true;
    for (size_t d = 0; d < K; d++) {
      ok &= (node->point[d] >= lower[d]);
      ok &= (node->point[d] <= upper[d]);
    }
    if (ok) res.push_back({node->point, node->data});

    size_t d = depth % K;
    if (node->point[d] >= lower[d])
      search(lower, upper, node->left, depth+1, res);
    if (node->point[d] <= upper[d])
      search(lower, upper, node->right, depth+1, res);
  }
};

#endif
