#include <nanobind/nanobind.h>
#include <nanobind/stl/bind_vector.h>
#include <nanobind/make_iterator.h>
#include <nanobind/stl/array.h>
#include <nanobind/stl/pair.h>
namespace nb = nanobind;

#include <vector>
using std::vector;

#include "kdtree.h"
using Tree = KDTree<long double, 2, size_t>;
using Point = Tree::Point;
using Pair = Tree::Pair;

NB_MODULE(kdtree, m) {
  nb::bind_vector<vector<Pair>>(m, "pair_vector");

  nb::class_<Tree>(m, "KDTree")
    .def(nb::init<>(), "Inicializa uma K-D Tree vazia.")
  
    .def(nb::init<const vector<Pair>&>(),
        "Constrói uma K-D Tree balanceada a partir de uma lista de pares (ponto, dado).",
        nb::arg("pairs"))

    .def("insert", nb::overload_cast<const Pair&>(&Tree::insert),
        "Insere um par (ponto, dado).",
        nb::arg("pair"))

    .def("search", nb::overload_cast<const Point&, const Point&>(&Tree::search),
        "Busca intervalar.",
        nb::arg("lower_bound"),
        nb::arg("upper_bound")
    );
}
