/*
* @brief arquivo de cabeçalho para arvore k dimensional utilizada no trabalho pratico
* autores : Augusto G.Lima, Cauã M.Pereira, Heitor G.Leite
* histórico : 20250528 arquivo criado
*/

#ifndef KDTREE_H
#define KDTREE_H

#include<vector>
#include"kdcell.hpp"

using K=2;

class kdtree_t
{
private:

    ptr_kdcell_t root;
    ptr_kdcell_t insert_recursive(ptr_kdcell_t cell, ptr_kdcell_t new_cell, int depth);
    void ortogonal_search_recursive(ptr_kdcell_t cell, const coordinates_t& lower, const coordinates_t& upper, int depth, std::vector<ptr_kdcell_t>& result);
    
public:
    kdtree():root(nullptr){}
    void insert(ptr_kdcell_t new_cell);
    std::vector<ptr_kdcell_t> ortogonal_search(const coordinates_t& lower, const coordinates_t& upper);
};

#endif // KDTREE_HPP